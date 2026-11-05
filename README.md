# DeepSeek API 全栈课程（2026）

本项目依据 DeepSeek 中文官方 API 文档（2026-11-05 抓取核对）编写，采用“概念 → 协议 → SDK → 工程实践 → Agent 集成”的递进路线。课件使用 LaTeX Beamer，所有 Python 例程均不超过 200 行、5000 字符，每课不超过 3 个 Python 文件。

## 课程地图

| 课次 | 主题 | 学完能够 |
|---|---|---|
| 第1课 | 平台、模型、鉴权与首次调用 | 配置环境，完成 HTTP/SDK 调用，查询模型与余额 |
| 第2课 | Chat Completions 基础 | 正确组织消息、参数、响应与多轮上下文 |
| 第3课 | 流式输出、用量与缓存 | 解析 SSE，读取 usage 与缓存命中指标 |
| 第4课 | 思考模式 | 控制推理强度，处理 reasoning_content |
| 第5课 | 结构化与补全 | 使用 JSON Output、前缀续写、FIM |
| 第6课 | Tool Calls | 实现工具闭环、strict Schema 与思考工具链 |
| 第7课 | 图像理解 | 使用 URL、Base64 与 detail 传图 |
| 第8课 | Files API | 管理文件生命周期并复用图片 |
| 第9课 | Search / Fetch | 搜索、抓取并构建有来源的 Web RAG |
| 第10课 | Responses API | 使用 items、语义事件与工具调用 |
| 第11课 | Anthropic Messages API | 迁移 Anthropic SDK 与 Claude 工具协议 |
| 第12课 | 生产可靠性 | 重试、限流、隔离、成本与可观测性 |
| 第13课 | Agent 集成与综合项目 | 接入主流 Agent，完成搜索型研究助手 |

## 官方文档覆盖矩阵

核对日期：2026-11-05。覆盖范围为 DeepSeek 中文站点地图中的“快速开始、API 指南、API 文档、Agent 接入”。新闻和历史更新作为版本背景在第1课、第13课说明，不逐条复述已下线模型。

这张矩阵用于把官方文档能力对应到课程、课件和例程，方便检查是否存在遗漏；它不是运行例程所需的配置文件。

| 官方页面或能力 | 对应课程 | 覆盖内容 |
|---|---|---|
| 首次调用、模型与价格 | 第1课 | base URL、Key、模型选择、能力、价格快照 |
| Token 用量、模型列表、余额 | 第1、3、12课 | 估算与 usage、`GET /models`、`GET /user/balance` |
| Chat Completions API | 第2–7课 | 当前请求参数、消息/响应结构、流式、logprobs、视觉、工具 |
| 多轮对话 | 第2课 | 无状态上下文拼接、历史裁剪 |
| KV Cache | 第3、12课 | 命中规则、指标、成本设计 |
| 思考模式 | 第4、6课 | 开关、effort 映射、reasoning_content、工具调用 |
| JSON Output | 第5课 | response_format、提示约束、截断与空内容兜底 |
| 对话前缀续写 Beta | 第5课 | `/beta`、assistant prefix、stop |
| FIM Completion API Beta | 第5课 | `/completions`、prompt/suffix、4K 限制 |
| Tool Calls | 第6课 | tool_choice、循环、并行调用、strict JSON Schema |
| 图像理解 | 第7课 | URL、Base64、file、detail、Token 与限制 |
| Files API 全端点 | 第8课 | 上传、列表、查询、删除、过期、分页、配额 |
| Search / Fetch API | 第9课 | 两端点、搜索语法、响应、错误、计费、QPS |
| Responses API | 第10课 | 请求/响应 items、流式事件、工具、视觉、兼容差异 |
| Anthropic Messages API | 第11课 | Headers、字段映射、消息、工具、视觉、流式与用量 |
| 错误码、限速与隔离 | 第12课 | 400/401/402/422/429/5xx、重试、user_id、保活 |
| Agent integrations | 第13课 | Harness、Claude Code、Codex、OpenCode、OpenClaw、Hermes、Reasonix、WorkBuddy/CodeBuddy、Qoder |
| 更新日志 | 第1、13课 | 当前模型别名、迁移原则、上线前复核 |

### API 端点清单

| 方法与路径 | 对应课程 |
|---|---|
| `POST /chat/completions` | 第2–7课 |
| `POST /beta/completions` | 第5课 |
| `POST /responses` | 第10课 |
| `POST /anthropic/v1/messages` | 第11课 |
| `POST/GET /files`、`GET/DELETE /files/{id}` | 第8课 |
| `POST /v1/tools/search`、`POST /v1/tools/fetch` | 第9课 |
| `GET /models`、`GET /user/balance` | 第1课 |

### 时效说明

模型名、上下文长度、价格、并发与兼容字段均可能更新。例程避免硬编码价格；课件中的数值用于理解规则，生产配置应以运行时 `/models` 与官方价格页为准。

## 目录约定

```text
第N课/
├── 课件/
│   ├── main.tex
│   └── main.pdf
├── 素材/（需要视觉输入的课程可选）
└── 例程/
    ├── 01_xxx.py
    └── ...（最多 3 个）
```

根目录的 `beamer-common.tex` 是所有课件的公共主题；官方页面与课程的对应关系已合并到本 README 的“官方文档覆盖矩阵”。

第7课已提供 `素材/README.md`，默认视觉例程会读取 `素材/示例图.png`；请按说明放入自制图片，避免提交带版权或隐私风险的素材。

## 环境准备

1. 安装 Python 3.10+，执行 `python -m pip install -r requirements.txt`。
2. 在 PowerShell 设置当前会话的 Key：`$env:DEEPSEEK_API_KEY="sk-..."`。
3. 进入某课的 `例程` 目录运行脚本，例如：`python 01_first_call.py`。
4. 安装 TeX Live/MiKTeX（含 XeLaTeX、ctex、beamer、listings），进入某课 `课件` 目录执行两次 `xelatex main.tex`。

联网例程会产生真实费用。默认模型可用 `DEEPSEEK_MODEL` 覆盖；默认基础地址为 `https://api.deepseek.com`。

## 学习建议

- 第1–4课是必修基础，第5–11课按应用场景选学，第12–13课面向上线与综合实战。
- 首次运行先把 `max_tokens` 调小；流式程序以正常终止事件为准，不把 keep-alive 当正文。
- 价格、模型能力与限额会变化；课件给出的是核对日快照，上线前应重新查看官方文档。

## 官方来源

- 中文文档主页：https://api-docs.deepseek.com/zh-cn/
- API 参考：https://api-docs.deepseek.com/zh-cn/api/create-chat-completion
- 更新日志：https://api-docs.deepseek.com/zh-cn/updates
