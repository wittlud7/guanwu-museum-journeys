# DeepSeek 随行伴游

Web 和 `mini.html` 小程序尺寸预览共用服务端 `/api/guide`。模型真实调用 DeepSeek，通过 `search_catalog`、`get_item`、`plan_visit`、`propose_journey` 查询已收录资料、分配参观时间和提出行程建议。新增 `plan_city_visit` 提供半天一馆/一天两馆及自定义三馆组合（可分多天），`compare_items` 对照两件文物的有来源资料。加入行程需游客点击确认。资料来源随答案显示，不提供虚构展厅定位、实时展出或预约承诺。用户的观察仅在主动点击“请伴游”后随问题发送，不会自动上传手记。

本次已用用户提供的配置完成真实调用：资料讲解及来源、亲子讲解、行程提议与确认均通过。使用 `deepseek-v4-flash`，可用服务端 `DEEPSEEK_MODEL` 调整。API 协议参考 [DeepSeek 官方文档](https://api-docs.deepseek.com/zh-cn/guides/tool_calls/)。

本机启动：`node scripts/preview.mjs`，访问 http://localhost:4173/mini.html 。服务端优先读环境变量 `DEEPSEEK_API_KEY`，也可读取 Git 忽略的根目录 `settings.json` 中 DeepSeek 配置。密钥不进入前端、原生小程序或部署资源。部署密钥单独保存在 Sites Secret；修改后需部署以生效。

生产端使用 `server-app/` 的 Vinext / Cloudflare Worker，原有 `dist/` 继续作为静态内容源，由 Vite `publicDir` 复制到 `server-app/dist/client`。不要把整个工作目录或 settings.json 打包发布。

构建顺序：

1. `python scripts/sync_server.py`
2. 在 `server-app` 中运行 `npm run build`
3. 发布 `server-app/dist/`，沿用根目录 `.openai/hosting.json` 中的 Site ID。

微信原生工程包含 11 城 80 馆内容和按城市浏览，但尚未接入微信登录与专用 AI 网关。原生线上 AI 需微信身份校验、额度管理及合法 HTTPS 域名配置，不能把服务端模型密钥放进原生客户端。跨馆对看、观物卡导出与真实 AI 在浏览器小程序预览中体验。

会员仍是免费试用演示，不扣款。本轮读取到站点现状为公开访问，更新保留该分享设置。Worker 对每个可识别访客在单实例内限制每分钟10次提问，且单次有工具轮数、消息长度与超时上限；单实例限制不是全局计费额度，正式商业使用需服务端账户与持久额度控制。正式付费前需接入账户和支付订单校验。

社区 `/api/community/` 独立使用D1持久存储，身份仅信任平台认证头。公开帖子不进入AI事实资料库。路线分享仅包含公开馆序与交通偏好，不发送私人日期/时刻。单实例写入限流不等同于正式运营的全局风控。

2026-10-26：AI目录新增46项中国世界文化/混合遗产。search_catalog 支持省份与遗产名，get_item 返回正式名录、看点和来源；遗产地不混作博物馆加入原有馆间行程。语音包是预生成的合成录音，与 DeepSeek 文字问答分开；不把模型回答自动送往语音服务。
