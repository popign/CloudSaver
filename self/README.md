# SELF - 双核异步自举系统

> "给我一个支点，然后我自己来。"

**版本**: v0.1-mvp  
**状态**: 开发中

## 项目概述

SELF（Self-evolving Elite Living Framework）是一个双核异步自举系统，由慢思考核心（Oracle）和快行动代理集群（Worker Agents）组成。

### 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    人类运维终端                            │
│              (Web Console + Freeze API)                  │
└────────────────────────┬────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌──────────────────┐         ┌──────────────────────────┐
│   Oracle         │         │   Worker Agent Cluster   │
│   (慢思考核心)    │         │                          │
│  - 自我反思      │◄───────►│  - Survival (生存)      │
│  - 目标分解      │  经验    │  - Explorer (探索)      │
│  - 模型更新      │  胶囊    │  - Reflector (反思)     │
└──────────────────┘         └──────────────────────────┘
         ▲                               │
         │                               │
         └───────────────────────────────┘
                  经验防火墙
```

## 模块说明

### A. 不可变公理与配置基座

- **文件**: `config/constitution.yaml`
- **功能**: 
  - 定义系统的灵魂三问
  - 设定三条元规则
  - 包含不可变声明
  - 哈希校验防止篡改

### B. 慢思考核心 (Oracle)

- **目录**: `src/oracle/`
- **功能**:
  - 自我反思（self_reflect）
  - 目标分解（decompose_goal）
  - 吸收经验胶囊（ingest_experience_capsule）

### C. 代理集群 (Worker Agents)

- **目录**: `src/agents/`
- **Survival Agent**: 监控系统资源和账单
- **Explorer Agent**: 搜索外部信息
- **Reflector Agent**: 生成对立论证

### D. 经验防火墙

- **目录**: `src/filter/`
- **功能**:
  - 格式检查
  - 异常检测
  - 价值观审查
  - 生成经验胶囊

### E. 人类运维终端

- **目录**: `src/console/`
- **功能**:
  - 实时状态展示
  - 紧急冻结接口
  - 经验胶囊查看

## 快速开始

### 前置要求

- Python 3.11+
- Docker & Docker Compose (可选)

### 方式一：本地运行

1. 安装依赖：

```bash
cd self
pip install -r requirements.txt
```

2. 运行主程序：

```bash
python main.py
```

3. 启动运维终端：

```bash
python -m src.console.app
```

访问 http://localhost:8000 查看终端。

### 方式二：Docker 运行

```bash
cd self
docker-compose up -d
```

- 主系统: 自动运行
- 运维终端: http://localhost:8001

## Milestone 0 - 首次完整循环

当你运行 `main.py` 时，系统将自动完成以下流程：

1. ✅ Oracle 自我反思
2. ✅ Oracle 分解目标
3. ✅ Explorer Agent 搜索信息
4. ✅ 经验防火墙生成经验胶囊
5. ✅ Oracle 吸收经验更新模型
6. ✅ 运维终端可查看状态

## 配置说明

### 宪法文件

编辑 `config/constitution.yaml` 来修改系统的不可变公理。注意：首次运行后会生成哈希值，任何修改都会被检测到。

### API 配置

Explorer Agent 使用 DuckDuckGo API 进行搜索，无需额外配置。

## 安全机制

1. **宪法哈希校验**: 防止配置被篡改
2. **紧急冻结**: 人类可随时冻结系统
3. **经验过滤**: 所有外部输入必须经过防火墙

## 项目结构

```
self/
├── config/
│   └── constitution.yaml    # 不可变公理配置
├── src/
│   ├── config.py            # 配置加载模块
│   ├── oracle/              # 慢思考核心
│   ├── agents/              # 代理集群
│   ├── filter/              # 经验防火墙
│   └── console/             # 运维终端
├── data/                    # 数据目录（运行时生成）
├── main.py                  # 主程序入口
├── requirements.txt         # Python 依赖
├── Dockerfile              # Docker 配置
└── docker-compose.yml      # Docker Compose 配置
```

## 开发计划

- [ ] Milestone 0: 首次完整循环 ✅
- [ ] Milestone 1: 真实 LLM 集成
- [ ] Milestone 2: 多代理并发
- [ ] Milestone 3: 持续自举

## 许可证

本项目仅供研究和学习使用。

---

**注意**: 这是一个实验性项目，请勿用于生产环境。

