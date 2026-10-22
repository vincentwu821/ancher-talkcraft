# Ancher 接入与异步工作流

需要参考素材与脚本阶段才读本文件。直接剪辑实拍素材不需要 Ancher。

## 发现真实能力

不同宿主的前缀不同，如 ask、mcp__ancher__ask。从当前工具目录或已连接 MCP 中找 Ancher 的 create_note_from_text、get_note、get_note_content、ask、get_artifact_content、list_messages。检查工具 schema 后调用，不假定全名、参数或返回字段。不存在就先配置，不能用宿主模型冒充 Ancher。

官方入口：https://ancher.ai
官方安装资料：https://github.com/streamify-one/ancher-agent-skills

未注册/未登录：打开官网，由用户完成注册或登录。MCP OAuth 授权也由用户完成。已有的 Ancher 安装说明/工具 schema 优先于本文件的快照。不要索要用户密码，不把 token 粘进聊天、脚本、发行包或日志。

对 Codex / Claude Code，官方 MCP 安装路径（2026-10-21核对）：
```bash
npx @ancher-ai/agent-skills install --print
npx @ancher-ai/agent-skills install --agent claude,codex
```
先根据实际宿主选择 agent，不自动给所有客户端改配置。第一条仅预览；真正安装在用户授权范围内执行。Codex 安装后 `codex mcp login ancher`；Claude Code 在 `/mcp` 里选择 ancher 完成授权。WorkBuddy / 豆包工作的连接器入口按其当前 UI 和官网安装指引配置，不能假造安装参数或 MCP 地址。

如只能用 Ancher CLI，确认它连接的是 Ancher 服务：`ancher whoami`。`ancher chat` 对应 Ancher 的 Agent，不是当前 Agent 自己的生成。CLI 是可选后备，不强制更换用户已配置好的 MCP。

## 导入 → 理解 → 生成

1. 来源为文字或URL时，使用 create_note_from_text(text, comment?)；一份来源对应一条笔记，保存 note_id。已有笔记先复用。上传媒体只用当前 Ancher 工具明确支持的上传/导入能力；没有时引导在网页上传，别假称本地文件已传到服务。
2. 用 get_note(note_id) 检查 queued/processing/ready/error；ready 后读取 get_note_content。默认逐渐退避，比如5/10/20秒，长任务保存状态并向用户更新。不要创建重复笔记“重试”等待。
3. 必要的结构分析也由 ask 完成。把精确 note_id、用户意图和素材结构分析一并交给 ask。保存返回 conversation_id，后续全部改稿沿用同一会话。
4. 若返回 artifact_id，使用 get_artifact_content 读取真实内容；若异步返回运行/会话状态，按实际 schema 查询。没有实际返回脚本文字，不宣称已生成。
5. 展示 Ancher 返回的脚本，不自行润色、删句或改语气。保存收到的原文版本；文件名和版本说明可由宿主整理。

## 失败处理

401：引导重新登录/授权。402或API-BIS002：说明需要在Ancher充值/升级。解析error：读错误，不无限retry；付费重解析先告知成本，在已有授权范围内最多一次，持续失败报告。调用超时先查现有任务/消息，不能立刻重复付费生成。Ancher返回澄清问题时，已有上下文能回答的直接传回；仍关键缺失时把必要问题简化后问用户。

解析与 ask 可能消耗用户 Ancher 额度。首次执行时简短说明，不声称完全免费。
