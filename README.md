# 糖尿病智慧健康管理辅助 Agent

一个面向糖尿病日常健康管理场景的全栈 Agent 项目。系统结合患者档案、近 7 天血糖记录、医学知识库检索与确定性风险规则，生成可追溯的个性化健康提示。

> 本项目仅用于学习、健康科普与日常管理辅助，不构成医疗诊断或治疗建议。出现异常症状或高风险指标时，请及时咨询专业医务人员。

## 核心功能

- **LangGraph 工作流**：通过意图分类、患者上下文加载、医学知识检索、建议生成和风险评估等节点组织业务流程。
- **个性化上下文**：融合患者基本档案、血糖记录、饮食、用药和运动数据。
- **血糖趋势分析**：计算均值、波动程度、达标率与近期变化趋势。
- **医学知识 RAG**：使用 Hugging Face Embedding 与 ChromaDB 构建向量知识库，并通过 Metadata Filter 按糖尿病、饮食、用药等类别检索。
- **规则与模型协同**：由确定性规则完成高低血糖识别和风险分级，由大模型负责解释与自然语言表达。
- **业务数据管理**：提供患者、血糖、饮食、用药、运动及健康报告等模块。
- **前后端分离**：FastAPI 提供 REST API，Vue 3 提供交互页面和数据可视化。

## 系统流程

```mermaid
flowchart LR
    U[用户问题] --> I[意图分类]
    I --> C[加载患者档案与近 7 天数据]
    C --> R[医学知识检索]
    R --> G[LLM 生成个性化建议]
    G --> A[确定性风险评估]
    A --> O[健康提示与就医提醒]
```

## 技术栈

### 后端与 Agent

- Python、FastAPI、Pydantic
- LangChain、LangGraph
- Hugging Face Embedding、ChromaDB
- MySQL、Tortoise ORM
- REST API、SSE

### 前端

- Vue 3、TypeScript
- Pinia、Element Plus
- ECharts

## 项目结构

```text
diabetes-health-agent/
├─ backend/          # FastAPI、Agent 工作流、RAG 与业务接口
├─ frontend/         # Vue 3 前端
├─ database/
│  └─ diabetes.sql   # 数据库初始化脚本
└─ README.md
```

## 本地运行

### 1. 初始化数据库

创建 MySQL 数据库，并按需导入：

```text
database/diabetes.sql
```

### 2. 启动后端

推荐使用 Python 3.12+ 与 uv。

```powershell
cd backend
Copy-Item .env.example .env
uv sync
uv run uvicorn main:app --reload --port 8000
```

启动前请在 `.env` 中配置数据库连接、模型服务和向量库等参数。不要提交真实密钥。

### 3. 启动前端

```powershell
cd frontend
npm install
npm run dev
```

具体环境变量名及启动差异请同时参考 `backend/README.md` 和前端配置。

## 设计要点

1. LLM 不直接承担医疗风险判定，异常识别由可解释、可测试的规则完成。
2. RAG 检索结果与患者近期数据共同进入上下文，减少脱离个人情况的泛化回答。
3. ChromaDB 元数据过滤用于缩小检索范围，提高特定类别知识的相关性。
4. 工作流节点职责分离，便于调试、状态持久化和后续扩展工具调用。
5. 所有健康建议均附带非诊疗声明，高风险场景优先提示线下就医。

## 项目定位

该项目用于展示 Agent 工作流编排、RAG 知识检索、结构化业务数据融合以及 FastAPI 全栈落地能力，适合作为 Agent 应用开发方向的学习与求职作品。
