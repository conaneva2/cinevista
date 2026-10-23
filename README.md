# 幕野 CineVista — personal camera research

个人兴趣驱动的相机软件与离线模拟研究。当前重点是 Sony A7R II / ILCE-7RM2 4.01 的电脑实验环境，以及实时反挤压的可行性验证。本项目与 Sony、DMP 及其他厂商无隶属、认可或支持关系。

**这是开发中的源码备份，不是可用的完整相机模拟器，也不是相机恢复工具。请勿依据此仓库向真实相机安装应用或刷写固件。** 原生窗口、完整 Android 桌面和 APK 安装/启动/重启验证尚未通过；宿主界面和测试通过不能保证真机安全。

## 包含什么

- Java 相机应用研究源码、几何/导出模块和主机测试。
- 本地 Studio 调色原型、相机背面交互原型及离线实验工具。
- [QEMU 源码补丁](emulator/qemu/README.md)：解释器缓冲区、虚拟 NAND 持久化、可选图形控制寄存器模型和命令读取观察器。没有 GPU 指令执行、图像写回或完成中断模型。
- 筛选后的设计文档、来源记录和研究状态。历史文档中的本地运行记录仅为引用，原始日志不公开，旧阶段描述不覆盖当前限制。

**不包含** Sony 固件、解包/反编译结果、驱动或专有库、字体、ROM/RAM/闪存镜像、SDK、APK、签名材料、账号凭据、用户照片、原始设备日志和旧 Git 历史。需要专有输入的实验会因缺输入而停止，不会自动下载或补造它们。这不是对私人研究环境的完整备份。

## 电脑检查

自行准备 JDK 17（或兼容版本）、Python 3.10+ 和 Node.js 后，在仓库根目录运行：

```sh
python3 tools/cv.py check
```

该命令检查主机逻辑、源码边界和文档，不安装相机应用，不代表 APK/硬件认证。需要 SDK 的构建和需要固件的启动实验另有输入要求。GitHub 工作流仅保留手动入口，未自动开启下载、构建或发行。

[当前状态](PROJECT_STATUS.md) · [虚拟相机边界](docs/VIRTUAL_CAMERA.md) · [架构](docs/02_ARCHITECTURE.md) · [公开范围与法律核查](docs/PUBLICATION.md) · [第三方许可](third_party/NOTICE.md)

## 许可、权利与下架

自有应用及工具代码按 [MIT](LICENSE) 发布；第三方保留各自许可。[QEMU 补丁](emulator/qemu/README.md) 分别适用 GPL-2.0-or-later / LGPL-2.1-or-later，不能当成 MIT。个人兴趣、不收费是维护动机，不给 MIT/GPL 附加“仅限非商用”限制。

维护者可随时停止维护或删除自己控制的仓库及内容。若权利人认为某个文件侵犯其权利，请通过本仓库 Issue 提供具体路径、权利依据和联系渠道；请勿公开提交隐私或凭据。收到具体、可信的通知后，将尽快核实，并在必要时先行下架相关内容。

**下架不是免责承诺，也不能召回他人的 fork、克隆、缓存或已经依法取得的许可。** “个人研究”声明不授予对第三方固件、代码、商标、专利或资产的使用权。软件按现状提供，无功能、安全或恢复保证。

This is an independent personal-interest research project, unaffiliated with Sony or DMP. Proprietary firmware and private environment data are not distributed. The emulator is incomplete. Maintainers may remove their hosted materials at any time and will review substantiated rights complaints; removal cannot recall third-party copies or revoke rights already granted under applicable licenses.
