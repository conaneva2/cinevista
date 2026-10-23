> 当前专题汇总：[研究手册](research/README.md)。下文保留阶段实验记录，较早停点以手册及项目状态的后续证据修订为准。

# 安装、启动兼容实验环境

> 2026-10-22最新进展：QEMU NAND控制器级跨进程持久性通过；原版Android已运行到Sony窗口服务/JNI消息等待。Linux文件系统及/data持久性、完整桌面和APK安装仍未通过，见末尾最新阶段。

2026-10-22：第一阶段已在本机运行。它是**按固件关键方法执行的离线回放环境**，不是完整 A7R II / Android 模拟器。原事故 APK 的资源被实际解析，APK 的 DEX、Activity 和完整安装程序没有运行。相机操作暂停不变。

## 运行

在工程根目录执行：

```sh
source .local/env.sh
.local/connection/venv/bin/python tools/install_boot_lab.py
```

输出到新的 `.local/compat-lab/<UTC时间>/`，不覆盖旧结果；可用 `--output .local/compat-lab/<新目录>` 指定路径。阅读 `results.json`；每个固件案例都有指令轨迹和 JSON 状态快照。未知方法/指令、缺失或变化的输入会报错，不会被默认当作成功。

使用已有 Android SDK aapt 30.0.3、PMCA Python 虚拟环境、baksmali 2.5.2 产生的本地解析结果，没有新增依赖或下载系统镜像。普通 `python3` 缺少 PMCA 导入需要的 Crypto；应使用上面的现有虚拟环境，不必重新安装包。

此环境依赖本机已有的私有输入。`config/install-boot-lab.lock.json` 固定 4.01 原始 ODEX、所选 smali、libdvm、内联表、原 APK、PMCA 源文件等 67 个文件的 SHA-256；开始和结束均核对。它不会自动获取固件，也不应随项目发布固件。缺少输入时会明确停止，而不是退化成纯假数据测试。

新解析的 framework 来源、命令与分析副本转换记录见 `handoff/runs/20261022T075951Z-install-boot-lab/framework-deodex.json`。只在派生副本调整 Sony ODEX 容器版本标签供 baksmali 读取，并使用匹配 libdvm 的真实内联表；原始固件未改变。早期有 AnalysisException 的解析结果不用于回放。

## 哪些部分实际执行

| 环节 | 实际执行 | 替身或未执行 |
|---|---|---|
| 图标 | aapt 解析事故 APK 的编译清单、图标资源；回放固件 `loadIcon`、Activity 默认图标回退、`Drawable.createFromXmlInner`、`IconCache.cacheLocked` | 资源服务、子 drawable 的 inflate、文字和像素渲染为替身；假设 XML 子资源能成功膨胀 |
| 安装标记 | 回放固件 `InstallAppProgress.createInstallStamp` 的分支、异常处理 | `File` 只操作内存中的虚拟文件列表；没有运行完整安装 Activity |
| 安装通信 | 执行固定版本 Sony-PMCA-RE 的真实 Python `installer.install` 循环 | 完全合成的消息和 FakeCamera；没有 APK 传输，没有 USB 上下文/驱动对象 |
| 重新进入同步 | 回放 `SyncAndroidService.Resume(8)` → `PackageManagerService.syncAppsFromFilesystemToRam` | 进入类型 8 是指定条件，不声称所有实际重启都经过此入口 |
| 状态变化 | 按固件执行检查标记、调用清理、扫描、写设置、删除标记的顺序 | Settings、扫描、清理、Binder、系统状态服务用显式适配器；不模拟真实 packages.xml、安装事务或原生 Backup |
| “重启”案例 | 序列化状态，再建立全新的对象和回放环境；断点案例从已写出的 JSON 快照重新加载 | 没有 bootloader、Linux、zygote、system_server、SSB、真实断电时序或恢复验证 |

每条轨迹带 smali 文件、文件行号、原方法的 `#@` 代码偏移。方法的分支与 try/catch 来自固件文本；宿主仅实现有限指令语义。每个案例列出所有实际经过的外部适配器。`Unsupported` 与模拟进程丢失不会被固件 catchall 吞掉。套件使用单线程，不证明并发锁、持久落盘或恢复时序正确。

新增包广播/后台线程分支尚无适配器；扫描替身返回指定成功/失败，且新增包列表为空。走到未支持调用即停止。此阶段不能证明完整 APK 安装成功或开机稳定。

## 本轮结果

24 个场景符合预期，其中 20 个固件方法案例、4 个真实 PMCA 循环案例。`passed` 表示观察到预期返回或预期异常，不是“相机兼容性通过”。

- **图标异常有条件复现：** 原 APK 应用图标为 `res/drawable/probe_icon.xml`（以实际结果文件为准），XML 根为 `layer-list`。在资源膨胀成功的替身条件下，固件分派为 LayerDrawable，启动器 `cacheLocked` 偏移 `0xbc` 强转 BitmapDrawable 时抛出 ClassCastException，该方法没有覆盖此处的异常处理。两次全新对象回放相同；这不等于整机循环重启。BitmapDrawable 类型对照通过，未制作修正版 APK。
- **100% 不是最终完成：** 合成 100% 进度后注入接收错误，真实 PMCA 循环抛错且未调用 sendEnd；收到最终完成消息才 sendEnd。失败完成消息也可以 sendEnd，因此 sendEnd 单独不代表安装成功。
- **同步受安装标记控制：** Resume 类型 8 才走本次跟踪的同步分支；类型 7 对照不进入。虚拟标记存在时会调用未完成安装清理及临时文件清理；无标记时不进入该清理分支。
- **扫描失败与标记删除并非绑定：** 注入 scanDirWithB 返回 false 或目录缺失，返回值为 false，但仍执行设置写入及标记删除。
- **删除返回值被忽略：** 注入 File.delete 返回 false，方法仍可返回 true，标记留存；下一次条件回放再次走标记分支。
- **中断/异常留存：** 删除前注入进程丢失、设置读写边界注入异常、Binder RemoteException，分别验证标记与异常控制流。它们是故障条件，不是相机捕获日志；真实 Settings 是否会向此边界传播这些异常未验证。

最新证据：`handoff/runs/20261022T075951Z-install-boot-lab/FINDINGS.md`。没有证明哪个分支实际造成事故，也没有证明修好图标即可恢复相机。

## 完整模拟器的社区线索

社区资料调研发现 [ma1co/qemu 的 BIONZ 板级实现](https://github.com/ma1co/qemu/blob/1909382c0d3533051cead7fde70ca8e84807ee14/hw/arm/bionz.c)，包含 CXD90014。此前只看官方 QEMU 板型列表，不足以排除社区支持，现予修正。

[OpenMemories-CI 的 CXD90014 测试](https://github.com/ma1co/OpenMemories-CI/blob/4f8c6367a75e9afd02bc684425e3fbff424b2223/tests/test_cxd90014.py) 目标是 DSC-RX100M5，包含更新内核、加载器及 USB 更新路径测试；直接内核测试替换 init 为 BusyBox shell。它不是 A7R II 正常 Android 开机/应用安装验收。完整加载器测试还使用 bootrom、boot1、boot5、nflasha1、Backup.bin、DmmConfig.bin、ulogio.bin；直接内核测试不要求全部这些文件。

本机尚无该 QEMU 二进制。官方 4.01 解包树按同名查找，只找到上述列表中的 DmmConfig.bin；这只是指定目录的文件名审计，不排除内核/其他材料在不同容器中。下一阶段可先研究更新内核在该板型下的最小启动，再判断正常系统所缺外设、配置和专有服务。不把 RX100M5 的测试映像或初始化配置直接当 A7R II。

本轮没有克隆/编译 QEMU、下载机身 dump，未复制 OpenMemories-CI 代码。完整相机环境与自动恢复能力仍未实现。

## 回退与使用边界

新增内容仅位于工具、测试、配置、文档及本地实验目录。删除本轮新增工具/配置/文档并还原对应索引即可撤销；不要覆盖已有未提交改动，不要删除原 APK、固件或事故证据。生产 App、相机、安装暂停文件都未修改。

这套环境适合先排除已知安装/启动控制流问题，不能作为再次装机或解除 `CAMERA_WRITE_HOLD` 的依据。实时反挤压、DSP、原生编码器和真实硬件性能不在此环境覆盖内。


## 后续：QEMU启动材料鉴定（2026-10-22）

最新材料审计在主系统nflasha3中找到了裸ARM vmlinux.bin和ext2 initrd，之前只按更新示例同名文件查找的清单不代表缺所有内核。Android/system、BusyBox和s_start_android.sh也齐备。已生成884 KiB的独立cramfs最小用户态候选并校验CRC/内容/链接；没有运行QEMU。这个候选是正常4.01内核+实验根，不是缺失的官方nflasha1更新系统。

CXD90014 QEMU把内核/initrd装载到0x80038000/0x80628000，但没有接普通-append；固件kemco覆盖入口指向VA0x40033000，候选用generic-loader在物理0x80033000注入独立参数。该地址、串口、电源GPIO和硬件启动仍待运行验证。

更关键的是固定QEMU的bionz_nand写入只报完成，擦除也不修改后端。必须补实际持久存储或明确采用不同的虚拟块设备，才能研究APK写入与整虚拟机重启。宿主当前缺可用的已核验Sony QEMU程序和pkg-config；未擅自安装工具或声称已构建。

详细缺口、候选manifest与后续验收顺序：`handoff/runs/20261022T082324Z-qemu-boot-readiness/FINDINGS.md`。候选：`.local/compat-lab/qemu-research/a7rii-4.01/shell-candidate/candidate.json`。原固件未修改，仍不操作相机。


## QEMU实际启动阶段（2026-10-22）

固定ma1co/qemu提交1909382c0d3533051cead7fde70ca8e84807ee14，使用本地TCI构建及非EXEC字节码缓存小补丁。原始正常内核、上轮最小cramfs和kemco加载实际成功；bootcon/PL011后端需mux=on。真实guest shell可读proc/sysfs、挂载tmpfs并写入读回，Binder/ashmem已注册。没有真实持久存储、Sony完整服务或Android开机。

从仓库根复跑：`python3 handoff/runs/20261022T084735Z-qemu-first-boot/boot_probe.py boot-recheck-01 20 --inspect`。输出名需未存在；工具核验输入hash，限制时长，只用进程管道和本机Unix socket，不接设备、网络或共享目录。退出后清理socket，留下串口、QMP、命令和结果JSON。

完整构建、失败阶段、宿主修改与边界见`handoff/runs/20261022T084735Z-qemu-first-boot/FINDINGS.md`。TCI模拟时钟和BogoMIPS不得作为实际录像/DSP性能证据。tmpfs读回不等于重启持久性；下一关仍是存储及Android服务链。


## NAND持久性与Android实际服务停点（2026-10-22）

外部QEMU补丁已把写/擦命令接入普通文件后端；旧版本失败、新版本整页/附加区、扇区、擦除跨新进程读回通过。qtest测试时CPU停止，因此只覆盖控制器，不能替代Linux/FTL文件系统重启测试。原Sony NAND驱动在devctrl注册报-65537，原生分区未挂载。

已将原/system ext2以只读loop方式加载，运行原Android init，/data和/cache暂为tmpfs。缺OSAL时显示库gralloc.diadem.so+0x638e发生空指针异常；logcat确认消息分配返回-9。加载原devno/osal_utm/osal_uipc后不再在此处崩溃，而反复等待Sony窗口服务连接，Zygote预加载也等待Sony消息应答。init.rc与原库未修改，不是用假服务应答跳过启动。

G08仍进行中：缺真实存储初始化与原生窗口/其他Sony服务；桌面、APK安装、真实重启同步和事故复现未完成。详细命令、原始hash、实验对照及回退见`handoff/runs/20261022T091300Z-qemu-storage-android/FINDINGS.md`。当前可复跑：`python3 handoff/runs/20261022T091300Z-qemu-storage-android/run_guest.py android-recheck-01 130 handoff/runs/20261022T091300Z-qemu-storage-android/android-final.commands --android-osal`，输出名需未存在。只连接本机Unix socket和专用普通文件，无设备/网络透传。


## 同机型配置与备份前置依赖（2026-10-22）

固定A7R II分支的接线只能作为候选：本机旧MB89083未实现其CID/CRC协议。实际Android改接线对照未推进窗口连接，IRQ170未启用/挂起，定时器正常；不修改GIC来掩盖未启动的BOSS链路。原版native im已执行；补原版备份文件、原kemco中的预留内存和Backup_load=1后backup.ko加载成功，窗口/JNI等待仍在。实验initrd移到0x90000000，避免与预留区重叠；没有修改原固件代码。

完整逻辑分区约438.75MiB，仍缺FTL/控制状态；/data仍tmpfs，无法据此验收安装后重启保留。详细对照与复跑入口：`handoff/runs/20261022T100302Z-a7rii-board-alignment/FINDINGS.md`。每次独立启动，保存失败结果，禁止相机透传。没有采用社区的跳错、异常存活或假成功补丁。

随后改用原版bootin.elf启动调度，im.elf实际加载了libObj.so；当前停止在THREAD_INFRA0的dmp_allocator_lib_init断言（dmp_allocator.c:103，e == MA_ErrNone，gl_common池）。具体底层错误与依赖尚未闭环，未禁用断言或伪造成功；完整system_server、窗口服务和桌面仍未通过。详细原始串口与地址映射见本轮android-bootin-01及native-assertion.json。这是模拟环境的新停点，不是故障相机重启原因复现。

## gl_common依赖定位（2026-10-23）

实际断点读取证明缺grm_ma回调时同步发送为-1020，补原驱动后发送为0而创建为-9999。原生服务按原启动表先于Android单独验证；DMM配置补齐后还依赖osal_ulogio的0x61记录区。当前/setting/ulogio.bin确实缺失（原filp_open返回-2），更新包未找到该输入；没有用替身返回或移除断言推进。

完整过程与仅原生诊断的复跑入口见`handoff/runs/20261022T225823Z-gl-common/FINDINGS.md`。G08未完成；实验guest固定地址/只读调试不是机身设置。完整Android、APK、冷启动数据保留与真实事故原因仍未证明。
