# A7R II 虚拟相机：开发预览 0.1

> 2026-10-23最新：原GPU诊断入口审计确认任务软件signal不能代替硬件IRQ；新公开A6000日志支持同系列SMAPH-S30/IRQ76，但缺逐命令硬件协议。未新增执行模型或启动进展，窗口/Android/APK仍未通过，长期目标进行中。 本轮没有启动新的客体或更改默认操作台；GPU合同未变化时不重复空跑，继续离线追原生存储等独立缺口。见`handoff/runs/20261023T022306Z-sugilite-diagnostics/FINDINGS.md`和`handoff/runs/20261023T022306Z-sugilite-diagnostics/SESSION.md`。


2026-10-23。目标是先在电脑上验证固件和应用，减少后续真机开发风险。当前提供相机背面式操作台和真实 QEMU 启动实验；完整 Android、APK 安装及启动尚未就绪。当前通过的实验不能保证真机不变砖。

## 使用

在项目根目录运行：

```sh
python3 tools/virtual_camera.py --port 8765
```

打开 [本地虚拟相机](http://127.0.0.1:8765/)。右上方启动键创建独立 QEMU 进程及新日志，最长运行 110 秒；再次点击停止。启动页显示实际 Linux、日志驱动和 DMM 结果，原固件异常会显示“固件停在原始错误”。进程正常退出不等于固件通过。

MENU 返回启动页，AEL 打开硬件页，Fn 打开应用页，C3/播放键打开日志。方向键切换页面，Esc 返回启动页。这些按键目前操作宿主控制台；尚未送入原生 Sony 输入服务。背屏内容也不是固件 framebuffer。APK 与录像入口保持不可用。

仅监听本机回环地址，不需要网络账号。工具复用本机既有固件、实验镜像和 QEMU；输入清单在 `config/virtual-camera.lock.json`，缺文件或哈希漂移会拒绝启动。该控制台目前依赖此工作区的私有实验材料，尚不是可分发的一键安装包。停止服务器可按 Ctrl-C，同时会结束它启动的实验进程。无需相机、USB 或 ADB。

## 硬件配置与实际约束

| 项目 | 依据与本版实现 | 尚未覆盖 |
|---|---|---|
| CPU | OpenMemories 资料列 CXD90014 为四个 Cortex-A5；固定 QEMU 板型创建一个 Linux CPU | 其他核心、DSP、图形加速器未完整模拟；CPU 主频未确证，TCI 速度没有真机标定 |
| RAM | 原 4.01 kemco 与板型对应 1 GiB 物理地址空间；恢复原来的三个主要保留区 | 实际探针 MemTotal=201516 kB（约196.8 MiB）；实验 initrd/临时展开文件仍改变使用量 |
| 内存保留 | `0x28000@0x80000000`、`0x15b1000@0x82d90000`、`0x31800000@0x8e800000` | 首区额外保留 64 KiB 保护实验参数；大型实验 initrd 移至 `0x84400000`，与原启动介质不同 |
| 设置空间 | 原 partinf 为 13 MiB；控制台将 `/setting` 的 tmpfs 配额限制到 13 MiB | 尚非原 FAT 持久分区，重启后设置不保留 |
| Android 数据 | 原布局数据分区约 99.75 MiB；逻辑分区末端 438.75 MiB | 本版原生服务实验尚未挂载 Android /data；64 MiB 合成 NAND 只用于既有控制器实验，不代表整机存储 |
| 内置物理闪存 | 拆机资料显示 Micron MCP；完整容量/型号映射尚未可靠闭环 | 不将 MCP 总密度、旁路 DDR3 或逻辑分区末端当成确证的物理 NAND 容量 |
| 屏幕 | 原 WindowServer 实际日志为 640×480、双缓冲；外壳参考官方后背按钮布局 | 原生显示、LCD/EVF 切换、按键输入未接通 |

运算能力不能靠给宿主进程设置一个随意的 CPU 百分比来精确还原。本版先固定指令集、CPU 数和内存布局；待时钟、外设和调度模型有依据后再校准时间。不能用当前 QEMU 的耗时推断 A7R II 反挤压帧率。

公开依据：[OpenMemories 硬件资料](https://openmemories.readthedocs.io/hardware.html)、[原始拆机记录](https://www.ifixit.com/Teardown/Sony+a7R+II+Teardown/45597)、[Micron MCP 产品页](https://www.micron.com/products/obsolete/obsolete-nand-mcp-catalog/part-catalog/part-detail/mt29rz4c8dzzmhan-18w.80d)、[Sony 后背部件说明](https://helpguide.sony.net/ilc/1520/v1/en/contents/TP0001097508.html)。具体数值另与本地 4.01 的 kemco、partinf 和真实运行记录相互校对；内存芯片时钟不当作 CPU 主频。

## 当前突破与下一关

2026-10-23本轮更新：已从首个GPU缓冲追到原程序的逐条构建，确认4组×8字节及128字节缓冲的地址编码/初值。新增独立QEMU取指解包观察器，三次真实提交解析一致；但写回副作用与完成状态产生条件没有闭合，因此未实现执行/IRQ，原窗口和Android仍等GPU。前端4组与控制6组qtest通过。默认网页操作台未切换新构建。证据和复跑：`handoff/runs/20261023T012044Z-sugilite-command/FINDINGS.md`、`SESSION.md`。以下为阶段历史。

2026-10-23最新进度：独立实验模型已使原grm_gles通过上电读回断言并加载。随后原程序真实提交GPU任务，但完成位没有产生，原驱动超时后复位重试；当前停在THREAD_INFRA0的sugilite_ioctl等待。GPU执行/写回/IRQ、原生窗口和Android桌面仍未完成。模型仅覆盖已观察控制字段，上电初值和实际频率/时序待证。旧网页操作台仍运行原固定二进制，未静默切换新模型。详见`handoff/runs/20261023T004916Z-sugilite-model/FINDINGS.md`和`SESSION.md`；下面记录此前字体/内存依赖修复过程。

已从官方 4.01 `nflasha5` 的暖启动内存快照恢复 3372 字节 `ulogio.bin`，并找到匹配 FAT 目录项。原版 `osal_ulogio.ko`、DMM 成功初始化；恢复原版 `stream.ko` 与设备节点后，实际断点确认 `gl_common` 创建返回 0，并正常通过原断言。

最新分组实验已恢复原 `/dev/uinput`，成功注册 D keyboard；按原 Backup 指向恢复字体资源后，TextRM 返回0并正常通过原断言。Appframework 继续到图形帧缓冲创建失败，具体停在 GraphicsContext3DShaderMusashi.cpp:292 的窗口表面创建。sugilite 实际节点是 `/dev/dmpgles2`，原 grm_gles 驱动又在上电读回检查处触发 sugi_hw.c:221；当前 QEMU 缺对应图形寄存器设备，不能只补节点解决。下一步需有依据地补图形硬件模型，保留原断言和失败对照。

本页操作台仍锁定上一轮实验；本轮字体/图形分组探针按新 SESSION 命令单独运行，尚未合入默认启动按钮。原生按键、像素显示和 APK 入口仍未就绪。

完整第一版仍须通过：原生窗口和输入 → Android/system_server/启动器 → 持久 `/data` → 原事故 APK 的受控安装/启动/中断/重启对照。即使都通过，也只覆盖已建模的条件，不能自动解除 `.local/CAMERA_WRITE_HOLD`。

最新记录：`handoff/runs/20261023T002402Z-sugilite-window/FINDINGS.md`；续接：`handoff/runs/20261023T002402Z-sugilite-window/SESSION.md`。上一轮操作台与日志恢复记录仍保留。停止本地服务器即可退出，原始固件和生产 APK 未改。
