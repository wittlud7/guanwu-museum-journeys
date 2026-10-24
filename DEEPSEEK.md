# DeepSeek 随行伴游

Web 和 `mini.html` 小程序尺寸预览共用服务端 `/api/guide`。模型真实调用 DeepSeek，通过 `search_catalog`、`get_item`、`plan_visit`、`propose_journey` 查询已收录资料、分配参观时间和提出行程建议。加入行程需游客点击确认。资料来源随答案显示，不提供虚构展厅定位、实时展出或预约承诺。

本次已用用户提供的配置完成真实调用：资料讲解及来源、亲子讲解、行程提议与确认均通过。使用 `deepseek-v4-flash`，可用服务端 `DEEPSEEK_MODEL` 调整。API 协议参考 [DeepSeek 官方文档](https://api-docs.deepseek.com/zh-cn/guides/tool_calls/)。

本机启动：`node scripts/preview.mjs`，访问 http://localhost:4173/mini.html 。服务端优先读环境变量 `DEEPSEEK_API_KEY`，也可读取 Git 忽略的根目录 `settings.json` 中 DeepSeek 配置。密钥不进入前端、原生小程序或部署资源。部署密钥单独保存在 Sites Secret；修改后需部署以生效。

生产端使用 `server-app/` 的 Vinext / Cloudflare Worker，原有 `dist/` 继续作为静态内容源，由 Vite `publicDir` 复制到 `server-app/dist/client`。不要把整个工作目录或 settings.json 打包发布。

构建顺序：

1. `python scripts/sync_server.py`
2. 在 `server-app` 中运行 `npm run build`
3. 发布 `server-app/dist/`，沿用根目录 `.openai/hosting.json` 中的 Site ID。

微信原生工程包含 11 城内容，但尚未接入微信登录与专用 AI 网关。当前私有 Site 的登录凭据不能直接用于 `wx.request`；原生线上 AI 需自有 HTTPS 网关、微信身份校验及合法域名配置。浏览器小程序预览中的 AI 已可真实使用。

会员仍是免费试用演示，不扣款。现有私有访问范围保持不变。正式开放付费前需接入账户、额度与支付订单校验。
