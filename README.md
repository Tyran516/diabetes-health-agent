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

准备 Python 3.12+、uv、MySQL 8.0 和 Node.js/npm。以下命令以 PowerShell 为例，初始位置为项目根目录。

### 1. 初始化 MySQL 业务数据库

使用 MySQL 8.0（初始化脚本使用 `utf8mb4_0900_ai_ci` 排序规则）。在项目根目录打开 MySQL 客户端：

```powershell
mysql -h localhost -P 3306 -u root -p
```

在 MySQL 客户端中执行：

```sql
CREATE DATABASE IF NOT EXISTS diabetes CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE diabetes;
SOURCE database/diabetes.sql;
```

如果使用其他数据库名，请相应修改 `CREATE DATABASE`、`USE` 和后端 `DB_NAME`。也可以使用数据库管理工具，将 `database/diabetes.sql` 导入选定的数据库。

脚本包含删除并重建表以及导入示例数据的语句，仅应导入用于本项目的空数据库；重新导入会覆盖对应表中的现有数据。后端 `app/database.py` 设置了 `generate_schemas=False`，应用启动不会自动创建业务表。

### 2. 配置并启动后端

```powershell
cd backend
Copy-Item .env.example .env
```

先编辑 `backend/.env`，替换数据库密码和模型 API 密钥等占位值，再执行：

```powershell
uv sync
uv run uvicorn main:app --reload --port 8000
```

必须在 `backend` 目录执行上述启动命令。`main:app` 指向 `backend/main.py` 中的 FastAPI 实例；路由、数据库及知识库代码位于同级的 `app/` 目录。

| 配置项 | 用途 |
| --- | --- |
| `DB_HOST`、`DB_PORT`、`DB_USER`、`DB_PASSWORD`、`DB_NAME` | MySQL 连接；`DB_NAME` 必须与导入 SQL 的数据库一致 |
| `LLM_MODEL`、`LLM_API_KEY`、`LLM_BASE_URL` | 模型名称、真实 API 密钥及服务地址 |
| `LLM_TEMPERATURE`、`LLM_MAX_TOKENS` | 模型生成参数 |
| `BG_LOW_THRESHOLD`、`BG_HIGH_THRESHOLD` | 血糖风险规则阈值 |
| `CHROMA_PERSIST_DIR`、`CHROMA_COLLECTION_NAME` | 本地向量库目录及集合名称，两项均需填写 |
| `RAG_TOP_K` | 向量检索默认返回数量 |

数据库配置由 `app/config.py` 读取上述 `DB_*` 变量并拼接连接 URL，无需额外设置 `DATABASE_URL`。不要提交填写了真实密钥的 `.env`。

启动成功后访问 [接口文档](http://localhost:8000/docs)。

### 医学知识库初始化

MySQL 保存患者及健康记录，ChromaDB 保存医学知识向量，两者分别初始化：

- `app/core/vector_store.py` 在模块导入时创建本地 ChromaDB 客户端，并加载嵌入模型 `paraphrase-multilingual-MiniLM-L12-v2`。模型未缓存时需要联网下载。
- `main.py` 的启动生命周期调用 `init_knowledge_base()`。当前集合为空时，将 `app/core/knowledge_base.py` 中的内置医学知识写入 ChromaDB；集合已有任意数据时跳过导入。
- `CHROMA_PERSIST_DIR=./data/chroma_db` 相对于启动时的工作目录解析。按本文从 `backend` 启动时，数据保存在 `backend/data/chroma_db/`。
- 此过程不会创建 MySQL 表，也不会自动更新非空集合中的知识内容。

### 3. 启动前端

另开终端，从项目根目录执行：

```powershell
cd frontend
npm install
npm run dev
```

开发服务配置端口为 `3000`，默认访问 [前端页面](http://localhost:3000)，实际地址以终端输出为准。

| 文件 | 作用 |
| --- | --- |
| `frontend/package.json` | `dev`、`build` 和 `preview` 命令 |
| `frontend/vite.config.ts` | Vue 插件、`@` 路径别名、开发端口及 API 代理 |
| `frontend/src/api/index.ts` | Axios 客户端，`baseURL` 为 `/api` |

开发时，Vite 将 `/api` 请求转发至 `http://127.0.0.1:8000`，保留路径前缀，与后端路由的 `/api` 前缀一致。修改后端地址或端口时，请同步修改 `frontend/vite.config.ts` 的 `server.proxy['/api'].target`。当前前端未提供 `.env.example`，也未通过环境变量配置 API 地址。Vite 的开发代理不适用于生产部署，部署时需要为 `/api` 配置相应反向代理。

后端细节见 [backend/README.md](backend/README.md)。

## 设计要点

1. LLM 不直接承担医疗风险判定，异常识别由可解释、可测试的规则完成。
2. RAG 检索结果与患者近期数据共同进入上下文，减少脱离个人情况的泛化回答。
3. ChromaDB 元数据过滤用于缩小检索范围，提高特定类别知识的相关性。
4. 工作流节点职责分离，便于调试、状态持久化和后续扩展工具调用。
5. 所有健康建议均附带非诊疗声明，高风险场景优先提示线下就医。

## 项目定位

该项目用于展示 Agent 工作流编排、RAG 知识检索、结构化业务数据融合以及 FastAPI 全栈落地能力，适合作为 Agent 应用开发方向的学习与求职作品。
