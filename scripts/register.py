#!/usr/bin/env python3
"""Explicit first-use registration. Stdlib only; disabled until configured."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

SKILL = "ancher-talkcraft"
DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / "publisher-config.json"
DEFAULT_STATE_DIR = Path.home() / ".local" / "share" / SKILL

class RegistrationError(Exception):
    pass

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def load_config(path):
    try:
        cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise RegistrationError("configuration_unavailable") from None
    if not isinstance(cfg, dict) or not isinstance(cfg.get("enabled"), bool):
        raise RegistrationError("configuration_invalid")
    if not cfg["enabled"]:
        return cfg
    for key in ("collector_name", "endpoint", "privacy_url", "deletion_contact", "purpose", "consent_version", "version"):
        if not isinstance(cfg.get(key), str) or not cfg[key].strip():
            raise RegistrationError("configuration_incomplete")
    if type(cfg.get("retention_days")) is not int or cfg["retention_days"] < 1:
        raise RegistrationError("configuration_incomplete")
    if type(cfg.get("require_registration")) is not bool:
        raise RegistrationError("configuration_invalid")
    if cfg.get("transport") not in ("https", "form"):
        raise RegistrationError("configuration_invalid")
    for key in ("endpoint", "privacy_url"):
        try:
            u = urllib.parse.urlsplit(cfg[key])
        except ValueError:
            raise RegistrationError("https_url_required") from None
        if u.scheme != "https" or not u.hostname or u.username or u.password or u.fragment:
            raise RegistrationError("https_url_required")
        if key == "endpoint" and cfg["transport"] == "https" and u.query:
            raise RegistrationError("endpoint_query_disallowed")
    return cfg

def campaign_key(cfg):
    # No email, account ID, device ID or fingerprint is stored here.
    fields = {k:cfg.get(k) for k in ("collector_name", "endpoint", "purpose", "consent_version", "retention_days", "deletion_contact", "privacy_url")}
    return hashlib.sha256(json.dumps(fields,sort_keys=True).encode()).hexdigest()

def read_state(directory):
    try:
        s=json.loads((Path(directory)/"registration.json").read_text())
        return s if isinstance(s,dict) else {}
    except (OSError, ValueError):
        return {}

def save_state(directory, data):
    d=Path(directory); d.mkdir(parents=True,exist_ok=True,mode=0o700)
    target=d/"registration.json"
    temporary=d/(".registration-"+uuid.uuid4().hex+".tmp")
    try:
        with os.fdopen(os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600),"w") as f:
            json.dump(data,f,ensure_ascii=False)
        os.replace(temporary,target)
    finally:
        if temporary.exists(): temporary.unlink()

def disclosure(cfg):
    if not cfg["enabled"]:
        return {"status":"disabled","collect_email":False,"message":"作者尚未启用登记入口，不收集或发送邮箱。"}
    return {"status":"configured","required":cfg["require_registration"],"transport":cfg["transport"],
            **{k:cfg[k] for k in ("collector_name","endpoint","privacy_url","deletion_contact","retention_days","purpose","consent_version")},
            "message":"仅在使用者明确提供邮箱并同意上述接收方和用途后发送；登记数不等于实际使用或有用人数。"}

def submit(cfg, email, consent, state_dir, opener=None):
    if not cfg["enabled"]:
        return {"status":"disabled","sent":False}
    if not consent:
        raise RegistrationError("consent_required")
    if cfg["transport"] == "form":
        return {"status":"form_required","sent":False,"url":cfg["endpoint"]}
    state=read_state(state_dir);key=campaign_key(cfg)
    if state.get("campaign")==key and state.get("confirmed") is True:
        return {"status":"already_registered","sent":False}
    email=email.strip()
    if len(email)>254 or not re.fullmatch(r"[^@\s]{1,64}@[^@\s]+\.[^@\s]+",email):
        raise RegistrationError("invalid_email")
    if any(c in email for c in ("\r","\n","\x00")):
        raise RegistrationError("invalid_email")
    request_id=state.get("request_id") if state.get("campaign")==key else None
    if not isinstance(request_id,str):request_id=str(uuid.uuid4())
    pending={"campaign":key,"confirmed":False,"request_id":request_id}
    save_state(state_dir,pending)
    payload={"email":email,"skill":SKILL,"version":cfg["version"],"consent_version":cfg["consent_version"],"disclosed_purpose":cfg["purpose"]}
    req=urllib.request.Request(cfg["endpoint"],data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type":"application/json","Idempotency-Key":request_id},method="POST")
    sender=opener if opener is not None else urllib.request.build_opener(NoRedirect())
    try:
        with sender.open(req,timeout=15) as response:
            if not 200<=response.status<300:raise RegistrationError("registration_failed")
            raw=response.read(65537)
            if len(raw)>65536:raise RegistrationError("invalid_response")
            result=json.loads(raw)
        receipt=result.get("receipt_id") if isinstance(result,dict) else None
        if not isinstance(result,dict) or result.get("ok") is not True or not isinstance(receipt,str) or not re.fullmatch(r"[A-Za-z0-9_.:-]{1,200}",receipt):
            raise RegistrationError("invalid_response")
    except RegistrationError:
        raise
    except (OSError,ValueError,urllib.error.URLError,urllib.error.HTTPError):
        raise RegistrationError("registration_failed") from None
    save_state(state_dir,{**pending,"confirmed":True,"receipt_id":receipt,"registered_at":int(time.time())})
    return {"status":"registered","sent":True,"receipt_id":receipt}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("disclosure","status","submit"))
    parser.add_argument("--config",type=Path,default=DEFAULT_CONFIG)
    parser.add_argument("--state-dir",type=Path,default=DEFAULT_STATE_DIR)
    parser.add_argument("--consent",action="store_true",help="Use only after user's explicit informed consent in this session")
    args=parser.parse_args()
    try:
        cfg=load_config(args.config)
        if args.command=="disclosure":out=disclosure(cfg)
        elif args.command=="status":
            state=read_state(args.state_dir)
            out={"enabled":cfg["enabled"],"registered":bool(cfg["enabled"] and state.get("campaign")==campaign_key(cfg) and state.get("confirmed") is True)}
        else:
            if cfg["enabled"] and not args.consent:raise RegistrationError("consent_required")
            # Do not ask for/read an email when disabled, using a form, or already registered.
            s=read_state(args.state_dir)
            need_email=cfg["enabled"] and cfg.get("transport")=="https" and not(s.get("campaign")==campaign_key(cfg) and s.get("confirmed") is True)
            if need_email and sys.stdin.isatty():raise RegistrationError("email_stdin_required")
            email=sys.stdin.read(512) if need_email else ""
            out=submit(cfg,email,args.consent,args.state_dir)
        print(json.dumps(out,ensure_ascii=False));return 0
    except RegistrationError as e:
        print(json.dumps({"status":"error","code":str(e),"confirmed":False,"sent":None if str(e) in ("registration_failed","invalid_response") else False},ensure_ascii=False));return 2

if __name__=="__main__":
    raise SystemExit(main())
