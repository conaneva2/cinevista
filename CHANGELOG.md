# 2026-10-25：命令DMA错误通道与4.01配置交叉核验（R34）

固定Altera官方硬件库源码版本，补充0x7c0/0x7d0、0x780 bit8和0x720完成事件的参照。两机4段原指令一致；恢复的4.01配置排除直接照搬出错停队列默认值。14项静态核查通过，无模型改动或新增客体测试。BOSS定向搜索未取得匹配载荷，上游未变不重复取差异。

# 2026-10-25：原状态消费指令隔离执行与阈值核验（R33）

追清软件警戒阈值来源，区别于ECC硬件强度；使用原ELF重定位和原getter/返回表，在隔离ARMv7环境执行两机38项状态分支用例。26项静态检查通过；保留实验工具初始化失败记录。无固件/模型变更，无新固件启动、NAND传输或挂载通过。补充Denali配置代际的公开旁证及A6000上游21提交/86路径增量覆盖范围。

# 2026-10-24：extra恢复标志与DMA参数追踪（R32）

确认bit1/2实际恢复消费，排除将分区记录的+6/+7误认extra字段；全局用途仍保留未知。对齐两机整页/分段DMA构造；新增旧Spectra对照及拒绝直接移植依据。53项静态核查、5项CPU暂停的控制器测试通过，无模型改动或新固件启动。BOSS、物理ECC、GPU与Android验收仍未通过。

# 2026-10-24：追清extra消费者与ECC错误归一化（R31）

以两机原模块确认0x40类逻辑块/LTU/循环代次字段、独立0xAA标记，以及单页和批量读取不同的ECC返回规则。挂载选择器同时检查坏块列表、逐项状态和extra内容；返回0不能单独证明成功。39项静态取证检查通过；QEMU/固件未变，无新增启动。A6000上游新增8提交/189文件未提供匹配BOSS；物理ECC与完成生产机制仍待证。

# 2026-10-24：追清extra构造、ECC状态与DMA等待语义（R30）

增加4.01/A6000原代码对照：共享8字节extra setter、0x40类字节布局、不同对象偏移、op7/op15状态输出，以及op16/op17仍依赖BOSS的证据。明确状态字节0并非独立成功条件，原DMA消费者会二次检查描述符。新增Cadence对照并记录不可移植的计数位/flags偏移差异。54项静态核查通过；本轮无模型变更或新启动，物理ECC与BOSS载荷仍缺。

# 2026-10-24：NAND配置保存与严格ECC边界（R29）

修复四项原驱动会保存/恢复的配置寄存器在模型中丢失；新增可选strict-ecc，在不支持的纠错传输发生前终止，避免产生假完成。原代码前后启动对照、55项证据检查及六组控制器测试通过，保留两次观察器失败。补充BOSS op5/op8布局、缓存/输出合同和Denali新旧错误位区别；原生挂载仍受BOSS执行端阻断。公开补充此前复位实验补丁与本轮配置补丁，均不含固件。

# 2026-10-24：恢复匹配启动配置并回放初始化（R28）

从4.01 WBI经原页表恢复nand参数副本，核对88,184字节非重定位代码；A6000与4.01共同确认坏块扫描、六条保留块生成及42组直接配置写入。一轮隔离启动由原驱动生成与快照一致的52字节设备信息，五个停点完成，随后主动停止。53项核查通过；没有BOSS载荷、存储挂载或Android新验收。

# 2026-10-23：BOSS合同细化与虚拟启动验证（R27）

恢复18类操作归属、CPU侧结果转换和两代PBI布局差异；76项静态核查。两次隔离QEMU启动确认默认复位超时和条件配置下BOSS超时，新增运行时坏块表指针ffffffff证据。保留首版观察器盲读E14失败；修正观察器后五个原指令停点验证通过。没有宣称返回0等于成功，没有新增Android/APK验收。

# 2026-10-23：A6000存储协议交叉取证（R26）

新增两份原厂启动驱动的离线比较，确认共同BOSS接口及4.01专有PBM版本检查；新增SA容器格式核验和社区增量去重。43项检查通过。提出完整BOSS协议模型的取证候选，未修改执行模型、原固件或相机。GPU完成规则仍缺，未新增Android/APK验收。

# 2026-10-23 BOSS候选来源与完整目标阻断审计

- 将两处WBI命中核对到原resources.arsc条目偏移表，将一处ODEX命中核对为proto_id字符串索引；其余弱候选保持未知，不作程序加载。
- 26项核查通过；当前11项完整要求仍缺GPU执行完成、原生窗口/Android和持久安装。没有活跃实验等待，连续GPU/BOSS缺口未解除。
- 更新资料和恢复工作条件；没有模型、固件、相机状态或断言变更，原始字节与日志只本地留存。

# 2026-10-23 MA缓存入口与调试上下文核验

- 原sysfs/kallsyms、模块偏移和内核态指令读回确认ma_cache_ctl地址，补全R23失败观察；用户态E14不能再被解释为地址错误或模块缺失。
- 限定首提交窗口内该入口零命中；32字节命令与128字节对象物理RAM读回吻合。两轮客体、50项证据核查通过，IRQ76仍0。
- 只改取证工具和研究文档；原固件及模型保持，完整Android/APK目标没有缩小或标完成。

# 2026-10-23 研究手册完善与失败记录补齐

- 五份手册补充易读术语、R23提交/等待观察、缓存入口核验失败及接续方法；修复证据索引表格，更新已被R22推进的窗口服务端表述。
- 明确客体检查完成与缓存观察器失败的区别，保留E14与零命中的解释边界；原始记录仅本地保存。
- 此次文档收尾没有新客体运行、模型或固件修改及相机操作；统一工程检查与公开备份核验独立记录，不作为Android或APK验收。

# 2026-10-23：原生 BufferManager 服务端与启动顺序

- 固定原libObj的注册回调、BufferFuncThread、六项跳表及命令1/2锁处理，明确其回复范围不包括GPU完成。
- 一次只读观察先命中GPU首提交，另外三个服务端断点在此前未命中；最终检查完成、IRQ76仍为0。39项证据与保护核查通过，无固件/模型修改或相机操作。
- 更新研究手册及接续任务，继续保留完整Android/APK环境的未完成状态；原始证据仅本地留存。

# 2026-10-23：MA 映射和窗口协议证据补充

- 补充 R21：一次原生进程映射观察，与 128 字节对象和首个命令包的物理读回交叉核对；原 stream 页属性及 grm_ma cache 方向得到原库和官方内核支持。
- 明确窗口共享管理区、客户端 lock/unlock 请求及私有格式 `0x158` 的参数来源；服务端、像素布局和 GPU 完成条件保持未知。
- 45 项证据与保护检查通过；未改变硬件模型、原固件或相机状态，Android/APK 无新增验收。五份研究手册同步更新，原始证据仅本地保留。

# 2026-10-23：研究手册与公开备份更新

本地与公开副本工程检查通过，首个同步提交 `540e073` 已读回核对全部207个公开文件及匿名提交身份。

新增五份相互链接的研究文档，汇总应用事故、录像链、Linux/Android实验、GPU/BOSS及同代机型对照；提供20组证据编号、原文件摘要、固定来源和接续验收。补充已修订的早期结论，保留未验证边界。此次为文档与证据整理，没有新GPU执行、Android/APK验收或相机操作。

# 2026-10-23｜公开源码备份与状态核实

## 2026-10-23：整理公开仓库开发资料

- 移除内部工具入口、执行提示与专用交接文档，公开协作说明统一引用 CONTRIBUTING.md 和产品文档。
- 同步文档索引、文件清单和规范检查要求；产品实现、研究限制和第三方许可保持原有含义。
- 本地工具链下统一检查通过（退出码 0）；本次仅更新当前源码树，未改写已有提交历史。

- 经许可与隐私初筛的212个文本文件已发布到 GitHub；远端文件树与本地审核版一致，提交使用匿名邮箱。
- 补充原存储探针的实际结果：冷初始化记录 mumin_devif_init 超时和 boss_init 返回 -10003；完整 Android/APK 环境仍未通过。

## Unreleased｜GPU诊断分派与公开记录对照 — 2026-10-23

- 静态解码原grm_gles的18个ioctl分支，并以原具名库封装核对软件signal与硬件IRQ等待的区别；不将空reset函数当硬件协议。
- 核对两个新社区来源：拒绝常量/固定成功的替代实现；A6000公布日志的SMAPH-S30与IRQ76只能作同系列交叉证据，不能关闭本机完成时序缺口。
- 无新GPU执行/Android进展、客体运行或相机操作，保存有界审计与继续工作的缺项。详见`handoff/runs/20261023T022306Z-sugilite-diagnostics/FINDINGS.md`。

## Unreleased｜原DMP调试符号与空同步提交 — 2026-10-23

- 从原4.01的DWARF确认四条GPU命令名称，解析128字节错误纹理的分配/纹理/虚读三个引用；未把纹理大小当虚读长度。
- 原客体只读断点实际确认首次计数0→4、wait_done=1；两份GLES的293项枚举一致。端口传播和完成IRQ仍缺合同，未新增伪完成/固件补丁；Android/APK仍未通过。
- 新增可复跑语义提取及只读跟踪记录，用户的模拟器持续目标保持进行中。无相机操作、新APK或大下载。详见`handoff/runs/20261023T015609Z-sugilite-semantics/FINDINGS.md`。

## Unreleased｜sugilite首个命令构建与取指前端 — 2026-10-23

- 原CPU写观察和构建函数闭合单值包格式、8字节计数、128字节缓冲初值和物理地址编码；未确认其写回用途，不伪造完成。
- 新增显式启用、独立构建的QEMU取指解包观察器；4组前端及6组控制qtest通过，原固件真实提交三次被解析，仍停在GPU等待/原超时重试。
- DMA、完成IRQ、原生窗口/Android仍未完成。保留模板支线、探针地址守卫及装载基址变化导致的失败；22项原输入和两个旧二进制不变。无相机操作/新APK/大下载。详见`handoff/runs/20261023T012044Z-sugilite-command/FINDINGS.md`。

## Unreleased｜sugilite控制寄存器模型与GPU超时链 — 2026-10-23

- 官方CXD90014源码与原4.01驱动交叉核对，新增可选QEMU控制寄存器实验模型，独立构建；原上电断言实际通过、grm_gles加载返回0。
- 原GPU提交、完成等待、超时复位和重试已动态对应；无GPU执行/写回/IRQ伪造，窗口与Android桌面仍未通过。初始值/时序未知部分明确保留。
- 6组qtest、13项证据一致性通过；22项原输入和旧QEMU不变，旧UI默认配置不变。预告后仅下载50.4 MiB官方包，无相机操作/新APK。证据：`handoff/runs/20261023T004916Z-sugilite-model/FINDINGS.md`。

## Unreleased｜输入/字体依赖修复与 sugilite 上电阻塞 — 2026-10-23

- 恢复原uinput节点，D keyboard实际注册；原版字体列表及六字体按原路径恢复，TextRM初始化返回0并通过原断言。
- Appframework推进到窗口表面创建失败；原grm_gles加载在sugi_hw.c:221触发断言，记录实际MMIO写入/读回和QEMU缺设备映射。保留分组正反对照，没有假成功或断言补丁。
- 原生窗口、Android桌面和APK仍未就绪；操作台默认配置保持上轮实验。22项原输入及QEMU哈希不变，无相机操作、下载/安装或新APK。证据：`handoff/runs/20261023T002402Z-sugilite-window/FINDINGS.md`。

## Unreleased｜恢复原日志配置与虚拟相机开发操作台 — 2026-10-23

- 从官方4.01 WBI快照恢复3372字节ulogio.bin，验证FAT目录项、TLV、保留内存和原logaddr；原日志驱动与DMM实际成功，最初生成工具仍未知。
- 补原stream驱动/节点后，gl_common创建返回0并通过原断言；窗口服务开始初始化，后续图形/Appframework仍报原错误，不宣称Android/APK通过。
- 新增本地相机背面操作台，连接固定限时QEMU实验，显示实际驱动状态和错误。固定RAM/原保留区及设置配额；CPU时间/完整NAND未等效。未就绪APK入口禁用。
- 新增7项主机边界测试及浏览器实际启动/停止/导航验证。用户优先级改为虚拟模拟器，详见ADR0016。无机身操作、固件代码补丁、新APK或大文件下载。

## Unreleased｜gl_common接收端与DMM启动依赖 — 2026-10-23

- 读取原程序真实返回值，确认gl_common同步消息因缺grm_ma回调返回-1020；补原驱动后传输成功，但DMM缺失使创建返回-9999。未跳过断言。
- 对照原启动表逐项补DMM及原始配置，定位更早的osal_ulogio记录区依赖；调试确认/setting/ulogio.bin打开返回ENOENT，当前更新包未提供该输入。
- 缩小仅原生服务的实验根，保存正反对照与失败日志；核心库继续初始化仍未通过，无相机操作、新APK、下载或原固件改写。详见`handoff/runs/20261022T225823Z-gl-common/FINDINGS.md`。

## Unreleased｜A7R II分支对照与原生备份服务启动 — 2026-10-22

- 对照固定同机型分支，新增电源连线/片选、SIO3与BOSS中断应答测试及两组Android启动快照；未发现当前IRQ170堵塞，未照搬错误绕过补丁。
- 审计完整逻辑分区与压缩数据边界；加入原版原生服务程序及默认设置实验，恢复备份预留内存并使用原版文件加载参数，backup.ko加载成功。
- 原版bootin调度后libObj.so实际加载，定位到dmp_allocator_lib_init的gl_common内存池断言；保留失败，不绕过。
- Android桌面、窗口服务、APK安装与/data持久性仍未完成；原固件/QEMU二进制不改，未操作相机。详见`handoff/runs/20261022T100302Z-a7rii-board-alignment/FINDINGS.md`。

## Unreleased｜NAND持久写入与Android服务对照启动 — 2026-10-22

- 修补独立QEMU NAND后端，保留修补前失败对照；整页/附加区、扇区和擦除跨全新进程读回通过。尚非Linux文件系统或Android /data持久性验收。
- 实际运行4.01 Android init/system。确认缺OSAL时显示库空指针崩溃；加载原版通信驱动后进入窗口服务连接及Sony JNI消息等待。原生NAND仍因devctrl初始化失败而无法挂载。
- G08保留进行中，未运行APK或复现事故，无机身操作、新APK或大文件下载。报告：`handoff/runs/20261022T091300Z-qemu-storage-android/FINDINGS.md`。

## Unreleased｜定制QEMU与4.01最小Linux实际启动 — 2026-10-22

- 在项目本地准备pkgconf/libmad及固定子模块，构建Sony QEMU 5.1.0；原生TCG运行失败后采用TCI及非EXEC字节码缓存补丁，没有修改原内核。
- 修正共享串口mux配置，实际进入4.01 Linux/BusyBox；独立启动验证guest命令、tmpfs读回和Binder/ashmem注册，保存可复跑入口与失败过程。
- 当前无持久分区，未运行Android/更新系统/APK；NAND持久性、原事故和真实硬件能力仍未验证。下载前已告知，未操作相机或发布任何固件。证据：`handoff/runs/20261022T084735Z-qemu-first-boot/FINDINGS.md`。

## 2026-10-22 SDF逐帧生命周期与电脑仿真调研（离线）

## Unreleased｜QEMU启动材料与持久存储缺口 — 2026-10-22

- 在4.01主系统中确认裸ARM内核、ext2初始根与Android chroot启动材料，准备独立最小Linux用户态候选并完成文件层回读；尚未启动QEMU。
- 追到Sony kemco参数入口，核对CXD90014加载地址；发现该QEMU NAND写/擦未持久实现，不能据此验收安装与重启保留。
- 区分正常Linux最小候选、缺失的专用更新系统、完整Android与事故状态。只取约308 KiB公开源码，未下载50.4 MiB官方内核源码包或安装工具，未操作相机。证据：`handoff/runs/20261022T082324Z-qemu-boot-readiness/FINDINGS.md`。


## Unreleased｜安装启动离线方法实验环境 — 2026-10-22

- 新增按67个本地输入SHA-256锁定的有限固件方法回放器，记录指令、外部替身、故障注入和JSON快照；复用aapt、baksmali、PMCA真实安装循环与现有Python环境。
- 24个案例覆盖图标强转、安装进度/最终回执、安装标记与Resume(8)条件同步；未运行完整APK或Android，也未重现实体相机重启或验证恢复。
- 社区资料调研找到CXD90014的QEMU板型及RX100M5更新系统测试；保留A7R II正常系统/专有硬件缺口。未操作相机、无新APK，事故暂停不变。见 `docs/INSTALL_BOOT_LAB.md` 和ADR0015。


官方4.01静态确认SDF与MC共用MMC队列0061003c；SDF消费输入票据并返回新票据，MC分离图像/YC描述释放且有定时释放和Vsync延迟回收。未找到现成SDF逐帧回送录像桥接，吞吐仍unknown。整机模拟缺专用板级/硬件模型；优先候选为按固件约束的安装启动兼容环境，尚未建成。原事故APK重检仍因XML图标拒绝exit2，不是整机故障复现。未操作相机、未改产品代码/固件、无新APK，保留CAMERA_WRITE_HOLD，T11仍blocked。
证据：`handoff/runs/20261022T073608Z-sdf-lifecycle-emulator/FINDINGS.md`。

## Unreleased｜录像动态连接与DSP几何离线续查 — 2026-10-22


## 2026-10-22 实际录像接收端与SDF缩放后端（离线）

- 解析SCALAR_MOVIE_REC固定拓扑、MovieRecorder→MovieEncoder主路端口请求，并保留VEF/TCUB和编码模式条件分支。
- 贯通独立宽高参数到ObjScalar3017、HAPI201及SDF图像票据任务；确认标准YC输出与完成机制，尚无连续录像桥接或实时性能证明。
- 仅本地固件调查和文档，未操作相机、未改产品代码/固件、无APK，T11仍blocked。证据：`handoff/runs/20261022T034123Z-movie-peer-scale-backend/FINDINGS.md`。

官方4.01离线确认录像槽6对应SFR(type0,dir2,no1)，上层对象pinNo3映射到该端口；已追清嵌套连接消息、运行时对端写入与发送读取，但目标录像模式的实际编码对端四元组仍未闭环。原生SCALE/resizeTrim接受独立宽高，不能直接等同于SA录像插件；所查VFX是Transfer，尚无自定义DSP反挤压与实时性能证明。T11仍blocked；未操作相机、未改产品源码/固件、无新APK，保留CAMERA_WRITE_HOLD。
证据：`handoff/runs/20261022T032031Z-rec-pin-dsp-geometry/FINDINGS.md`。

## Unreleased｜原生录像编码前反挤压调查 — 2026-10-22

## Unreleased｜DSP效果录像通道离线追踪 — 2026-10-22

官方4.01离线已把DSP插件路径5追到0x3039→SFR路径0x32→EffectMovieRec；SA输出经VFX形成画布，路径0x32将该画布标识/句柄替换进RecPin并交出。原生McPinMain→McAvcEncVfm图像接收实现也已定位，但RecPin输出槽6的动态连接到目标编码模式尚未闭环，不能宣称反挤压录像可用或硬件不可行。自定义几何处理、格式/帧率与恢复能力仍未证明；未操作相机、未改产品源码或固件、无新APK，T11仍blocked。
证据：`handoff/runs/20261022T023458Z-dsp-movie-chain/FINDINGS.md`。

官方4.01离线确认Sony录像源仅接受0/1，prepare/start走SDCom；所查标准Camera HAL录像入口直接返回错误。StreamBuffer为ES及管理区契约，未找到裸帧输入。DSP预览插件record选项真实选择路径5并进入SCALAR_CAMERA_PATCH，但到原生编码输入尚未闭环；不能由入口限制断言硬件不可能。软件H.264实现存在，实时性能未知，不作为当前主方案。未操作相机、未改设备代码、未生成APK，继续暂停。
证据：`handoff/runs/20261022T021116Z-video-encoder-feasibility/FINDINGS.md`。

## Unreleased｜实时反挤压离线可行性 — 2026-10-22

结合官方4.01实际ODEX/native实现与当前源码，确认SmartRemote存在CameraSequence取JPEG帧链；普通预览特殊格式仅分配描述信息，不能把改窗口尺寸或TextureView矩阵当成已实现反挤压。保留B路径优先候选，性能、权限与LCD/EVF仍未实测。按用户决定前置T11门槛，保留设备暂停；未改变设备代码或生成APK。
证据：`handoff/runs/20261022T014755Z-desqueeze-feasibility/FINDINGS.md`。

## Unreleased｜更新环境恢复可行性 — 2026-09-27

离线确认固定PMCA包含ILCE-7RM2更新载荷，型号与官方4.01匹配，主体firmware段0字节、带updater模块；但USB入口仍依赖已可通信设备，源码自动可写挂载设置区，应用数据恢复涉及双备份与同步。尚未验证故障时独立入口或可靠回滚；未操作机身、未生成新固件/APK，继续暂停机身操作。
证据：`handoff/runs/20260927T053659Z-recovery-feasibility/SESSION.md`。

## Unreleased｜充电HID证据核验 — 2026-09-20

用户Windows11只读记录确认：无电池、OFF、USB连接时054C:0994，Class03/00/00，USB Charger，状态OK；采样只记录一次出现。已确认充电HID枚举，不等于MTP/MSC/恢复接口。源码核验尚无可验证充电HID到恢复模式的转换路径。
证据：`handoff/runs/20260920T052255Z-charger-interface-review/SESSION.md`。

## Unreleased｜启动图标打包门禁 — 2026-09-20

G03新增最终包启动图标/组件契约：复用aapt30.0.3解析编译清单、全部图标配置并解码PNG；拒绝XML/别名/系统图标、NinePatch、额外组件及显式process/persistent。11项测试通过；事故原APK拒绝exit2，当前源码构建在资源预检按预期停止exit1。未替换生产图标、无新可安装APK、无机身操作。
证据：`handoff/runs/20260920T041708Z-launcher-gate/SESSION.md`。

## Unreleased｜恢复案例适用性核验 — 2026-09-20

引用来源存在语言解锁关闭后恢复的用户自述，但前提为已有解锁设置且能进Mass Storage；不符合目前已知安装史及USB表现。DPReview两帖403，浏览器超时，正文未读到。未改变机身操作暂停。
证据：`handoff/runs/20260920T040707Z-user-source-review/SESSION.md`。

## Unreleased｜控制台设备路由核验 — 2026-09-20

离线从原始initrd确认/dev/ttycons为指向ttyAM0的符号链接，内核含AMBA/PL011驱动字符串；init根据/proc/cmdline中的console=ttyAM0选择launch_shell参数。未确认物理针脚、电平、实际启用或故障日志；不是USB恢复已可用。
证据：`handoff/runs/20260920T035712Z-console-routing/SESSION.md`。

## Unreleased｜原生输入与早期控制台调查 — 2026-09-20

进一步确认Sony输入服务通过uinput转发按键，初始化/资源状态切换不能等同于持续采样所有已按住按钮；安全模式物理触发仍未证实。早期init的forced-senser检查读取机内文件，非已发现的按键/SD卡入口；另定位独立于Android的控制台程序及设备路径，物理接入未验证。
证据：`handoff/runs/20260920T035024Z-input-bridge-analysis/SESSION.md`。

## Unreleased｜安全模式调用链核验 — 2026-09-20

使用同固件libdvm真实22项内联表与仅改容器版本标记的离线分析副本，解析出ServerThread→detectSafeMode→enterSafeMode静态调用链；关键方法无解析占位错误。InputServant存在uinput及默认映射，但物理按键/早期持键状态/故障进度未闭环，仍不能给出可靠安全模式操作卡。
证据：`handoff/runs/20260920T034308Z-safe-mode-callchain/SESSION.md`。

## Unreleased｜启动路径调查与USB全ID记录 — 2026-09-20

离线确认4.01保留安全模式检测方法，但启动调用链有Sony优化字节码解析缺口，不能据此给出按键恢复步骤。ADB脚本/属性存在不等于对外可连接。修正被动USB记录范围：追加全部VID/PID及可用的数字端口位置，不再只依赖Sony厂商筛选；新增3项反向测试通过，未重新通电。
证据：`handoff/runs/20260920T033623Z-boot-path-analysis/SESSION.md`。

## Unreleased｜恢复入口分级 — 2026-09-20

继续离线核实恢复入口：官方4.01镜像包含android_console.sh及启动adbd的配置，但不证明故障机暴露ADB、可连入shell或可卸载应用。未找到已验证A7R II安全模式按键；搜索到的Sony安全模式说明适用于Xperia手机。
证据：`handoff/runs/20260920T033316Z-recovery-entry-triage/SESSION.md`。

## Unreleased｜上游故障Issue复核 — 2026-09-20

通过GitHub只读API筛选478条open Issue标题/正文，并读取12条重点帖完整评论。#433评论确认A7RM2，安装中断后循环重启且USB来不及连接，未报告软件恢复；#702安装APK后OFF仍重启与本机相似。#488提供A6000特殊15针接口读取启动日志线索，尚未验证适用于A7R II。
证据：`handoff/runs/20260920T032059Z-upstream-issue-review/SESSION.md`。

## Unreleased｜厂家恢复工具检索 — 2026-09-20

确认A7R II厂家维修手册使用Adjust Station及本型号Adjust Manual，但未证明黑屏无USB时可强制重刷。公开4.01升级器要求USB Mass Storage，已有4.01按官方流程结束。未找到可验证的本故障救砖包；无机身操作。
证据：`handoff/runs/20260920T031004Z-manufacturer-recovery-research/SESSION.md`。

## Unreleased｜安装/断线因果复盘 — 2026-09-20

用户确认仅电池、USB已拔掉时，拨到OFF后仍重复重启动作数次。复核原始命令/报错及官方4.01：Installing 100%在正常路径对应机身安装器成功回调后的通知，但结束握手未确认；错误在GetProxyMessage数据阶段返回后读取PTP响应时，未保存数据体，不能断言机身未发完成消息。APK传输/落盘/状态收尾不完整与新资源触发系统兼容故障继续并列调查。Sony安装器会尝试创建安装标记，恢复分支会同步应用，因此未刷固件不能推导未改变系统维护的状态。无新增机身操作、无恢复结论。
新增离线SPK往返、进度100%后异常/完成对照及PTP数据阶段后响应失败对照；均不代表相机恢复。记录一次性USB包装与异常回退缺口。证据：`handoff/runs/20260920T024526Z-install-forensic-review/SESSION.md`。

## Unreleased｜启动器图标兼容性调查 — 2026-09-20

官方ILCE-7RM2 4.01固件已在Mac离线解包。启动器IconCache.cacheLocked在loadIcon后无保护地强转BitmapDrawable；原安装APK的图标是XML layer-list，存在具体类型不兼容。该静态缺陷是循环重启的重要嫌疑，但缺相机崩溃日志与恢复验证，不能宣称已确认根因或硬件损坏。原APK继续隔离，没有生成或安装修正版。
离线工具/来源、局限及恢复诊断说明：`handoff/runs/20260920T022824Z-firmware-offline-analysis/SESSION.md`。当前操作卡已改为故障暂停，旧卡归档。

## Unreleased｜故障相机被动USB复测 — 2026-09-20

用户确认在北京时间10:12:21–10:12:51的修正工具监听窗口内开机，仍循环重启、随后断电。102次有效设备树快照均有15个USB设备，未捕捉Sony。此前10:11:09–10:11:19窗口用户未开机，仅是未开机对照。没有发送相机协议命令，不能从本次采样推断永久无USB或硬件损坏。恢复未完成，安装/机身写入暂停。
证据：`handoff/runs/20260920T021221Z-passive-usb-retest/SESSION.md`。

## Unreleased｜官方固件留存与MTP准备 — 2026-09-20

## USB证据纠正与电源复位结果（2026-09-20）

用户报告官方通用电源复位无效。复核发现原连续采样命令ioreg -a -p IOUSB未带-l，不输出idVendor；以厂商ID筛选所得11次空列表无效，撤回基于它的无USB结论。原最后一次名称树快照当时未显示Sony，但不能替代持续检测。新版observe_usb.py使用-a -l，兼容单根字典/列表，缺属性报错；7项测试及15个现有USB设备的主机对照通过。尚未重新观察故障相机；恢复状态未知，写入暂停。
证据：`handoff/runs/20260920T020751Z-usb-evidence-correction/SESSION.md`。本纠正优先于下方旧结论。


## 2026-09-20 故障后被动USB检查

用户随后确认采样时已经开机、仍反复重启，现已断电。11次快照未检测到Sony；采样间隔约1秒，不能排除间隔内短暂枚举。当前没有已验证可用的USB恢复通道。禁止重复安装或在未知通道上尝试卸载/刷写。 仅读取Mac设备树，未运行任何PMCA命令。


## 离线故障调查更新

离线排查发现上游#433有同型号安装后循环重启报告，但没有已验证恢复。用户确认无既往语言/制式修改；禁用语言tweak恢复假设。APK ZIP/DEX基本检查通过，不能排除Sony资源/包管理兼容问题；安装结束sendEnd未执行，但不能认定根因。机身写入继续暂停。

证据：`handoff/runs/20260920T015104Z-offline-investigation/FINDINGS.md`。


> **暂停机测／故障未恢复（2026-09-20）：** 严重机身故障：首次0.4-probe安装进度100%后USB I/O失败；用户报告黑屏反复重启，断开USB、拔电池后仅装电池不插卡仍复现。因果机制未确定，不能判定硬件损坏或宣称可软件恢复。立即暂停全部机身通信、安装、升级及测试，保留证据；T03阻塞。
> 本警示优先于下方历史安装与操作步骤。证据：`handoff/runs/20260920T014513Z-boot-loop-incident/SESSION.md`。


## 2026-09-20 首次授权机身安装尝试

用户明确确认后，向ILCE-7RM2（用户菜单固件4.01）发送已验签0.4-probe开发APK；进入安装模式成功，上传/安装进度均到100%，随后等待最终回执发生USB I/O错误，进程退出1。安装结果待机身应用列表与启动确认，禁止把100%进度记为成功或自动重装。


## 2026-09-20 MTP机身查询

A7R II实际MTP基础与扩展型号读取通过，model_code=0032828070。用户在机身菜单确认固件4.01（非工具精确读取）。PMCA原info重复初始化触发Access denied；单次包装会话查询成功，新增白名单只读适配入口与6项生命周期/反向测试。上游源码、系统安全设置均未修改。APK安装和启动仍未验证。


- 本机下载索尼中国ILCE-7RM2官方4.01 Mac包，记录来源/大小/SHA256并通过DMG校验；未执行升级。
- 隔离配置固定提交PMCA与Python依赖，实际加载ARM64 libusb；尚无设备。
- 增加固定info入口及连接说明、依赖锁和更新后的操作卡；未安装驱动或改安全策略。

## Unreleased｜中文大字取景页 — 2026-09-20

- 已确认的暗色大字方案进入现有API10 XML：贴边标题、独立Surface取景区、三个大字控制及紫色焦点。
- 首页/取景/图像自测操作提示集中到默认中文资源；原始诊断字段不改协议语义，尚无语言切换。
- 工程实验收进设置，保留单拍与未验证提示；对话框复用Sony运行时导航键映射。
- 同资源浏览器结构预览增加取景页；真实SDK构建与验签完成，无相机安装或机测。

## Unreleased｜中文与设计参考约定 — 2026-09-19

- 按用户要求确立中文默认语言，记录旧Android多语言与字体验证边界。
- 评估指定设计库的Linear/IBM/Apple参考，提出相机与Studio分场景取舍；未实施视觉改版。
- 实际中文资源化单列U03，不把规范当汉化完成。

## Unreleased｜相机首页布局解耦与结构预览 — 2026-09-19

- 首页改由API10 XML布局定义；MainActivity绑定原有六个动作，Sony与捕获生命周期不变。
- 增加从相同XML生成的离线结构预览，可切换假设视口；不模拟Sony取景或原生控件外观。
- 增加共享布局/动作绑定、文本转义和不支持节点拒绝检查；记录官方原生预览路线。
- 未安装Android Studio/运行模拟器；无新增机测或原生颜色资格。

## Unreleased｜Gitee首次私有同步 — 2026-09-19

- 用户确认目标仓库私有并提供Git身份；仅本仓库配置，不更改全局设置。
- 源代码与文档已推送OWNER/REPOSITORY的main，初始提交bf1cea0的远端哈希读回一致。
- SDK、密钥、构建产物、当前及历史原始执行日志留本机；提交源代码、制度文档和合成测试素材。
- 远端CI/分支保护仍未验证，不以Git推送代替设备认证。

## Unreleased｜工程治理 — 2026-09-19

- 新增单一task-board生成的TODO、用户说明书、文档索引/注册表/维护制度，纳入统一check。
- 加强模块依赖、编译顺序及文档反向测试；架构检查统一复用精确native profile，不解除默认禁写。
- 修正公开说明中的旧APK状态；初始化本地Git，增加私密产物排除。
- 按用户决定准备Gitee模板，绑定OWNER/REPOSITORY；远端可见性/身份尚待补齐，未推送、未启用远端CI。
- 相机Java/Studio算法没有变化，不新增任何机测或持久化能力声明。

## v0.6 本地开发推进 — 2026-09-19

- 完成Apple Silicon/macOS（历史测试平台）实际工具链配置与首个0.4-probe开发APK的SDK编译、DEX035、对齐和v1验签。
- 使用本地API10图标修复aapt badging；包身份与显式/隐含权限分别检查，版本命名从Manifest读取。
- 每次运行证据独立、防覆盖，修复macOS Java占位程序被doctor误识别的问题。
- 增加精确构建白名单、证据一致性校验与过渡期正反向测试；旧unknown保留为fixture，不删除设备门禁。
- 无机测、无持久颜色写入、无模型标定；工程与相机版本未混用。详细日志见PROJECT_STATUS。

## 0.6.0-design — 2026-09-19

- 将退出/重启后不运行App的原生颜色保留升为发布要求；保留实时样张创作。
- 核查Film Studio A7R II分支，区分运行时ISP效果、持久配置和软件LUT；记录API16第三方报告与非商用许可。
- 新增ADR0011、原生颜色政策/测试模板/发布门禁，更新所有主入口的冲突说明。
- 软件Studio仅更正范围提示；相机Java代码与颜色算法不变。无APK，无机测，无持久化驱动。


## 0.5.0-dev — 2026-09-19

- Studio 0.2: offline image import, live LUT preview, before/after, history, bounded curves/colour controls.
- Export the exact preview LUT; CVG authoring and CVP draft package. Camera importer remains absent.
- 27 added Node tests, 10 Chromium in-memory interaction checks; no Mac/Safari/device certification.
- Preserve native editor and Camera v0.4 unchanged; add Node tests to standard checks and a pinned setup-node CI step.

## 0.4.0-dev — 2026-09-19

Mac主环境、安装路线、Studio原生配方工具、22项契约测试；D8 jar调用和v1-only签名对齐Recipe Lab。没有APK/USB/Safari实测。

# Changelog

## 0.3.0-dev — 2026-09-19

### Added
源码复用调查、JPEG.CAM 公开仓库核查、工程与开源规范、ADR、模块清单、CI/PR/Issue 模板、环境诊断、架构守卫及故障注入测试、发布阻断检查。

### Changed
将 Filesafe/JpegGuard 从纯核心移至 io；Sony 相机/显示/按键集中到 sony；新增 Android-side camera-api 与诊断注入；UI 仅在 ProbeServices 选择后端。主机模块按依赖分别编译；Android 构建脚本同步多模块路线，未实测。

### Not implemented
未导入 Recipe Lab 配方代码；未集成 JPEG.CAM 或原生 C 图像库；无已验证 APK；无实机反挤压/出片/EVF 证据。正式 UI、颜色映射、文件关联、生产任务恢复仍待开发。

## 0.2 — 历史记录
见 docs/history/v0.2/ 和 evidence/history/v0.2/，不把历史测试日志冒充本次新执行记录。
