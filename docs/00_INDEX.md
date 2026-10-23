> 最新入口：`15_NATIVE_PERSISTENCE.md`（Film Studio、重启原生颜色）与 `16_NATIVE_COLOR_VALIDATION.md`（验收）；ADR0011替代ADR0010后端优先级。

- [v0.5 实时样张调色主流程](13_REALTIME_GRADING.md)
- [ADR0010 实时软件调色为主工作区](adr/0010-realtime-software-look-primary.md)

# v0.4 新入口

- [Mac与相机安装](10_MAC_CAMERA_RUNBOOK.md)
- [Studio与颜色导出](11_STUDIO_DESIGN.md)
- [本轮来源](12_V04_EVIDENCE_SOURCES.md)
- [下一轮任务](13_NEXT_TASKS_MAC_STUDIO.md)

# 工程文档索引

阅读顺序：状态 → 复用调查 → 架构 → 环境 → 开发流程 → 验证与发布。

| 文件 | 解决的问题 |
|---|---|
| 01_REUSE_AUDIT.md | 每项功能有没有现成代码、成熟到哪一步、采用方式 |
| 02_ARCHITECTURE.md | 当前模块与目标产品架构、依赖方向、协议和生命周期 |
| 03_ENVIRONMENT.md | 现代主机与旧相机运行时隔离、构建与 USB 部署 |
| 04_WORKFLOW.md | PR、并行代理、CI、审查和远端设置 |
| 05_TESTING.md | 测试分层、证据门槛、文件安全与发布条件 |
| 06_COLOR_INTEGRATION.md | Recipe Lab 数据/语义/机型适配与拍摄联动 |
| 07_OPEN_SOURCE.md | MIT、上游更新、许可证和资产台账 |
| 08_SOURCE_LEDGER.md | 本轮核查来源、提交和搜索边界 |
| 09_ROADMAP.md | 可执行任务、出口标准和停手条件 |
| adr/ | 关键取舍、原因及后果 |

本包不创建远端仓库、不设远端保护、不自动安装相机、不产生后台任务。配置文件是供后续启用的本地工程资产。
