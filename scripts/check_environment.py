#!/usr/bin/env python3
"""Read-only local CLI check; host MCP/media tools must be inspected separately."""
import importlib.util
import json
import shutil
import sys
print(json.dumps({"python":sys.version.split()[0],"commands":{name:bool(shutil.which(name)) for name in ("ffmpeg","ffprobe","ancher","node","npx")},"asr_modules":{name:importlib.util.find_spec(name) is not None for name in ("faster_whisper","whisper")},"note":"这里只检测本地命令/模块，不代表已登录Ancher、具备字级对齐或已连接宿主工具。"},ensure_ascii=False,indent=2))
