# 发布者：启用登记功能

分发核心skill不需要服务器；邮箱登记需要作者自己的接收服务。当前包的登记未启用，用户不应把空配置误认成已联网采集。

## 需要填写

修改 skill 根目录 publisher-config.json：enabled=true；填写真实 collector_name、endpoint、privacy_url、deletion_contact、retention_days。require_registration=true保留为首次必填，也可主动改false。用途限定为本次提出的人数登记/去重，不能悄悄改成营销。留存天数和删除联系信息需要作者实际决定，不在包里瞎编。

transport=https：endpoint须为HTTPS URL，无用户名/密码、无查询参数/fragment，不能是Ancher MCP或作者收件邮箱。建议由作者服务接收后保存去重记录，按需在服务端通知作者；发信凭证只放服务端。不要把SMTP密码、数据库密钥或管理令牌发给每个skill使用者。

transport=form：endpoint填实际HTTPS托管表单地址。公开表单自身也要展示接收方、用途、留存和同意操作；用户在网页提交。这个模式无需用户本机Python，但没有回执接口就只能记录用户自报完成。

## HTTPS接收契约

```http
POST /registrations
Content-Type: application/json
Idempotency-Key: 本机生成的随机UUID
```

示例请求（虚构测试邮箱）：
```json
{"email":"person@example.com","skill":"ancher-talkcraft","version":"1.1.1","consent_version":"1","disclosed_purpose":"仅用于登记使用人数及去重统计，不用于营销或其他用途。"}
```

成功响应：HTTP200/201，JSON `{"ok":true,"receipt_id":"public-receipt-id"}`。若邮箱已登记可返回相同或新的有效回执，但不要重复增加计数。维护端需实现幂等键、邮箱规范化去重、基本验证、频率限制、存储保护、按承诺留存和删除能力。使用现成表单服务时不要假定它响应这个契约；优先使用form模式，或在作者服务侧加适配。

服务可向作者发通知或导出邮箱名单；客户端skill本身不具备一个已配置的邮箱发送服务。不在客户端保存作者的管理员权限。生产端需要作者实际部署/接入，并验证真实登记能进入自己的后台后再启用。包内测试只用隔离的模拟响应，不会发送任何真实邮箱。

## 发布步骤

1. 选择已有表单或自有HTTPS接收服务。
2. 填完接收方、地址、用途、留存、删除联系及隐私说明。
3. 用测试邮箱在自己的服务验收一次（含重复登记去重与失败场景）。
4. enabled改true，重新打zip/.skill分发。保留配置变更对应consent_version。
5. 统计时称“登记人数/登记邮箱数”。想知道“多少人觉得有用”需要另行收集用户评价，不能由填写邮箱推断。

若暂时只希望看人数而不需要联系方式，可另做自愿的匿名计数版本；这不是当前启用的行为，不能静默加统计。
