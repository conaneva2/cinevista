# 文档目录

当前事实优先读取[项目状态](../PROJECT_STATUS.md)；历史交接及旧版说明保留用于追溯，不能覆盖当前实测结论。

新接手请先读[研究与开发手册](research/README.md)：总览、时间线、技术链路、证据资料和接续指南。

| 文档 | 用途 |
|---|---|
| [使用说明书](USER_GUIDE.md) | Studio操作、APK范围、故障处理 |
| [相机界面与预览](CAMERA_UI_PREVIEW.md) | XML结构预览与原生验证路线 |
| [TODO](../TODO.md) | 从任务板自动生成的执行入口 |
| [文档制度](DOCUMENTATION.md) | 文档归属、同步规则、检查与归档 |
| [架构](02_ARCHITECTURE.md) | 模块、依赖、接口和演进边界 |
| [虚拟相机开发预览](VIRTUAL_CAMERA.md) | 后背操作台、实际固件启动和硬件约束边界 |
| [离线安装启动实验](INSTALL_BOOT_LAB.md) | 固件方法回放、故障注入与完整模拟边界 |
| [相机连接与固件](CAMERA_CONNECTION.md) | 官方固件留存、MTP环境与操作步骤 |
| [工具链](03_ENVIRONMENT.md) | Mac构建、依赖、精确来源 |
| [协作流程](04_WORKFLOW.md) | 任务、分支、评审、合并、发行 |
| [测试规范](05_TESTING.md) | 主机/SDK/机测层次与证据 |
| [Gitee接入](GITEE.md) | 私有仓库、远端权限及CI状态 |
| [源码复用](01_REUSE_AUDIT.md) | 候选组件与许可边界 |
| [原生持久化](15_NATIVE_PERSISTENCE.md) | 产品主要求与研发范围 |
| [原生验收](16_NATIVE_COLOR_VALIDATION.md) | 退出、重启、恢复和预览验证 |
| [相机操作卡](../handoff/DEVICE_TEST_CARD.md) | 当前可执行的集中机测步骤 |
| [参与开发](../CONTRIBUTING.md) | 贡献、验证与评审要求 |

架构决策记录放在`docs/adr/`。制度、事实、历史记录分开维护，完整清单见[文档注册表](../config/documentation.json)。

- [ADR0014：机内实时反挤压可行性优先](adr/0014-desqueeze-feasibility-gate.md)

- [ADR0015：安装启动离线方法环境](adr/0015-offline-install-method-lab.md)

- [ADR0016：先建立虚拟相机环境](adr/0016-virtual-camera-first.md)
