# 当前完整模拟器受GPU协议与BOSS载荷缺口阻断（2026-10-23）

R25 排除了三处BOSS指纹误命中：两个暖启动片段对应原Android资源偏移表，ODEX命中为字符串索引。另两个弱候选仍未确认，未取得匹配程序。26项来源、结构及保护核查通过；没有新客体、相机操作或模型/原固件修改。

当前11项要求审计确认：GPU仍只取指解包，最新同模型运行IRQ76为0；原生窗口/输入、完整Android、持久data和APK生命周期未完成。没有活跃QEMU可等待，连续多轮的GPU完成规则/BOSS程序缺口保持。后续推进需要可与4.01核对的新规范、可靠实现/已有正常离线轨迹，或匹配载荷及加载依据；完整目标不缩减、不标完成。

详见[研究手册](docs/research/README.md)、[接续条件](docs/research/CONTINUATION.md)及R25证据。下方是阶段历史，保留已有成果与失败记录。

# 当前MA缓存入口已核实，GPU执行完成仍未实现（2026-10-23）

R24 用原系统代码段、符号与原指令读回确认MA cache入口地址。上轮E14发生在用户态调试读取；原程序正常进入内核后同地址读回成功。限定启动到首提交后的等待入口，该cache入口未命中，命令包和128字节对象从物理RAM读回吻合。

两轮客体检查完成，50项证据核查通过，IRQ76仍为0。原固件、9项保护输入与QEMU模型不变；没有新增GPU执行、原生窗口、Android或APK验收。下一步回到GPU事务完成条件、高层窗口队列/fence与匹配BOSS来源。详见[研究手册](docs/research/README.md)的R24；下方旧停点作为历史保留。

# 当前研究文档已汇总，缓存观察尚待核验（2026-10-23）

五份[研究手册](docs/research/README.md)汇总应用事故、录像链、模拟器开发、同代机型比较及 R01–R23 证据。入口页提供能力表和术语，后续文档保留详细接口、版本、hash、来源与验收条件。

最新 R23 记录了首包地址写入、4组提交和bit31等待；MA cache入口读回E14，观察器核验失败，不能据零命中推断没有缓存调用。客体最终检查完成、IRQ76仍0，与观察器失败分别记录。下一步先核实模块运行地址和调试上下文；原固件、9个保护输入与QEMU模型保持，完整窗口、Android和APK验收没有新增进展，G08/G10保持阻断。

本次收尾更新文档及公开源码备份；公开范围排除固件、反汇编、原始日志与私人环境，提交使用匿名邮箱。下面为阶段历史，旧“当前/最新”标题不覆盖本节。

# 当前：原生缓冲服务已定位，首包停点仍在 GPU 完成条件（2026-10-23）

R22 核实原生 `libObj` 的窗口缓冲服务注册、线程与命令1/2分派。锁定/解锁处理体仅更新共享记录和信号量，不调用GPU完成等待。一次只读四断点观察先命中GPU首提交；此前未命中服务注册、线程创建或等待入口。39项原字节、运行与保护核查通过，最终IRQ76仍为0。

原固件、9个保护输入及QEMU模型保持，相机暂停保留。没有新增窗口显示、Android、持久/data或APK验收，G08/G10仍阻断。下一步追原生首包实际cache调用、GPU访存完成生产端；匹配BOSS及高层窗口队列仍未闭合。详见[研究手册](docs/research/README.md)、[技术链路4b](docs/research/TECHNICAL.md)和[证据R22](docs/research/EVIDENCE.md)。下方为阶段历史。

# 当前：内存映射、窗口协议与研究手册更新（2026-10-23）

五份[研究手册](docs/research/README.md)已建立，R21 补充原生缓冲映射、CPU 缓存属性与窗口客户端协议。一次只读 QEMU 观察确认 128 字节对象和命令包均在 `/dev/stream` 映射中，虚拟/物理地址换算与读回相符；原 stream 驱动请求 uncached 页属性。`0x158` 已追到 Android 私有格式参数，但具体像素布局仍未知。

45 项输入、指令、映射和保护核查通过。观察时 IRQ76 仍为 0，没有新 GPU 执行、窗口、Android 或 APK 验收。原生窗口服务端、实际缓存维护调用与 GPU 完成规则仍待追踪；匹配 BOSS 程序仍缺，G08/G10 保留阻断。未操作相机，原固件、QEMU 模型、合成介质及相机暂停保护均保持。

详细技术事实见[技术链路第 4a 节](docs/research/TECHNICAL.md)，证据编号见[索引 R21](docs/research/EVIDENCE.md)。原始载荷、反汇编、运行日志和私人环境只留本地；公开备份仅纳入审阅后的自写资料。下方是此前阶段记录。

# 当前：研究文档汇总与模拟器真实边界（2026-10-23）

新入口：[研究与开发手册](docs/research/README.md)，包含探索时间线、技术链路、证据资料和接续指南。它覆盖截至A6000/RX100 V原DMP库比较的成果，并明确哪些早期结论已被后续证据修订。

本次五份手册已[同步GitHub](https://github.com/conaneva2/cinevista/commit/540e07395c455b0c8eafbde3c09c7c10ce70d38d)，两份工作区工程检查均退出0；公开源码树与审核副本一致，提交身份使用匿名邮箱。此项完成只代表文档与备份交付。

最近研究确认：RX100 V 2.00的DMPSUGIRM/EGL/GLES2与A7R II 4.01整库一致；A6000 3.21的共同提交/等待链可参照，但固定池与gralloc分支存在真实差异。62+56项静态核查通过。它们没有补齐GPU访存完成到IRQ76的条件，匹配BOSS程序及加载依据仍缺。

已通过范围：最小Linux、合成NAND控制器跨进程读回、有限原生初始化与安装方法回放。未通过：原生窗口/输入、完整Android桌面、持久/data、APK安装启动与冷启动。G08/G10保持阻断；操作台仍是宿主预览。没有新机身操作、断言绕过或GPU执行模型。

下一步沿MA映射/缓存属性与ws_hal缓冲所有权追踪，同时寻找匹配BOSS载荷和GPU完成规范；新的符号清单不计作行为证明。详见[接续指南](docs/research/CONTINUATION.md)。

公开仓库为审阅后的源码备份；原始固件、派生反汇编、私有环境和原日志不公开。下面是历史阶段记录，其旧“最新”标题不覆盖本节。

# GitHub 公开源码快照｜2026-10-23

## 2026-10-23：公开资料整理

公开协作入口统一为 CONTRIBUTING.md、docs/04_WORKFLOW.md 与产品文档；内部工具配置和专用交接材料已从当前源码树移除。当前相机暂停、仿真欠项与硬件验收状态不变。已复用本地工具链运行 python3 tools/cv.py check，退出码为 0；当前源码树文件名与文本检查未发现内部工具名称残留。

本副本排除了私人环境、固件、原始日志和旧 Git 历史。新增源码级 QEMU 补丁归档；许可和发布边界见 [PUBLICATION](docs/PUBLICATION.md)。下方为各阶段研究记录，旧结果不能覆盖最新边界。完整相机模拟器、Android 桌面、APK安装与重启验证仍未通过。

最近独立存储探针在原驱动冷初始化时记录到 mumin_devif_init 超时和 boss_init 返回 -10003；70秒宿主观察窗口内未完成模块加载，不能据此认定存储可用。未操作相机。

# 幕野 CineVista｜当前状态（2026-10-23）

## 最新：GPU诊断与公开实机日志已对照，完成产生条件仍未闭合

原GPU诊断入口审计确认任务软件signal不能代替硬件IRQ；新公开A6000日志支持同系列SMAPH-S30/IRQ76，但缺逐命令硬件协议。未新增执行模型或启动进展，窗口/Android/APK仍未通过，长期目标进行中。

原驱动18个ioctl分支静态复核；0xc004820d/e为任务间通知，0xc0048203等待GPU状态，不能接错。原srm_hw_reset直接返回0，恢复入口重新初始化寄存器，没有提供所缺的端口完成合同。新查cokeenet/zve10-qemu采用常量寄存器与图形替代返回，未合入；nicolvus/a6000-fw-decomp公开日志有IRQ76/dmpgles2累计6060，但其驱动与本机哈希不同，未直接移植。

本轮无客体启动、固件/QEMU改写、相机操作或大下载；小范围公开文本约1.30 MiB。继续离线追原生存储初始化等独立缺口，不凭猜测注入完成中断。证据与下一步：`handoff/runs/20261023T022306Z-sugilite-diagnostics/FINDINGS.md`、`handoff/runs/20261023T022306Z-sugilite-diagnostics/SESSION.md`。G08/G10仍进行中，CAMERA_WRITE_HOLD保留。

## 最新：原GPU命令名和128字节用途已证实；空同步提交仍待硬件完成合同

原4.01 Android DMP库保留DWARF和符号表：首四条已对应CU_DUMMY_READ_ADDR、CU_DUMMY_READ_START、RAS_ITERATOR、SYS_FRONT_PORT0。128字节全局明确为dmp_error_tex_buffer_id，初始化、8×8/A8L8备用纹理配置、虚读尾部引用均解析到同一GOT槽。不能向它写“完成标记”；128字节纹理大小也不等于虚读宽度。

新增只读客体实验，两处原指令断点确认命令计数0→4、wait_done=1，首次确为空同步提交。原GLES1/GLES2的293项寄存器枚举交叉一致。驱动等待/清理bit31已知，但端口传播、mask四位字段、虚读宽度和完成顺序仍未证实；未为推进启动注入IRQ或改原断言。原窗口/Android/APK仍未通过，没有新增GPU执行模型。

本轮保留语义提取和动态证据，继续执行用户要求的模拟器长期目标。公开资料复查未找到匹配硬件合同；搜索受限处明示。未改原固件、三版QEMU或默认操作台，无相机操作/新APK/工具安装/大下载。证据：`handoff/runs/20261023T015609Z-sugilite-semantics/FINDINGS.md`；续接：`handoff/runs/20261023T015609Z-sugilite-semantics/SESSION.md`。G08/G10保持进行中，CAMERA_WRITE_HOLD保留。

## 最新：首个GPU命令构建已追清，取指前端已运行；执行与完成仍待证

原4.01实际写观察确认单值包为头字加值、每组8字节，首个提交计数4对应32字节。已追到+6bd0a0通用构建函数和+69b190调用端；地址操作数来自128字节缓冲的物理地址右移4位。该缓冲由原程序填成64个ff00，动态读取吻合；没有证据把它当成完成标记，未擅自写入结束常量。

独立QEMU新增可选取指解包观察器，原固件三次真实提交均解析一致。4组前端qtest和6组控制回归通过，原grm_gles仍加载0；IRQ76仍为0，原超时复位/重试保持，窗口和Android未前进。当前只有执行模型前端，没有GPU指令副作用、DMA写回或完成中断。官方源码仅证实平台/IRQ；社区DMP相关代码虽有相同结束常量，格式/寄存器用途不同，不能照搬。

保留未命中断点和错误探针的失败记录，修正“模板直接提交”的初步推断；实际首包由通用函数重建。22项原输入、默认操作台及前轮QEMU哈希均不变。无相机操作、断言绕过、新APK或大文件下载，仅缓存约54 KiB社区文本。G08/G10仍进行中，CAMERA_WRITE_HOLD保留。

证据：`handoff/runs/20261023T012044Z-sugilite-command/FINDINGS.md`；复跑与明确欠项：`handoff/runs/20261023T012044Z-sugilite-command/SESSION.md`。下方为前阶段记录。

## 最新：sugilite上电检查通过，阻塞已推进到GPU命令完成等待

已结合Sony官方CXD90014内核源码和原4.01驱动，独立构建可选时钟/复位控制寄存器实验模型。原grm_gles上电读回实际为0x15，原断言正常通过、模块加载返回0；没有修改客体代码或发送伪造完成中断。

原libObj随后真实映射GPU窗口，并写入任务地址/启动参数；ioctl 0xc0048203等待0x80000000，IRQ76保持0。已观察到3000 jiffies超时、原关钟/复位/上电/寄存器重建、用户态返回-1并重新提交。THREAD_INFRA0仍等待GPU，原生窗口/Android桌面/APK未通过。GPU指令执行、图像/栅栏写回、完成中断和帧同步未实现；零上电初态、AVB字段与真实频率/时序的对应仍属待证，不宣称完整硬件等效。

下载前提醒后取得1个50.4 MiB官方内核包，仅提取有关源码；没有新依赖安装。官方QEMU显示适配是另一套通用CLCD，不能替代相机sugilite；尚未找到可据以实现的完整公开GPU规范。6组控制寄存器qtest和13项证据一致性通过；22项原输入与旧QEMU哈希不变。旧操作台仍固定原二进制，新模型按选项启用。无相机操作、新APK或断言绕过，G08/G10继续进行中，CAMERA_WRITE_HOLD保留。

当前证据：`handoff/runs/20261023T004916Z-sugilite-model/FINDINGS.md`；复跑和下一停点：`handoff/runs/20261023T004916Z-sugilite-model/SESSION.md`。下方均为阶段历史，不覆盖本节。

## 当前第一步：虚拟相机；TextRM 已通过，图形硬件模型是当前阻塞

按原固件路径补齐字体列表与六个字体文件后，原 TextRM 初始化返回0，Appframework 正常通过原来的字体断言。恢复原 /dev/uinput 节点后，D keyboard 注册成功。上一轮 DMM/gl_common 创建成果保持；本轮未修改任何原固件代码。

Appframework 随后推进到图形帧缓冲：窗口中间对象非空，但 GraphicsContext3DShaderMusashi.cpp:292 的窗口表面创建返回空，触发后续原 CreateFramebuffer failed 断言。原 grm_gles 驱动单独加载时在 sugi_hw.c:221 停住：写入图形电源寄存器后读回0，而原条件要求0x15；QEMU地址表缺少对应MMIO及图形设备。完整原生窗口、Android桌面、APK仍未通过。

已保存输入节点、字体与原图形驱动的分组对照和只读动态返回证据。22项原输入与QEMU哈希不变，无机身/USB/ADB操作、断言绕过、新APK或下载。现有相机背面操作台仍固定上一轮启动配置，显示/按键仍属宿主控制台；新字体实验通过本轮SESSION复跑，未静默更换界面配置。

下一关是有依据地实现图形时钟/复位、任务完成与显示缓冲，再联启Android。G08/G10保持进行中；不以模拟器缺设备推断真实A7R II不支持，也不以当前进展保证真机安全。CAMERA_WRITE_HOLD保留。

本轮证据：`handoff/runs/20261023T002402Z-sugilite-window/FINDINGS.md`；续接：`handoff/runs/20261023T002402Z-sugilite-window/SESSION.md`；使用：`docs/VIRTUAL_CAMERA.md`。

## gl_common原始错误已定位；当前缺少日志配置输入

离线只读断点确认：未加载grm_ma时，gl_common消息发送返回-1020（接收回调缺失），客户端仍读取未得到有效应答的结果并触发断言；不能据此判断硬件内存不足。加载原版grm_ma后同步发送返回0，但下游DMM未运行，创建返回-9999，原断言仍保留。

按原/sbin/init顺序补DmmConfig.bin后，DMM越过配置读取，停止于dmm_ctrl_Init+0xd4：缺osal_ulogio提供的0x61日志记录区，R0/R6为0。加入原版osal_ulogio后，实际filp_open("/setting/ulogio.bin")返回-2/ENOENT；更新包setting清单和已提取系统未找到该文件。核心库还未越过gl_common，下一步需定位匹配配置来源/生成过程及其内存范围，不用假地址或跳过断言。

本轮无相机操作、无下载、无新APK或固件/QEMU补丁。只在guest中固定调试地址并读取寄存器/内存；错误、缺输入与短窗口等待均保留。G08仍in_progress，完整Android、持久存储、APK与事故复现均未通过。证据：`handoff/runs/20261022T225823Z-gl-common/FINDINGS.md`；续接：`handoff/runs/20261022T225823Z-gl-common/SESSION.md`。

## 同机型分支对照：已进入Sony核心库初始化，停在内存分配断言

对照固定 frozencaviar/OpenMemories-CI@423179bd 的 A7R II 4.01 实验：已验证 MB89083/sio3/GPIO5 bit14 候选连线，旧模型仍缺新应答协议；更换连线未突破当前 Android 等待。两组实际启动均未见 IRQ170 堵塞，定时器继续计数，未照搬 GIC 优先级或固件错误绕过补丁。

官方逻辑分区末端438.75 MiB，64 MiB空白介质不能代表正常系统；压缩分区、LTU/FTL和bootloader控制信息仍缺。原版im.elf已执行；备份驱动先因缺路径失败，补原始默认文件后推进到file_load失败。恢复固件规定的备份预留内存、移开大型实验initrd并使用原驱动Backup_load=1后，backup.ko实际加载成功，没有修改原内核/驱动或默认数据；随后改用原版bootin.elf启动调度，im.elf实际加载了libObj.so；当前停止在THREAD_INFRA0的dmp_allocator_lib_init断言（dmp_allocator.c:103，e == MA_ErrNone，gl_common池）。具体底层错误与依赖尚未闭环，未禁用断言或伪造成功；完整system_server、窗口服务和桌面仍未通过。

这些是电脑实验条件的补齐，不是故障相机状态复现或安装安全保证。未操作相机、未下载大文件、无新APK，G08继续进行中。证据：`handoff/runs/20261022T100302Z-a7rii-board-alignment/FINDINGS.md`；续接：`handoff/runs/20261022T100302Z-a7rii-board-alignment/SESSION.md`。


## 虚拟闪存底层持久性已通过；Android推进到Sony服务等待

已修补外部定制QEMU的NAND写/擦空操作，整页/附加区、扇区和块擦除在关闭整个QEMU后新进程读回通过。此为控制器级测试；原版Sony NAND驱动仍在devctrl初始化报mumin_mount -65537，未获得Linux可挂载的持久分区，Android /data暂用tmpfs。

原版4.01 Android init与只读/system已实际执行。未加载OSAL时SurfaceFlinger在gralloc.diadem.so+0x638e空指针崩溃，logcat确认osal_valloc_msg返回-9；加载原版devno/osal_utm/osal_uipc后该故障消失，显示服务改为等待Sony窗口连接，Zygote预加载也进入Sony JNI消息等待。尚未完成桌面、完整system_server、APK安装或事故复现，G08仍in_progress。不是恢复能力或再次装机保证。

未操作相机、未改原始固件、无新APK或大文件下载；CAMERA_WRITE_HOLD、T11/G03不变。下方“Android未执行/NAND未修补”为历史阶段，本节更新其进度。证据：`handoff/runs/20261022T091300Z-qemu-storage-android/FINDINGS.md`；续接：`handoff/runs/20261022T091300Z-qemu-storage-android/SESSION.md`。

## 定制QEMU已构建，4.01最小Linux已进入命令行

本机已构建固定Sony QEMU 5.1.0；原生TCG受Apple Silicon可执行内存分配限制，最终采用TCI解释器和仅针对字节码缓存的非EXEC补丁。修正bootcon/PL011串口复用后，原始4.01内核成功挂载884 KiB实验根并运行BusyBox shell；独立启动的串口命令验证proc/sysfs、tmpfs写入读回，以及Binder/ashmem运行时注册。原始固件hash不变。

G07完成范围是宿主构建与最小Linux实际启动。完整Sony服务、Android、更新系统、APK均未执行；没有持久磁盘分区，NAND写/擦空操作仍未修复。不能据此推断原事故已复现、相机可恢复或实时反挤压可用。未操作相机、无新APK，T11/G03与CAMERA_WRITE_HOLD不变。下方“尚未开机/缺工具”为上一阶段历史状态，已由本节更新。
证据：`handoff/runs/20261022T084735Z-qemu-first-boot/FINDINGS.md`；续接：`handoff/runs/20261022T084735Z-qemu-first-boot/SESSION.md`。

## QEMU启动材料已鉴定，最小Linux候选已准备，尚未开机

官方4.01的nflasha3内实际有裸ARM Linux 3.0.27内核和ext2 initrd；已有BusyBox、Android 4.1.2/API16系统与chroot启动脚本。已准备884 KiB最小cramfs实验根并做CRC/内容/链接回读，原始输入未改。定位kemco参数读取到VA0x40033000（物理0x80033000候选），QEMU此板型没有接普通-append。专用更新分区nflasha1和设备个体状态仍缺，updater.img不是完整可启动系统。

重要限制：ma1co/qemu固定分支的bionz_nand写入分支不写后端、擦除只报完成，不能直接用于APK落盘/重启保留验证。还需核验板级启动、补持久存储、Sony服务/图形/Backup与SSB。宿主缺已核验的Sony QEMU二进制及pkg-config，未安装依赖、未编译或启动QEMU；没有更新系统/Android/APK执行证据。G06完成范围仅为本轮材料鉴定和候选准备；T11/G03及CAMERA_WRITE_HOLD不变。
证据：`handoff/runs/20261022T082324Z-qemu-boot-readiness/FINDINGS.md`；续接：`handoff/runs/20261022T082324Z-qemu-boot-readiness/SESSION.md`。


## 安装启动兼容环境第一阶段已运行

已建立仅主机的固件方法回放环境：实际解析官方4.01和原事故APK资源，24个条件案例符合预期（20个方法、4个真实PMCA循环）。图标在资源膨胀成功的替身条件下触发启动器BitmapDrawable强转异常；100%进度不代表最终完成；同步方法在扫描失败后仍可删除安装标记，而删除失败的返回值会被忽略。文件系统、Settings、扫描、Binder和绘制为显式替身，没有执行完整APK/Android开机，也没有复现真实整机循环重启或确认唯一根因。

社区资料中找到ma1co/qemu的CXD90014模型及OpenMemories-CI的RX100M5更新系统测试，修正此前仅依官方板型列表的判断；A7R II完整正常系统仍未启动。G05完成范围仅为本阶段方法实验环境，G03仍in_progress、T11仍blocked。未操作相机、未改生产源码/原始固件、无新APK，保留CAMERA_WRITE_HOLD。
入口：[实验环境说明](docs/INSTALL_BOOT_LAB.md)；证据：`handoff/runs/20261022T075951Z-install-boot-lab/FINDINGS.md`；续接：`handoff/runs/20261022T075951Z-install-boot-lab/SESSION.md`。


## SDF缓冲区归还、帧同步与仿真环境调研

官方4.01静态确认SDF与MC共用MMC队列0061003c；SDF消费输入票据并返回新票据，MC分离图像/YC描述释放且有定时释放和Vsync延迟回收。未找到现成SDF逐帧回送录像桥接，吞吐仍unknown。整机模拟缺专用板级/硬件模型；优先候选为按固件约束的安装启动兼容环境，尚未建成。原事故APK重检仍因XML图标拒绝exit2，不是整机故障复现。未操作相机、未改产品代码/固件、无新APK，保留CAMERA_WRITE_HOLD，T11仍blocked。
证据：`handoff/runs/20261022T073608Z-sdf-lifecycle-emulator/FINDINGS.md`；续接：`handoff/runs/20261022T073608Z-sdf-lifecycle-emulator/SESSION.md`。

## 实际录像接收端与独立缩放后端续查

官方4.01离线已找到SCALAR_MOVIE_REC选择的实际拓扑：Camera→Scalar录像出3→Effect→MovieRecorder入0；录像对象请求原生MovieEncoder主路YC输入，默认物理目标MC(type0,dir1,no0,osal005700f9)。中间VEF/可选TCUB及效果、编码规格分支仍需保留，未确认目标机运行时选择，不能声称所有录像模式完全闭环。SCALE/resizeTrim已追至model1/event0xa→ObjScalar3017→HAPI201→SDF票据式缩放任务，含标准YC输出与完成回执；没有已验证的逐帧回送录像连接或实时性能。T11仍blocked；未操作相机、未改产品代码/固件、无新APK，保留CAMERA_WRITE_HOLD。
证据：`handoff/runs/20261022T034123Z-movie-peer-scale-backend/FINDINGS.md`；续接：`handoff/runs/20261022T034123Z-movie-peer-scale-backend/SESSION.md`。本节更新下方较早“尚未定位实际模式接收端”的进度，不将静态配置等同机身验证。

## 录像动态连接与DSP几何离线续查

官方4.01离线确认录像槽6对应SFR(type0,dir2,no1)，上层对象pinNo3映射到该端口；已追清嵌套连接消息、运行时对端写入与发送读取，但目标录像模式的实际编码对端四元组仍未闭环。原生SCALE/resizeTrim接受独立宽高，不能直接等同于SA录像插件；所查VFX是Transfer，尚无自定义DSP反挤压与实时性能证明。T11仍blocked；未操作相机、未改产品源码/固件、无新APK，保留CAMERA_WRITE_HOLD。
证据：`handoff/runs/20261022T032031Z-rec-pin-dsp-geometry/FINDINGS.md`；续接：`handoff/runs/20261022T032031Z-rec-pin-dsp-geometry/SESSION.md`。本节更新下方较早的动态连接调查进度，仍不宣称实际录像链完整闭环。

## DSP处理画面至录像通道离线追踪

官方4.01离线已把DSP插件路径5追到0x3039→SFR路径0x32→EffectMovieRec；SA输出经VFX形成画布，路径0x32将该画布标识/句柄替换进RecPin并交出。原生McPinMain→McAvcEncVfm图像接收实现也已定位，但RecPin输出槽6的动态连接到目标编码模式尚未闭环，不能宣称反挤压录像可用或硬件不可行。自定义几何处理、格式/帧率与恢复能力仍未证明；未操作相机、未改产品源码或固件、无新APK，T11仍blocked。
证据：`handoff/runs/20261022T023458Z-dsp-movie-chain/FINDINGS.md`；续接：`handoff/runs/20261022T023458Z-dsp-movie-chain/SESSION.md`。本节更新下方较早“路径5去向未闭环”的调查进度；最后动态路由缺口仍保留。

## 编码前反挤压与相机源替换离线鉴定

官方4.01离线确认Sony录像源仅接受0/1，prepare/start走SDCom；所查标准Camera HAL录像入口直接返回错误。StreamBuffer为ES及管理区契约，未找到裸帧输入。DSP预览插件record选项真实选择路径5并进入SCALAR_CAMERA_PATCH，但到原生编码输入尚未闭环；不能由入口限制断言硬件不可能。软件H.264实现存在，实时性能未知，不作为当前主方案。未操作相机、未改设备代码、未生成APK，继续暂停。
证据：`handoff/runs/20261022T021116Z-video-encoder-feasibility/FINDINGS.md`；续接：`handoff/runs/20261022T021116Z-video-encoder-feasibility/SESSION.md`。

## 实时反挤压两路径离线鉴定

用户要求先判断机内实时反挤压的实现可能，暂不操作相机。官方4.01的SmartRemote存在CameraSequence连续取JPEG并读入应用缓冲区的实际代码；B路径取得明确实现依据，但第三方访问、机内解码显示性能、LCD/EVF与拍摄共存仍unknown。普通预览HAL使用0x158特殊描述格式，gralloc只分配32字节描述信息；当前项目只请求SurfaceView尺寸，未建立A路径实际视频非等比缩放链。不能据此断言硬件绝无可能，也不能宣称实时反挤压已可用。

T11提升为当前P0可行性门槛，离线初判完成，整体验收仍blocked；原生颜色需求保留并后置。没有新增相机操作、APK或固件补丁，保留事故暂停标记。详细证据：`handoff/runs/20261022T014755Z-desqueeze-feasibility/FINDINGS.md`；续接：`handoff/runs/20261022T014755Z-desqueeze-feasibility/SESSION.md`；决定：`docs/adr/0014-desqueeze-feasibility-gate.md`。

## 更新环境恢复能力离线调查

离线确认固定PMCA包含ILCE-7RM2更新载荷，型号与官方4.01匹配，主体firmware段0字节、带updater模块；但USB入口仍依赖已可通信设备，源码自动可写挂载设置区，应用数据恢复涉及双备份与同步。尚未验证故障时独立入口或可靠回滚；未操作机身、未生成新固件/APK，继续暂停机身操作。
证据：`handoff/runs/20260927T053659Z-recovery-feasibility/FINDINGS.md`；续接：`handoff/runs/20260927T053659Z-recovery-feasibility/SESSION.md`。

## Windows无电池充电接口已确认

用户Windows11只读记录确认：无电池、OFF、USB连接时054C:0994，Class03/00/00，USB Charger，状态OK；采样只记录一次出现。已确认充电HID枚举，不等于MTP/MSC/恢复接口。源码核验尚无可验证充电HID到恢复模式的转换路径。
证据：`handoff/runs/20260920T052255Z-charger-interface-review/FINDINGS.md`；续接：`handoff/runs/20260920T052255Z-charger-interface-review/SESSION.md`。

## G03 最终包门禁已落地，生产图标待修复

G03新增最终包启动图标/组件契约：复用aapt30.0.3解析编译清单、全部图标配置并解码PNG；拒绝XML/别名/系统图标、NinePatch、额外组件及显式process/persistent。11项测试通过；事故原APK拒绝exit2，当前源码构建在资源预检按预期停止exit1。未替换生产图标、无新可安装APK、无机身操作。
证据：`handoff/runs/20260920T041708Z-launcher-gate/FINDINGS.md`；续接：`handoff/runs/20260920T041708Z-launcher-gate/SESSION.md`。

## 用户提供恢复案例核验

引用来源存在语言解锁关闭后恢复的用户自述，但前提为已有解锁设置且能进Mass Storage；不符合目前已知安装史及USB表现。DPReview两帖403，浏览器超时，正文未读到。未改变机身操作暂停。
证据：`handoff/runs/20260920T040707Z-user-source-review/FINDINGS.md`。

## 控制台设备路由核验

离线从原始initrd确认/dev/ttycons为指向ttyAM0的符号链接，内核含AMBA/PL011驱动字符串；init根据/proc/cmdline中的console=ttyAM0选择launch_shell参数。未确认物理针脚、电平、实际启用或故障日志；不是USB恢复已可用。
证据：`handoff/runs/20260920T035712Z-console-routing/FINDINGS.md`；续接：`handoff/runs/20260920T035712Z-console-routing/SESSION.md`。

## 原生输入与早期控制台调查

进一步确认Sony输入服务通过uinput转发按键，初始化/资源状态切换不能等同于持续采样所有已按住按钮；安全模式物理触发仍未证实。早期init的forced-senser检查读取机内文件，非已发现的按键/SD卡入口；另定位独立于Android的控制台程序及设备路径，物理接入未验证。
证据：`handoff/runs/20260920T035024Z-input-bridge-analysis/FINDINGS.md`；续接：`handoff/runs/20260920T035024Z-input-bridge-analysis/SESSION.md`。

## 安全模式静态调用链已解析

使用同固件libdvm真实22项内联表与仅改容器版本标记的离线分析副本，解析出ServerThread→detectSafeMode→enterSafeMode静态调用链；关键方法无解析占位错误。InputServant存在uinput及默认映射，但物理按键/早期持键状态/故障进度未闭环，仍不能给出可靠安全模式操作卡。
证据：`handoff/runs/20260920T034308Z-safe-mode-callchain/FINDINGS.md`；续接：`handoff/runs/20260920T034308Z-safe-mode-callchain/SESSION.md`。

## 启动路径离线核验与观察器补全

离线确认4.01保留安全模式检测方法，但启动调用链有Sony优化字节码解析缺口，不能据此给出按键恢复步骤。ADB脚本/属性存在不等于对外可连接。修正被动USB记录范围：追加全部VID/PID及可用的数字端口位置，不再只依赖Sony厂商筛选；新增3项反向测试通过，未重新通电。
证据：`handoff/runs/20260920T033623Z-boot-path-analysis/FINDINGS.md`；续接：`handoff/runs/20260920T033623Z-boot-path-analysis/SESSION.md`。

## 恢复入口继续核验

继续离线核实恢复入口：官方4.01镜像包含android_console.sh及启动adbd的配置，但不证明故障机暴露ADB、可连入shell或可卸载应用。未找到已验证A7R II安全模式按键；搜索到的Sony安全模式说明适用于Xperia手机。
证据：`handoff/runs/20260920T033316Z-recovery-entry-triage/SESSION.md`。

## 上游Issue复核

通过GitHub只读API筛选478条open Issue标题/正文，并读取12条重点帖完整评论。#433评论确认A7RM2，安装中断后循环重启且USB来不及连接，未报告软件恢复；#702安装APK后OFF仍重启与本机相似。#488提供A6000特殊15针接口读取启动日志线索，尚未验证适用于A7R II。
证据：`handoff/runs/20260920T032059Z-upstream-issue-review/FINDINGS.md`；续接：`handoff/runs/20260920T032059Z-upstream-issue-review/SESSION.md`。

## 厂家恢复工具检索

确认A7R II厂家维修手册使用Adjust Station及本型号Adjust Manual，但未证明黑屏无USB时可强制重刷。公开4.01升级器要求USB Mass Storage，已有4.01按官方流程结束。未找到可验证的本故障救砖包；无机身操作。
证据：`handoff/runs/20260920T031004Z-manufacturer-recovery-research/FINDINGS.md`；续接：`handoff/runs/20260920T031004Z-manufacturer-recovery-research/SESSION.md`。

## 最新安装复盘与OFF现象

用户确认仅电池、USB已拔掉时，拨到OFF后仍重复重启动作数次。复核原始命令/报错及官方4.01：Installing 100%在正常路径对应机身安装器成功回调后的通知，但结束握手未确认；错误在GetProxyMessage数据阶段返回后读取PTP响应时，未保存数据体，不能断言机身未发完成消息。APK传输/落盘/状态收尾不完整与新资源触发系统兼容故障继续并列调查。Sony安装器会尝试创建安装标记，恢复分支会同步应用，因此未刷固件不能推导未改变系统维护的状态。无新增机身操作、无恢复结论。

复盘：`handoff/runs/20260920T024526Z-install-forensic-review/FINDINGS.md`；续接：`handoff/runs/20260920T024526Z-install-forensic-review/SESSION.md`。原APK与安装日志哈希已留存；本轮仅主机分析，未生成或安装新APK。

## 官方固件离线调查：启动图标兼容性缺陷

官方ILCE-7RM2 4.01固件已在Mac离线解包。启动器IconCache.cacheLocked在loadIcon后无保护地强转BitmapDrawable；原安装APK的图标是XML layer-list，存在具体类型不兼容。该静态缺陷是循环重启的重要嫌疑，但缺相机崩溃日志与恢复验证，不能宣称已确认根因或硬件损坏。原APK继续隔离，没有生成或安装修正版。
证据：`handoff/runs/20260920T022824Z-firmware-offline-analysis/FINDINGS.md`。下一步：T03恢复入口调查与G03主机防复发；无需再次通电。

## 修正后的USB复测（2026-09-20，用户已确认通电）

用户确认在北京时间10:12:21–10:12:51的修正工具监听窗口内开机，仍循环重启、随后断电。102次有效设备树快照均有15个USB设备，未捕捉Sony。此前10:11:09–10:11:19窗口用户未开机，仅是未开机对照。没有发送相机协议命令，不能从本次采样推断永久无USB或硬件损坏。恢复未完成，安装/机身写入暂停。
证据：`handoff/runs/20260920T021221Z-passive-usb-retest/SESSION.md`。

## USB证据纠正与电源复位结果（2026-09-20）

用户报告官方通用电源复位无效。复核发现原连续采样命令ioreg -a -p IOUSB未带-l，不输出idVendor；以厂商ID筛选所得11次空列表无效，撤回基于它的无USB结论。原最后一次名称树快照当时未显示Sony，但不能替代持续检测。新版observe_usb.py使用-a -l，兼容单根字典/列表，缺属性报错；7项测试及15个现有USB设备的主机对照通过。尚未重新观察故障相机；恢复状态未知，写入暂停。
证据：`handoff/runs/20260920T020751Z-usb-evidence-correction/SESSION.md`。本纠正优先于下方旧结论。


## 重置方法核验（历史记录；用户随后报告无效）

核验Sony通用电源复位：取电池一分钟→无电池时开关ON→按快门30秒→开关OFF→装电池开机一次。不同于先前仅拔电池；尚未执行、无恢复结果。来源是通用电源故障支持文，不是安装后循环重启的已验证修复。A7R II出厂重置/初始化需菜单可用；目前无法进入。未找到官方不进菜单的本型号强制出厂重置组合键。
证据：`handoff/runs/20260920T015912Z-reset-research/SESSION.md`。


## 首次被动USB观察（历史结论已撤回）

**纠正：下述11次厂商筛选缺少必要属性，不能用于判断Sony设备缺席；原始记录保留，当前结果见顶部修正复测。**

单次被动USB观察：2026-09-20 01:53:37–01:53:47 UTC，11次ioreg快照均未列出Sony设备；用户随后确认采样时已经开机、仍反复重启，现已断电。11次快照未检测到Sony；采样间隔约1秒，不能排除间隔内短暂枚举。当前没有已验证可用的USB恢复通道。禁止重复安装或在未知通道上尝试卸载/刷写。不能据此断言USB永久不可用或硬件损坏。没有运行PMCA、发送模式切换或安装命令。
证据：`handoff/runs/20260920T015336Z-passive-usb/SESSION.md`。


## 离线故障调查更新

离线排查发现上游#433有同型号安装后循环重启报告，但没有已验证恢复。用户确认无既往语言/制式修改；禁用语言tweak恢复假设。APK ZIP/DEX基本检查通过，不能排除Sony资源/包管理兼容问题；安装结束sendEnd未执行，但不能认定根因。机身写入继续暂停。

证据：`handoff/runs/20260920T015104Z-offline-investigation/FINDINGS.md`。


> **暂停机测／故障未恢复（2026-09-20）：** 严重机身故障：首次0.4-probe安装进度100%后USB I/O失败；用户报告黑屏反复重启，断开USB、拔电池后仅装电池不插卡仍复现。因果机制未确定，不能判定硬件损坏或宣称可软件恢复。立即暂停全部机身通信、安装、升级及测试，保留证据；T03阻塞。
> 本警示优先于下方历史安装与操作步骤。证据：`handoff/runs/20260920T014513Z-boot-loop-incident/SESSION.md`。


工程仍为v0.6开发基线；相机Manifest **0.4-probe / versionCode4**；Studio软件原型0.2。ADR0011的原生持久颜色主目标与实时样张创作、宽幅/真实倍率要求均保持。


## 首次安装尝试（2026-09-20）

用户明确确认后，向ILCE-7RM2（用户菜单固件4.01）发送已验签0.4-probe开发APK；进入安装模式成功，上传/安装进度均到100%，随后等待最终回执发生USB I/O错误，进程退出1。安装结果待机身应用列表与启动确认，禁止把100%进度记为成功或自动重装。

证据：`handoff/runs/20260920T014014Z-first-install/SESSION.md`。本条取代下文历史“尚未尝试安装”；未修改固件或系统安全设置。

## 最新机身连接实测（2026-09-20）

A7R II实际MTP基础与扩展型号读取通过，model_code=0032828070。用户在机身菜单确认固件4.01（非工具精确读取）。PMCA原info重复初始化触发Access denied；单次包装会话查询成功，新增白名单只读适配入口与6项生命周期/反向测试。上游源码、系统安全设置均未修改。APK安装和启动仍未验证。

续接：`handoff/runs/20260920T013642Z-mtp-query/SESSION.md`。此前“无设备”仅为历史准备阶段结果。

## 固件与连接准备历史（2026-09-20）

官方中国ILCE-7RM2固件4.01的Mac包已下载至.local/firmware，267199906字节，SHA256 `a72f8e3ad329ac8fdb916e9db1a82b02f6d0c9a698c130658d6ab7a7a5a5a1ed`；DMG内部校验通过，未运行。官网仅列旧版macOS，未获得本Mac升级资格，下载不代表中文地区转换。

PMCA固定a82f5ba，独立Python3.12 ARM64 venv、libusb1.0.30、依赖冻结/归档已完成；帮助、后端加载、info与pip check实际通过。Sony设备枚举为空，尚无机身通信/安装。新增info-only入口`sh tools/macos/camera_info.sh`，拒绝附加参数。见docs/CAMERA_CONNECTION.md。没有改系统安全设置，没有写机身。

续接：`handoff/runs/20260919T225708Z-connection/SESSION.md`。T03的主机准备完成，仍等设备连接；下一步MTP查询型号/版本，不需先升级固件。

## 最新中文取景界面实现（2026-09-20，U04 / U03）

用户已选择第一款暗色大字方案，并确认顶部不能露出取景图。本轮已将该方向落入现有原生XML：顶部贴边、独立Surface区域、镜头/画幅/设置三个20sp按钮和明确焦点边框。设置保留尺寸实验、重启取景、完整诊断及返回；对话框复用实际读取的Sony键映射。拍摄状态机、单拍限制和Sony调用路径不变。

首页、取景页、图像自测的操作与提示集中为默认中文资源。诊断原始字段与合成测试靶仍保留英文；语言选择/英语资源和中文字形机测未完成，U03仍in_progress。Studio本轮未改。

本轮统一check通过：50项Node、65项工具/资源契约、44项Java（含10000随机几何）、3000组对照、14项Python参考及17个Android源语法检查。真实API10 SDK构建、DEX035/对齐/v1验签通过。最新APK：`build/android/20260919T160456Z-native-ui-apk3/CineVista-Probe-0.4-debug.apk`；SHA256：`bf6fdea4f0e449cc565bb3319375f87f3070298df1f104667f752cc4041ebd58`。首次资源构建因前向焦点ID引用失败，显式声明后成功；完整历史见`handoff/runs/20260919T160456Z-native-ui/SESSION.md`。

同源XML/样式/中文资源的浏览器布局预览已检查两种假设视口、选项独立切换、方向键焦点和设置开关。它不渲染真实相机画面。没有Android模拟器运行、相机安装或机测；不能据此确认实际屏幕尺寸、字体、Surface裁切与EVF。U02继续待原生预览环境接入。

## 最新用户语言与设计要求

已确认简体中文为默认产品语言，写入开发约定与相机UI说明。已核查Android多语言资源机制，推荐Linear暗色层级结合IBM信息结构，该段记录早期调研，现已按上方用户选定方案实现。U03负责实际中文资源化、语言偏好和字体验收；当前探针仍含英文，本轮仅规范/调研更新，无新APK或机测。

## 最新相机UI工作（U01）

首页从Java动态建控件改为API10 XML布局，MainActivity绑定原有六个动作。新增离线首页结构草图，直接读取同一XML；浏览器实际检查640×480/480×320假设视口、按钮提示和Tab焦点。不是Android精确渲染或相机截图。说明见`docs/CAMERA_UI_PREVIEW.md`。

`python3 tools/cv.py check`通过：50项Node、62项工具、44项Java、3000组对照、14项Python参考与17个源文件语法检查。`python3 tools/cv.py android`实际通过API10编译、DEX035、对齐、v1验签与包检查。

本轮APK：`build/android/android/CineVista-Probe-0.4-debug.apk`；SHA256：`a8107f3f4938e00fc9454384b03f63910741f1f6fcc6488c675c25e240b92ffb`。原始首包与历史日志保留。

U01完成；U02待接入Android Studio/原生模拟器预览，本轮没有安装IDE/模拟器或新增SDK。相机生命周期、取景、原生持久颜色能力状态不变，仍无机测。续接：`handoff/runs/20260919T151319Z-camera-ui/SESSION.md`。

## 最新工程治理（G01/G02）

已在现有工程建立README/说明书/文档制度/索引、单一任务板生成TODO、Gitee协作模板与ADR0013。架构检查补齐全限定类名绕过、portable IO引用Android、生产层依赖桌面/测试模块及编译顺序，残余Backup全禁改为同一受审查profile校验。统一check和真实SDK构建通过；详情见`docs/ENGINEERING_AUDIT.md`。

本地Git main已提交并推送到`https://gitee.com/OWNER/REPOSITORY.git`。首个提交`bf1cea0aa52b717a698e9296096af270fc46d005`的远端读回与本地一致。用户确认仓库私有并提供Git身份；API可见性未独立读回。Gitee CI/保护规则仍未启用，.github仅保留可选。G01完成；G02的仓库同步已完成，远端CI/保护配置仍待接入，不阻塞T04主机研发。

最新推送续接：`handoff/runs/20260919T145923Z-gitee-push/SESSION.md`。

治理续接：`handoff/runs/20260919T144316Z-engineering/SESSION.md`。此前Mac首轮接手记录保留，不重新标日期/设备结果。

## 首轮接手已完成

- T00：原始MANIFEST 190/190、交接MANIFEST 206/206通过；接手时无Git目录，无基线偏离。修改前完整源码快照与逐文件hash已保存，历史evidence没有覆盖。
- 主机实测：Apple M4 Pro、24 GiB、macOS27.0（26A428）。初始无可用JDK/SDK；现已在.local隔离配置Temurin17.0.20.1+1 ARM64、Google官方API10 r02、Build Tools30.0.3。官方分发校验通过。
- T01：**第一个完整检查通过的开发APK已实际生成**。真实API10类型编译、资源、DEX035、对齐、v1签名（min/maxSDK10）、包名/版本/权限/定义类检查均通过。旧系统图标导致首次badging失败，已换自有API10图标；权限检查保留官方工具的明确隐含读存储语义。
- T02必要过渡：独立run-id证据、禁止覆盖；构建profile精确JNI/源码例外白名单（生产为空）；旧未实现断言转历史fixture，真值需匹配报告；证据路径/hash/机型/固件/构建/计划绑定，启用可选功能也受发行门禁约束。测试覆盖篡改、空文件、越界路径、伪造真值、额外库/错误ABI/未审查源码。详见ADR0012。

APK：`build/android/sdk-complete/CineVista-Probe-0.4-debug.apk`（30726字节）  
SHA256：`d11e4da7e863ba8e8f534d99b605f96486fe9e2d804968806199895257515bac`  
签名证书SHA256：`5e1b4abe5a643faaf1bf3b947698231158059b0b594c9355479be376344caa87`

## 验证范围

`python3 tools/cv.py check`通过：50项Node、46项工具/契约、44项Java（含10000随机几何）、3000组Java/Python对照、14项Python参考、17个Android源语法解析。真实SDK构建另外执行，不能与语法解析混为一谈。实际Node为26.8.2，不声称Node22/JDK21矩阵已跑。

`release-check`仍退出2：14项必需门禁unknown、完整工具链资格false。开发APK不代表正式发行。证据一致性检查也不能鉴别编造的人工观察，仍需实际样片审阅。

## 未完成与下一步

USB只读清单未发现Sony设备。**没有安装APK、没有任何机测、没有读取这台A7R II固件/SDK、没有持久化驱动、相机CVL/CVP解析器或原生预览标定。** 运行时矩阵/反挤压/EVF也未验证。Studio已有软件能力保持，未进行本轮Safari交互复测。

T02仍in_progress：可选API16隔离、JNI/ELF/链接与来源资格、逐门禁专用取证约束和人工审阅流程待后续。当前生产profile为无JNI的java-probe。

下一任务T03：固定审查Sony-PMCA-RE及依赖，用户连接A7R II后先只读info，再在知情安装范围内测试基础探针。设备未到位时继续T04严格导入器/不可变计划与JS-Java共享向量，不改写颜色未知状态。

## 续接与证据

本轮记录：`handoff/runs/20260919T141703Z/SESSION.md`；相机集中操作：`handoff/DEVICE_TEST_CARD.md`。工具链来源/hash：`config/toolchain.lock.json`和`third_party/TOOLCHAIN_DECISION_20260919.md`。

本地重跑：`source .local/env.sh`，然后`python3 tools/cv.py check`或`python3 tools/cv.py android`。新调用自动分配新证据目录；不要重复使用已写入的CINEVISTA_RUN_DIR。首轮未执行远端动作；现已按用户授权私有推送源码，未公开发行、上传照片/密钥或更改系统安全设置。
