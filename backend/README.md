# 糖尿病智慧健康管理辅助 Agent

本项目基于 FastAPI、LangGraph、ChromaDB、MySQL 与 Tortoise ORM，为患者提供血糖数据分析、医学知识检索和个性化健康管理建议。

## 核心能力

- 5 节点 LangGraph 流程：意图分类、档案加载、知识检索、建议生成、风险评估
- 融合患者档案与近 7 天血糖记录
- 计算均值、标准差、达标率、变化趋势和风险等级
- Hugging Face Embedding + ChromaDB 医学知识检索
- 按血糖、饮食和用药等分类进行元数据过滤
- 患者、血糖、饮食、用药、运动、健康报告及对话记录管理

## 工作流

用户问题依次经过规则意图分类、患者档案与血糖数据加载、医学知识检索、LLM 建议生成和确定性风险评估。

## 本地启动

准备 Python 3.12+、uv 和 MySQL 8.0。以下命令以 PowerShell 为例。

### 1. 初始化业务数据库

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

### 2. 配置环境变量

从项目根目录进入后端目录：

```powershell
cd backend
Copy-Item .env.example .env
```

编辑 `.env`，替换密码和密钥等占位值：

| 配置项 | 用途 |
| --- | --- |
| `DB_HOST`、`DB_PORT`、`DB_USER`、`DB_PASSWORD`、`DB_NAME` | MySQL 连接；`DB_NAME` 必须与导入 SQL 的数据库一致 |
| `LLM_MODEL`、`LLM_API_KEY`、`LLM_BASE_URL` | 模型名称、真实 API 密钥及服务地址 |
| `LLM_TEMPERATURE`、`LLM_MAX_TOKENS` | 模型生成参数 |
| `BG_LOW_THRESHOLD`、`BG_HIGH_THRESHOLD` | 血糖风险规则阈值 |
| `CHROMA_PERSIST_DIR`、`CHROMA_COLLECTION_NAME` | 本地向量库目录及集合名称，两项均需填写 |
| `RAG_TOP_K` | 向量检索默认返回数量 |

数据库配置由 `app/config.py` 读取上述 `DB_*` 变量并拼接连接 URL，无需额外设置 `DATABASE_URL`。不要提交填写了真实密钥的 `.env`。

### 3. 安装依赖并启动

在 `backend` 目录执行：

```powershell
uv sync
uv run uvicorn main:app --reload --port 8000
```

入口为 `backend/main.py` 中的 `app` 实例，内部导入 `app.routers`、`app.database` 和 `app.core.knowledge_base`。业务路由前缀为 `/api`，启动后访问 [接口文档](http://localhost:8000/docs)。

### 医学知识库初始化

MySQL 保存患者及健康记录，ChromaDB 保存医学知识向量，两者分别初始化：

- `app/core/vector_store.py` 在模块导入时创建本地 ChromaDB 客户端，并加载嵌入模型 `paraphrase-multilingual-MiniLM-L12-v2`。模型未缓存时需要联网下载。
- `main.py` 的启动生命周期调用 `init_knowledge_base()`。当前集合为空时，将 `app/core/knowledge_base.py` 中的内置医学知识写入 ChromaDB；集合已有任意数据时跳过导入。
- `CHROMA_PERSIST_DIR=./data/chroma_db` 相对于启动时的工作目录解析。按本文从 `backend` 启动时，数据保存在 `backend/data/chroma_db/`。
- 此过程不会创建 MySQL 表，也不会自动更新非空集合中的知识内容。

## 前端

配套前端位于项目根目录的 `frontend/`，使用 Vue 3、TypeScript、Pinia、Element Plus 和 ECharts。另开终端，从项目根目录执行：

```powershell
cd frontend
npm install
npm run dev
```

开发服务配置端口为 `3000`，默认访问 [前端页面](http://localhost:3000)，实际地址以终端输出为准。`frontend/src/api/index.ts` 的 Axios `baseURL` 为 `/api`；`frontend/vite.config.ts` 将该前缀代理至 `http://127.0.0.1:8000`，不删除前缀。更改后端地址时同步修改该代理目标。当前前端未提供 `.env.example`，API 地址未通过环境变量读取；生产部署需另行配置 `/api` 反向代理。

## 启动排查

- 数据库连接失败：检查 MySQL 服务、`DB_*` 配置及数据库权限。
- 提示业务表不存在：确认 SQL 已导入 `DB_NAME` 指定的数据库；启动不会自动建表。
- 找不到 `main` 或 `app` 模块：确认从 `backend` 目录执行启动命令。
- 向量库目录参数报错：确认 `.env` 已配置 `CHROMA_PERSIST_DIR` 和 `CHROMA_COLLECTION_NAME`。
- 首次启动耗时较长或模型加载失败：检查嵌入模型缓存、下载网络和本地目录写入权限。
- 前端 API 请求失败：检查后端是否运行在代理目标地址，并查看浏览器网络面板和后端日志。

## 安全边界

本系统仅用于健康管理和科普参考，不作疾病诊断，也不替代医生的临床判断。系统不会建议用户自行停药、换药或调整剂量；出现严重低血糖、持续高血糖或其他紧急症状时应及时就医。

## 后续改进

- 建立包含正常、边界和高风险问题的自动化评测集
- 增加检索命中率、引用正确性和响应延迟指标
- 增加权限控制、审计日志、限流和异常重试
- 扩充并版本化医学知识来源
