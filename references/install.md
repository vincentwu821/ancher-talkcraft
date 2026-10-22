# 安装、分发与能力检查

这是标准 Agent Skills 目录：SKILL.md + references/ + scripts/ + assets/。包不内置Ancher登录信息、作者邮箱、私有媒体或项目绝对路径。格式可移植不等于每个客户端都有同样的MCP、原生弹窗、ASR、图像和视频执行能力。

核对日期：2026-10-21。下面是官网说明支持的加载方法，不代表在四个客户端逐个完成了实机端到端视频测试。

## Codex

把整个 ancher-talkcraft 文件夹放在用户 `~/.agents/skills/` 或项目 `.agents/skills/` 下。不要只复制SKILL.md，保留旁边的资源。开启新会话后用 `$ancher-talkcraft` 或自然语言触发。若当前版本提供设置中的导入入口，也可按其UI安装。

官方说明：https://learn.chatgpt.com/docs/build-skills

## Claude / Claude Code

Claude Code 优先在对话内通过插件源安装，无需手动访问 GitHub 下载：

```text
/plugin marketplace add vincentwu821/ancher-talkcraft
/plugin install ancher-talkcraft@ancher
```

在插件面板选择安装范围；也可在添加 Ancher 源后进入 `/plugin` → Discover 搜索 `ancher-talkcraft`。安装后用自然语言调用 Ancher TalkCraft，或使用插件技能命令 `/ancher-talkcraft:ancher-talkcraft`。这是作者维护的 Ancher 插件源，不代表已通过 Anthropic 官方目录审核。

独立 Skill 是另一种安装方式：整个文件夹放在 `~/.claude/skills/` 或项目 `.claude/skills/` 下，用 `/ancher-talkcraft` 调用。插件和独立 Skill 选择一种安装方式，避免重复加载。Claude客户端若支持自定义Skills上传，按其Skills页面导入ZIP；普通聊天的文件附件不是安装认证。云端会话的文件/工具能力与本机终端不同，先检查实际执行环境。

官方说明：https://code.claude.com/docs/en/skills

## WorkBuddy

在“专家·技能·连接器”进入技能，选择“添加技能 → 上传技能”，上传发行包 ZIP，保留 `.zip` 扩展名，不改为 `.skill`。ZIP 解压后应是 `ancher-talkcraft/SKILL.md`，旁边保留 references、scripts、assets 等资源；不要只上传 SKILL.md，也不要额外套一层目录。上传 ZIP 时由客户端解包；若当前界面提供文件夹导入，则选择解压后的完整 ancher-talkcraft 文件夹。在“已安装”中确认启用。本地导入不等于公开上架技能市场。

官方说明：https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market

## 豆包工作

适用的是具备“插件·技能·伙伴”和自定义技能导入的**豆包工作**。进入“技能 → +添加 → 上传技能”，上传文件/文件夹。官方文档将入口写作小写skill.md，所以发行时附doubao版ZIP，将同一入口文件命名为skill.md；其余内容保持一致。不要把这个适配副本反过来用于要求大写SKILL.md的标准Agent。

普通豆包聊天若只有附件/文本对话，可读流程但不能保证调用Ancher或渲染视频；不要宣称已完整安装或能自动完成全流程。先检查是否有MCP/插件接入Ancher及必要媒体执行能力。

官方说明：https://www.doubao.com/work/docs/zh-cn/articles/081010973544-skills

## 第一次运行

只检查当前分支需要的能力，不统一要求所有工具：

| 当前任务 | 必要能力 |
| --- | --- |
| 参考内容→脚本 | Ancher MCP/实际Ancher Agent，授权网络访问；缺失时先引导接入 |
| 已拍素材→视频 | 读写媒体、实际剪辑/渲染、ASR与字级时间对齐、可看图和预览/试听；可调用本机或宿主等价工具 |
| 封面 | 视频帧提取、图像/排版工具，保持人物可识别 |
| 首次邮箱登记 | 已配置作者HTTPS接口+Python/HTTP能力，或托管表单+浏览器；明确同意 |

本机可用 `python3 scripts/check_environment.py` 只读检查常见CLI。命令存在不代表已认证、满足完整渲染或已准备好字级字幕。

## 分发

标准包包含一个完整 ancher-talkcraft/ 文件夹。邮箱统计配置默认未启用；作者启用前应按publisher-setup.md填真实服务并测试，不能发带空接收方的必填提示。不要把自己的Ancher token、邮箱发送凭据、已登记用户状态、素材或生成项目放进包。

Agent Skills标准：https://agentskills.io/specification
Ancher官方接入：https://github.com/streamify-one/ancher-agent-skills
