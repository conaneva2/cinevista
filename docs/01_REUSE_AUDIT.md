# 2026-10-25：复用原指令与固定QEMU核验状态消费者

R33复用固定4.01/A6000模块、已有ELF解析器、R28配置和R29 QEMU；没有新增依赖或复制其他项目实现。新增测试夹具限于私有研究目录，原始指令与反汇编不公开。通用virt/Cortex-A7仅用于ARMv7指令语义，不代替CXD90014板级或性能验证；三处标准ELF重定位不改判定逻辑，38例通过。

公开参照为Denali维护者2017-03-30补丁说明及已有Linux v6.12源码（GPL-2.0，仅事实对照）。配置寄存器代际差异、Sony ECC_ENABLE高位未知，均构成拒绝直接移植理由。A6000资料增量固定76d15b7至6984ce8，21提交/86路径，仅检查返回的patch；7个缺失patch的文件未全文检索，不引入其代码或固件。

# 2026-10-24：原驱动DMA来源与旧Spectra对照

R32复用固定4.01/A6000原模块、已有ELF工具及R29实验QEMU，未新增依赖。新增Linux v2.6.37 `drivers/staging/spectra`五份文本共127739字节，GPL-2.0，仅对照事实，源码不并入MIT项目。精确tag、blob与SHA256保存在私有证据清单；公开手册链接上游。

Spectra的0x720 bit1、完成/失败位15/14及请求中断bit8提供同类IP参照；其指针拆分、flags/status偏移、ECC填充公式与Sony存在实质差异，因此不移植描述符、ECC或中断执行逻辑。旧版16位纠错公式给28字节/步，8步已占224字节，无法同时容纳Sony的8字节metadata；这是否定直接套用的证据，不是Sony实际码字答案。匹配BOSS定向检索仍未取得可验证程序。

# 2026-10-24：extra消费者与A6000增量资料复核

R31复用固定4.01/A6000原模块、R27 ELF提取器及Linux v6.12 Denali缓存（GPL-2.0，仅作结构事实对照）。确认软件metadata与ECC状态，不据此生成物理spare。原模块/反汇编继续本地保留，未复制到公开副本。

A6000资料项目对照f4dc706262de807f6a9502cd5abc37af469747e0至76d15b79d5a401334974bda5abc55a4a33e2b736，8提交/189文件。仅读取增量，未引入代码或新依赖；变化以拍摄链路、证据修订和测试为主，未出现匹配BOSS。已删除的镜头BL/bootloader猜解不能成为NAND程序证据。完整来源及拒绝直接移植理由见研究手册。

# 2026-10-24：原extra/status合同与Cadence命令DMA对照

R30复用R27解析器、R28恢复配置和R29固定Sony模块/Denali缓存。新查Linux v6.12 `drivers/mtd/nand/raw/cadence-nand-controller.c`，GPL-2.0，84,073字节；仅核查结构事实，不复制进应用或模拟器。相似状态位不能消除Sony计数bits9:4与新源码bits9:2、flags偏移+18与+20的差异，直接移植成本与风险不可接受。Altera官方ECC表仅支持旁证容量计算，未下载大PDF，不采纳为Sony硬件规格。

原固件、反汇编与运行证据仍仅本地；公开内容是自写事实摘要。没有新增依赖、固件下载或机身访问。原生执行缺口不以静态核查计数代替。

# 2026-10-24：Denali ECC分代规则与原Sony读写合同

R29复用原4.01/A6000模块、R28参数、R27解析器和既有QEMU/qtest工具；新增核对Linux v6.12的drivers/mtd/nand/raw/denali.h及denali.c（GPL-2.0），共50,488字节，不引入依赖或复制驱动实现。适配成本在Sony定制DMA、BOSS和未确定ECC码字/元数据布局，通用驱动不能直接替代。新版bit0错误规则与原Sony消费路径对应，旧ECC_TRANSACTION_DONE含义不采纳为Sony完成规则。

仅自写事实总结公开；原文件、反汇编及日志留本地。QEMU配置/拒绝补丁独立遵循GPL-2.0-or-later，既有复位补丁一并补归档；不改应用MIT许可，不发布执行二进制。候选只实现四配置保存与未建模访问拒绝，不能声称ECC处理或BOSS挂载完成。

# 2026-10-24：复用原暖启动状态与页表读取器

R28继续使用fwtool.py@cdba742b（MIT）、R16已核实的WBI页表方法、R27 ELF与只读观察器、既有QEMU实验二进制。Sony官方缓存内核包提供启动RAM参数区域的交叉依据；不重复下载或引入新依赖。原4.01快照/模块及派生字节仅本地，不并入公开MIT源码。

与A6000比较保留块生成和配置寄存器映射；不复制外机参数。4.01保存配置只用于独立初始化回放，原模块自行处理输入，不注入BOSS回答或IRQ。不能由初始化一致推导出完整存储/ECC可用；进一步适配成本仍取决于缺失合同。公开仅自写研究摘要，见证据R28。

# 2026-10-23：复用原驱动与已有QEMU作启动对照

R27复用R26固定原lld/nand、既有ELF读取器与Apple LLVM，未下载或引入第三方代码。两机逐一核对18类操作实际提交/调用、结果转换与PBI布局，不移植A6000数据。复用既有build-nand-reset实验二进制和启动器；默认配置为对照，两项实验复位属性仅隔离后续依赖，Sony真实性仍未证实。只修改私有观察脚本，不修改模型/固件，不跳过原断言。

初始坏块表指针与SRAM传递的新运行证据保留本地。公开仅发布自写摘要，原模块、ASM、日志、虚拟介质和私人环境不上传。没有新依赖或传输；复用边界及失败见研究证据R27。

# 2026-10-23：A6000 BOSS驱动与新增来源取舍

继续复用fwtool.py@cdba742b固定解码、既有范围缓存、Python标准库和Apple LLVM；无需安装。Sony官方A6000 3.21仅新增约2.09MiB范围正文，两原驱动匹配既有公开hash并离线复读。原厂字节及派生材料只私有取证，不并入MIT代码。首次索引分区错误和追加预算已保留。

nicolvus@f4dc7062只审阅4个增量提交与未读启动说明，不采用代码；新nex3-filmgrain-project@4b5f95b0（MIT作者材料）仅提供SA格式线索并与原4.01验证；unixtract@51e50742元数据GPL-3.0，仅读两解析器，未安装/复制。外机启动/恢复不直接适用。BOSS协议模型仍是研究候选，完整语义/验收与GPU规则均未闭合，适配工期未知。来源见[证据R26](research/EVIDENCE.md)。

# 2026-10-23 BOSS候选来源核查

复用已有fwtool.py固定解码器、Python标准库ZIP/ELF相关工具及原4.01输入，只追R16未分类候选。新增AOSP android-4.1.2_r1 ResourceTypes.h和DexFile.h文本查阅（Apache-2.0），用作资源数组/DEX字段定义，无代码复制或新依赖；来源见[证据索引](research/EVIDENCE.md)。原Gitiles页面读取失败，AOSP GitHub镜像读取成功；未下载固件、仓库或大文件。相同字节只能按结构核对，不能把字符串索引、资源偏移或未分类SA数据误当BOSS程序。GPU/BOSS缺口仍阻止执行适配，工期未知。

# 2026-10-23 原MA入口与QEMU调试实现复核

复用已有QEMU固定归档1909382c及Sony官方内核包，局部读取module/sysfs、ARM内存与调试读取源码；四份调试相关源码与原归档逐字节一致。沿用Python标准库、原ELF符号与元数据断点观察器，无新依赖、安装或下载。原字节、日志、源节选留本地，自写结论及来源公开。成本和边界：只解决本首包观察的入口/上下文问题，不能替代GPU完成规范、BOSS载荷或真实性能模型；不复制外机实现或改原断言。

# 2026-10-23 研究手册维护与失败记录复核

复用既有五份手册、R21/R22证据、R23观察记录及本机文档/工程检查工具，无新工具安装和运行依赖。保留缓存入口读取E14的失败，不通过放宽核验取得成功。公开资料复核沿用软件保护条例、Sony许可与GitHub删除说明的已有官方链接；发布范围只增加自写技术总结，不引入原厂字节或第三方实现。个人兴趣声明不代替分发授权，许可和公开范围见[PUBLICATION](PUBLICATION.md)。

# 2026-10-23：原生缓冲服务取证

复用既有ELF/PLT解析、Apple LLVM、Python和R21只读QEMU观察器。新增的小型Thumb BL候选扫描必须逐点以LLVM与上下文核验，不把数据或邻近动态符号当函数语义。原生函数身份另以原断言字符串、GOT、线程参数和跳表核对。原厂字节/反汇编只本地保留，无新组件或许可引入。

AOSP 4.1.2使用标志复用R21缓存，不重复下载；其0x1f00范围不覆盖HW_VIDEO_ENCODER=0x10000，不能据此推定Sony录像支持。两条锁命令未提供GPU完成协议，不移植替身或改成功返回。详见[证据R22](research/EVIDENCE.md)，完整适配成本仍取决于GPU和BOSS缺口。

# 2026-10-23：MA/窗口契约与官方接口参照

复用本机 Python、已有 ELF 解析和 Apple LLVM，修正分析脚本对原生 PLT 可选 Thumb veneer 的识别；对每个跳转槽核验 GOT/重定位，不放宽未解析检查。没有新运行依赖或工具安装。复用既有 Sony GPL 内核包，仅局部提取页属性、DMA、映射和打开标志文件；原厂派生材料只私有取证。

新增 AOSP `android-4.1.2_r1` 的 gralloc.h、graphics.h（Apache-2.0），13,816 字节文本，只核对参数次序和私有格式范围，不复制实现。精确来源、hash 与适用边界见[资料索引 R21](research/EVIDENCE.md)。Android 客户端不能直接代替原生 libObj/服务端，未移植 A6000 代码或假定完整 DMP 兼容；完整适配仍缺硬件完成与 BOSS 依据。

# 2026-10-23：研究手册整理

复用既有原始记录、固定版本和本地Python文档检查工具，无新运行依赖、工具安装或第三方代码引入。五份自写汇总见[研究手册](research/README.md)；最近A6000/RX100 V原驱动与库的事实、固定来源和许可界限见[资料索引](research/EVIDENCE.md)。原厂程序与派生反汇编继续不进入公开副本。公开核查沿用MIT自有代码与逐文件GPL/LGPL QEMU补丁边界；同代资料只用于交叉核对，不据此替换4.01原库。

> **v0.6修订优先：** 后端主线改为原生颜色持久化，同时保留实时样张创作。参见 `15_NATIVE_PERSISTENCE.md` 和 ADR0011。下文的软件主线/永不持久写入/所有机身API10表述作为历史设计，不覆盖新决定。实现状态仍以 PROJECT_STATUS 为准。

## 2026-10-23：GPU诊断与新增社区对照

复用原4.01驱动/库和现有LLVM提取，不增加依赖。新增静态分派审计，只读原文件，不运行相机ioctl。cokeenet/zve10-qemu固定654138ef：根许可证MIT，但QEMU/内核修改仍遵循上游许可；其常量寄存器及图形固定返回不满足原固件同步验证，未合入。nicolvus/a6000-fw-decomp固定2ebc1436：只取作者公布的7个文本记录，核对哈希，支持同系列IRQ76与SMAPH-S30；未审查可并入代码的许可，不复用代码，不使用其相机脚本。其A6000驱动hash不同，适配不能直接搬地址。

两个来源共约1.30 MiB文本，缓存有逐文件URL/大小/SHA256；未克隆整库或下载新固件。DMP官方产品说明不含当前所需寄存器合同。完整取舍及固定链接见`../handoff/runs/20261023T022306Z-sugilite-diagnostics/FINDINGS.md`。

## 2026-10-23：原DMP调试信息与同步合同

复用原4.01 Android `libGLESv2_dmp.so`/`libGLESv1_CM_dmp.so`/`libDMPSUGIRM.so` 的现有ELF/DWARF及本机Apple LLVM，只做本地读取，不并入MIT发行包。两份GLES的293项寄存器枚举一致；同一错误纹理全局的分配/纹理/虚读引用已闭合。新增小型只读提取与GDB观察脚本，复用现有QEMU运行器和RSP方式，无新增依赖/构建系统。

Sony官方内核缓存固定哈希仍为f502295d086c9e523758b86dc27134d78004a487f8ffe052cfa7d78aa3051cfa；ma1co/qemu固定1909382c0d3533051cead7fde70ca8e84807ee14的三版二进制保持。DMP官方产品页未提供寄存器合同；公开资料检索与既有libctru固定9b55eda44cf80b971503991e0c78f9bc8fe50425均不足以证明Sony端口/IRQ语义，未复制PICA执行代码。原库调试路径不是已取得的SDK源码；未声称可以重新分发专有代码。精确来源、地址和欠项见`handoff/runs/20261023T015609Z-sugilite-semantics/FINDINGS.md`。


# 01｜源码复用调查与采购决策
2026-09-19；审查范围是本次取得的官方资料、公开源码和指定提交。没有在相机上独立复现上游项目。

## 结论
不要整包 fork 某个相机 App，再往其主 Activity 中继续堆功能。采用成熟基础组件，选择性移植同平台的工作代码，把幕野特有的几何、摄影工作流和能力判断留在独立模块。

“源码存在”“许可证允许”“可以编译”“已经适配 API10”“已经在 A7R II 指定固件上测试”“适合发布”是六件事。项目近期活跃、星数和 README 中的兼容列表不能替代这些检查。

分级：A=通用领域成熟组件；B=同平台有具体实现但仍需移植验收；C=仅接口声明/有限例程；D=本轮没有核验到所需的可复用完整实现。分级是我们的选型判断，不是上游认证。

## 全功能复用矩阵
| 功能 | 现有源码/技术 | 证据与成熟度 | 幕野采用方式 | 仍需做什么 |
|---|---|---|---|---|
| USB 安装应用 | Sony-PMCA-RE | B；MIT；已有安装命令和社区工具 [S01] | 作为外部工具，不造安装器，不打进 APK | 固定实际采用提交、驱动和首测电脑验证 |
| 相机打开/释放、半按/全按、按键 | PMCADemo + OpenMemories | B；MIT；具体 Java 实现 [S02,S03] | 在 sony 适配模块中移植必要路径 | 实际模式拨盘、错误、生命周期和保存回执 |
| 背屏/EVF 信息与切换 | OpenMemories DisplayManager | B/C；包装代码存在，机身表现未知 [S03] | 复用已理解的设备信息逻辑 | 分别校准物理显示比例、有效图像区域、切换状态 |
| 普通宽幅遮框 | JPEG.CAM CinemaMatteView | B；Canvas 示例，使用 2.71f [S07] | 借鉴显示层做法；使用幕野统一 Geometry，不复制近似常量 | 框到成片校准、移框和对焦放大映射 |
| 胶片色彩 | Recipe Lab Recipes/Params/运行时参数 | B；MIT；A6000 为研发基准 [S04] | 复用配方与已理解的参数语义；独立来源目录与适配器 | A7R II 参数映射、RAW/PE/曝光与稳定延迟验收 |
| 真实实时反挤压 | 原生 Surface、旧 Camera 回调、CameraSequence | C/D；目前没有核验到 A7R II 上完整现成方案 [S03,S05] | 保留探针，两条主要显示路线逐一测试；不自造硬件 API | 实际影像非等比变换、完整边缘、帧更新、延迟与 EVF |
| 缩放/裁切/JPEG 原生输出 | Sony CropImageFilter/ScaleImageFilter/JpegExporter | C；存根不是实现源码 [S03] | 优先测试已有优化管线，以接口封装 | 输入限制、尺寸、像素结果、所有权和媒体登记 |
| 内存有界的软件 JPEG 输出 | libjpeg-turbo；JPEG.CAM 分行处理 | A(codec)+B(同平台例程) [S08,S09] | 优先复用成熟 codec；借鉴分行处理，不另写 JPEG 编解码 | PMCA ABI/NDK、重采样质量、色彩、错误与资源预算 |
| YUV/RGB 变换 | libyuv | A(通用)+未适配 [S11] | 只有取得可用预览帧后才进入依赖选型 | 帧格式/步长/权限/ABI，不能拿缩放库当取帧接口 |
| JPEG 元数据/方向 | API10 ExifInterface 可用部分；现有严格输入守卫 | 平台组件可复用，API 能力需按 API10 核对 [S13] | 尽量复用平台元数据功能；不扩写一套完整 EXIF 引擎 | 改尺寸/方向后重建标签与缩略图；MakerNote/ICC 单独策略 |
| 设置/任务日志 | SharedPreferences + SQLiteOpenHelper | A(平台) [S14,S15] | 小设置用平台偏好；持久任务使用 SQLite 的独立 repository | 版本迁移、事务、幂等恢复；当前探针还未实现完整队列 |
| 查照片/回看 | OpenMemories MediaManager/PMCADemo Playback | B；查询与显示例程 [S02,S03] | 复用媒体读取；写入封装在 MediaPort 后 | “写 JPEG”不等于“原生相册/无线传图可用” |
| 真实源图关联 | CameraEx StoreImageCompleteListener/StoreImageInfo | C；有回执字段 [S03] | 读实际回执，验证文件身份后才确认 | RAW+JPEG 分组、晚回调、错配、重启恢复 |
| 构建/签名 | javac + Android SDK aapt/D8/zipalign/apksigner | A(官方工具)，API10 组合待鉴定 [S16,S17] | 复用官方工具，不造编译器/DEX/签名算法 | 完整 SDK 编译、包检查、签名、实机加载 |
| 质量流程 | Git/GitHub Actions、Python unittest、现有回归 | A(通用工具)，项目规则为新增 [S18] | 现成 CI 编排+小型边界检查；不造测试平台 | 远程配置实际生效、失败样本与设备回归 |
| 视频/HDMI 反挤压直录 | 本轮未找到可核验全链路 | D | 独立后续研究，不从照片功能推定 | 录像时预览、编码控制、接口权限、输出比例 |

## 重要修正：JPEG.CAM 已找到源码
上一轮只核查了网站，未找到可复用源码；本轮定位到 `upsetstomach56/JPEG.CAM-2.0`，审查提交 `20a30c82a058560c64002e205f2152104c3ea8ba`。README 自称 early beta/proof of concept。[S06]

有价值的部分：`CinemaMatteView.java` 的同平台遮幅；`native-lib.cpp` 的 JPEG 分行/分块处理；Java/NDK 分工。它不是只有图片和演示的空壳。

不能整套原样并入：静态读取发现中心裁切用2.71f、复制全部 APP/COM 标记、全局 LUT 状态以及直接以 wb 打开输出。这些与幕野精确比例、冻结拍摄意图、元数据重建和不覆盖的约束不同。[S07,S08] 这是代码审查发现的设计差异，不是我们已经复现了上游某个事故。

根目录 MIT 许可证仍为 ma1co 的继承声明；单独的字体、LUT、纹理、stb/libjpeg 依赖必须另核来源和许可。不要推断“根目录 MIT”覆盖所有外部素材。本包不分发这些资产。

## 不采用的捷径
- 不拿现代 CameraX/TextureView/Compose 手机 App 改包名当 API10 相机 App。
- 不把 Sony 存根当真正图像实现打入 APK，不重写同名 com.sony 类。
- 不为简单照片裁切引入完整 OpenCV、FFmpeg、云端服务或大型依赖注入框架。
- 不因为老 NDK 示例可构建就永久锁死有安全隐患的古老 codec；旧平台适配和依赖安全需共同评估。
- 不扩展现有 JpegGuard 成全功能元数据解析库。它目前只是“明确支持/明确拒绝”的前置检查。
- 不通过一份胶片配方给所有机身写入相同 A6000 Backup 槽。

## 复用入口规则
每次引入必须记录：确切用途、备选、锁定提交/版本、许可证与资产范围、移植改动、设备证据、退出成本、维护责任。`adopt` 不等于已经 vendored，`included_code=false` 必须保持真实。

同一功能先做最小集成实验；只有已有轮子不满足明确条件才新增实现，并提交 ADR。即使采用成熟库，也测试我们的调用、缓冲、坐标和参数组合。

检索限制：已检查列出的代码库及关键词 anamorphic/desqueeze/PMCA 等，没有核验到目标相机完整实时反挤压成熟源码；不宣称全网绝对不存在。

## 相机UI预览增量决策（2026-09-19）

复用平台API10 XML/View布局，首页资源与事件分离；无新增APK依赖。原生精确预览优先Android Layout Editor，当前仅交付有限首页结构草图，不重做Android排版引擎。候选、版本、许可和未采用理由见[相机界面与预览](CAMERA_UI_PREVIEW.md)。

## 中文大字UI实现（2026-09-20）

继续复用已锁定Google API10r02的XML/字符串/selector/AlertDialog，构建工具30.0.3；未新增第三方库或字体。Sony按键沿用既有KeyResolver并复用于Dialog窗口。用户选择Linear方向的自有概念，未复制品牌源码/字体；图片只作本机设计参考，不打入APK。浏览器草图新增有限结构映射，明确不实现完整Android排版。原生视觉验收待U02/T03。

## PMCA连接准备（2026-09-20）

采用Sony-PMCA-RE MIT固定a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0作为外部CLI，不并入APK。审查CLI/驱动/枚举/info及install分派，未调用安装/固件/服务模式。依赖版本和归档哈希见config/camera-connection.lock.json；CLI无设备查询成功不等于已连接。继续优先现有ARM64 libusb1.0.30，不安装未获macOS27资格的旧Sony系统驱动。官方固件仅本机留存，不再分发。


## 2026-09-20 MTP查询适配

继续复用MIT Sony-PMCA-RE a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0的设备、协议解析与传输；不修改上游、不重写USB驱动。tools/macos/camera_info.py仅组合单会话调用，避免listDevices重复包装导致第二次backend.reset权限错误。实际ILCE-7RM2扩展型号读取成功；不推断安装通道通过。


## 2026-09-20 被动USB证据修复

复用macOS内置ioreg和Python标准库plistlib/subprocess，不新增USB库/驱动。使用-a -l请求设备属性；支持当前macOS返回单个根字典。主机工具只做参数、证据结构校验与脱敏输出；无相机协议实现。缺失属性需报错，不能按无设备处理。

## 2026-09-20 官方固件离线事故分析

采用fwtool.py MIT提交cdba742b73eed5981480c326aeb30033aabf0223解包官方4.01数据，复用既有Cryptodome3.23.0/PyYAML6.0.3；只调用解包器，不执行升级器或USB。拒绝自研固件解密/文件系统。Sony固件和派生代码仅本地诊断，不入MIT发行包。

复用baksmali/dexlib2/util2.5.2（BSD-3-Clause）及Maven声明的本地分析依赖：Guava27.1-android、JCommander1.64、JSR3053.0.2、failureaccess1.0.1。均保存在.local/recovery-research，逐包Maven校验和与SHA256留档，不修改系统或App运行时依赖。拒绝把现代dexdump错误解析的优化指令当证据。解析成本是采用固件API16和同包30项BOOTCLASSPATH；部分execute-inline仍未还原，只使用确认无分析错误的cacheLocked方法。工具精确归档/hash/局限见最新事故SESSION；退出成本为停用本地分析目录。

## 2026-09-20 安装流程复盘

继续使用同一PMCA提交、baksmali2.5.2和官方4.01副本；未新增依赖或并入固件代码。9个关键方法局部符号解析无错误，另保留PackageManagerService共30处分析错误及目标同步方法不完整限制。标准库mock仅验证主机错误传播与结束握手，不模拟设备安装成功。来源与方法哈希：`handoff/runs/20260920T024526Z-install-forensic-review/reviewed-methods.json`；复盘：`handoff/runs/20260920T024526Z-install-forensic-review/FINDINGS.md`。


## 2026-09-20 厂家恢复工具来源

确认A7R II厂家维修手册使用Adjust Station及本型号Adjust Manual，但未证明黑屏无USB时可强制重刷。公开4.01升级器要求USB Mass Storage，已有4.01按官方流程结束。未找到可验证的本故障救砖包；无机身操作。
未取得或引入专有软件；仅引用Sony手册摘要。来源与限制：`handoff/runs/20260920T031004Z-manufacturer-recovery-research/FINDINGS.md`。


## 2026-09-20 ODEX离线解析辅助

pyelftools0.32（PyPI包SHA256核验，公共领域许可及包内许可条款）仅作为本地取证工具zipimport，未安装到系统或纳入APK/运行时。复用ELF解析器而非自造通用解析；AOSP结构定义用于核验，Sony字节数据不发布。baksmali2.5.2沿用既有工具。来源/许可/hash：`handoff/runs/20260920T034308Z-safe-mode-callchain/dependency.json`；限制：`handoff/runs/20260920T034308Z-safe-mode-callchain/FINDINGS.md`。

## 2026-09-20 G03 打包契约

沿用config/toolchain.lock.json已核验Android SDK Build Tools30.0.3及API10 jar，遵循既有SDK许可，工具不并入APK。复用aapt的二进制XML/资源表解析及PNG crunch解码；不引入自研通用资源解析器或PNG编解码器。Python标准库仅固定dump适配、PNG块类型筛选与项目白名单。资源别名/复杂值保守拒绝。测试使用真实aapt临时包，SDK缺失明确skip，不造假SDK。证据：`handoff/runs/20260920T041708Z-launcher-gate/FINDINGS.md`。


## 2026-09-27 更新环境离线可行性

沿用MIT Sony-PMCA-RE a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0与MIT fwtool.py cdba742b73eed5981480c326aeb30033aabf0223；仅离线解析既有型号载荷，不重写解密器、不执行USB、不新增运行时依赖。只读审查PMCA的OpenMemories-Platform子模块固定提交85bcb5454bc68a971b674d3b9e93eeedbf35cf3c的备份API；没有复制其实现或引入依赖。新增小型主机脚本只组合既有解析器并保存哈希/断言，退出成本是停用该分析脚本。拒绝把通用updater shell直接当作只读救援工具，因其自动可写挂载及未验证的故障入口；永久固件改写方案尚未采用。Sony固件与提取二进制只存.local，不随MIT发行。维护责任为本轮调查作者；设备证据仍缺失。详见handoff/runs/20260927T053659Z-recovery-feasibility/FINDINGS.md。


## 2026-10-22 实时反挤压离线鉴定

复用已有官方ILCE-7RM2 4.01解包副本、baksmali/dexlib2/util2.5.2（BSD-3-Clause）及前述固定依赖、pyelftools0.32（原许可条款）和系统Apple LLVM。无新下载、系统安装或产品运行时依赖。精确输入SHA256、命令及选取函数索引见 `handoff/runs/20261022T014755Z-desqueeze-feasibility/evidence-manifest.json` 及同目录JSON。仅分析副本修改ODEX容器版本标记并使用同固件inline table；原始固件未改。SmartRemote、CameraSequence与图形库专有代码仅作本地证据，不复制到MIT产品。选择官方取帧调用链作为B路径依据，拒绝把第三方桩类或Surface尺寸当成硬件能力证明。迁移成本在权限/生命周期、帧释放、机内解码显示和LCD/EVF；尚未实施。退路为保留离线证据并停止候选，不产生设备状态回退要求。


## 2026-10-22 原生录像编码前路径

继续复用本机官方ILCE-7RM2 4.01、baksmali/dexlib2 2.5.2（BSD-3-Clause）、pyelftools 0.32（沿用已核验归档与许可）、Apple LLVM与c++filt，只做静态取证，未下载或引入运行时组件。Sony代码仍属固件本地诊断资料，不并入MIT发行包。标准Camera HAL录像短函数、Sony SDCom录像链及DSP路径5已核验；路径5到电影编码输入未闭环。软件H.264组件虽有实现，但不据此选用为实时原生录像替代。证据和源SHA256：`handoff/runs/20261022T021116Z-video-encoder-feasibility/FINDINGS.md`及同目录各JSON。


## 2026-10-22 DSP效果录像通道

继续复用已有官方4.01、pyelftools0.32及Apple LLVM/c++filt，无新下载、安装或产品依赖。对av-cam.bin创建字节不变的分析ELF包装，选区反汇编后包装作为可重建中间文件删除；不执行目标代码。SHA256及静态指令复核见 `handoff/runs/20261022T023458Z-dsp-movie-chain/evidence-manifest.json`。原始固件和派生汇编留在.local，不并入MIT产品或上传。确认路径5至EffectMovieRec及画布至RecPin的实际实现；动态连接至编码模式尚缺证据，未实施硬件接入或自定义DSP算法。维护责任为本轮调查作者，退出成本为停止候选研究；没有设备状态需要回退。


## 2026-10-22：录像动态连接与DSP几何续查

复用本地官方4.01、此前反编译结果、pyelftools 0.32与系统LLVM，不引入组件或依赖，不下载整库。确认SFR录像槽6的外部身份和运行时连接机制；目标模式对端未闭环。SCALE/resizeTrim与SA插件契约不同，VFX Transfer不能当作已证明缩放器。无可核验的新DSP重采样上游实现。证据：`handoff/runs/20261022T032031Z-rec-pin-dsp-geometry/FINDINGS.md`；主机校验见同目录validation.json，设备与性能未验证。


## 2026-10-22 实际录像拓扑与SDF缩放复用审查

来源仍为本地官方ILCE-7RM2 4.01专有固件，六个输入哈希见 `handoff/runs/20261022T034123Z-movie-peer-scale-backend/evidence-manifest.json`；只做接口/行为分析，不将固件代码纳入MIT发行。复用既有pyelftools 0.32分析脚本与系统LLVM，无下载或安装新组件。

SCALAR_MOVIE_REC的Camera→Scalar→Effect→MovieRecorder拓扑及原生MovieEncoder主路YC请求已定位；VEF/可选TCUB与编码格式分支不可忽略。SCALE/resizeTrim已追到SDF任务、标准YC画布及输出票据，作为底层缩放候选保留。没有现成逐帧接回录像的证据，不能直接用ScaleImageFilter替换SA插件，亦无实时预算验证；适配成本仍包含帧桥接、所有权、同步、格式和硬件资源并用。无新增依赖/复制组件，不能由此解除事故暂停。

详见 `handoff/runs/20261022T034123Z-movie-peer-scale-backend/FINDINGS.md`；T11继续blocked。


## 2026-10-22 SDF生命周期与仿真候选复核

- 复用本地官方4.01、已有pyelftools0.32/LLVM反汇编与aapt30.0.3检查，不下载新固件或引入图像/仿真依赖。新增libStm票据生命周期及MC的MMC释放、Vsync证据，输入哈希见本轮manifest。固件为本地研究材料，不随MIT工程分发。
- OpenMemories-Framework（已有锁定候选f8df3504d8684433a331ee869e64f67cc8be9730，MIT）：公开README的普通Android模拟器能力依靠dummy实现，只可借鉴应用替身分层，不能用来证明Sony安装/硬件行为。本轮未导入代码。
- QEMU官方Arm文档（2026-10-22读取滚动页；未选二进制版本、未安装）：需要适配板模型，公开列表未见A7R II；完整SoC/外设模型成本未定，当前不采用其作为可直接启动固件的现成方案。后续实际引入需锁定版本及核验GPL等具体组件许可。
- Android Emulator官方快照文档（2026-10-22读取；镜像/运行时版本未选、未下载）：可作为兼容实验的回滚机制；API16/ABI与本Mac组合尚未验证，不能替代冷启动测试或实体恢复。实际采用前核对SDK/系统镜像许可，当前未引入。
- 实际复用现有launcher_contract检测留存事故APK，exit2拒绝XML图标；没有另造安装框架、没有新可安装APK。完整仿真未获证据，候选范围限安装/启动组件兼容实验。
- 来源与精确证据：`handoff/runs/20261022T073608Z-sdf-lifecycle-emulator/FINDINGS.md`、`handoff/runs/20261022T073608Z-sdf-lifecycle-emulator/evidence-manifest.json`、`handoff/runs/20261022T073608Z-sdf-lifecycle-emulator/original-apk-gate.json`。


## 2026-10-22｜安装启动实验环境复用决定

| 候选/精确版本 | 许可与适配成本 | 本轮决定 |
|---|---|---|
| Android SDK aapt 30.0.3；本机二进制hash写入实验结果 | 外部Android SDK工具，遵守SDK条款；已有本地安装 | 复用二进制XML/资源解析，不自写APK资源解析器 |
| baksmali 2.5.2；匹配libdvm的22项内联表 | BSD-3-Clause工具；Sony固件内容不据此开源 | 复用反汇编；只改分析副本容器标签，拒绝含解析错误的方法 |
| Sony-PMCA-RE `a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0` | MIT；已有独立Python venv，FakeCamera输入无需设备后端 | 直接运行真实installer.install循环，不重写安装协议，不把合成消息说成事故抓包 |
| Python标准库unittest/json/unittest.mock | PSF；已有宿主工具链 | 复用测试/快照/断网替身；新增小型固件方法控制流回放器是限定实验适配，不是通用Android模拟框架 |
| ma1co/qemu `1909382c0d3533051cead7fde70ca8e84807ee14` | QEMU为GPL系，具体文件仍需逐项审查；需要构建、映像与板级适配 | 已确认含CXD90014，作为后续独立宿主候选；本轮不克隆/构建，不并入MIT应用 |
| OpenMemories-CI `4f8c6367a75e9afd02bc684425e3fbff424b2223` | 未取得可据以移植的许可证结论；测试还依赖机型dump | 只读参考RX100M5 updater测试设计，不复制源码或固件；不能据此声明A7R II Android可启动 |
| OpenMemories-Framework `f8df3504d8684433a331ee869e64f67cc8be9730` | MIT；dummy API不是固件运行实现 | 不将接口替身当本次真实环境；仍是API参考 |

原始固件与原APK保持本地，配置锁只保存路径与hash。新回放器无法替代原生扫描、Settings持久化、系统启动或DSP；未知调用停止。边界、运行命令、反例及原始证据见 `INSTALL_BOOT_LAB.md`、`handoff/runs/20261022T075951Z-install-boot-lab/FINDINGS.md`。


## 2026-10-22｜QEMU启动候选材料

- 固定QEMU仍为 `1909382c0d3533051cead7fde70ca8e84807ee14`，源码VERSION 5.1.0；只读取10个相关源码文本，未克隆/构建。generic-loader可用作固定地址参数加载候选；CXD90014的NAND写/擦未保存后端，不能复用为已通过的持久安装环境。GPL系外部宿主候选不并入MIT相机APK。
- 固定OpenMemories-CI `4f8c6367a75e9afd02bc684425e3fbff424b2223`仅参考RX100M5测试范围，不复制其未明确许可的测试代码；其gzip/cramfs处理不直接用于本机裸内核/ext2初始根。
- 复用已有fwtool.py `cdba742b73eed5981480c326aeb30033aabf0223`，MIT：从原ext2提取BusyBox及动态依赖/链接，用现成cramfs写入器制备最小实验根，并用读取器核对CRC和内容。不自写文件系统打包器；实验fixture属主规范化为root，原始属主单独记录，不声称完整文件系统还原。
- 复用已有LLVM objdump、pyelftools0.32、Python标准库；只有原始固件分析副本，没有设备执行。候选rootfs905216 bytes，原始内核不补丁。
- 索尼官方ILCE-7RM2源码页的linux-kernel.tar.gz仅HEAD核验大小52,882,363 bytes，未下载；与4.01精确匹配和各组件许可待核验，不能宣称已取得完整专有系统源码。
- 证据和精确小文件SHA-256：`handoff/runs/20261022T082324Z-qemu-boot-readiness/upstream-inputs.json`、`firmware-inputs.json`、`boot-candidate.json`。无新增生产依赖。


## 2026-10-22｜QEMU实际构建与最小Linux执行

| 来源与精确版本 | 许可/适配 | 决定与结果 |
|---|---|---|
| ma1co/qemu 1909382c0d3533051cead7fde70ca8e84807ee14，5.1.0 | COPYING GPLv2，各文件许可保留；独立宿主实验工具 | 本机构建；原生TCG分配失败后复用自带TCI，只将TCI字节码内存去掉EXEC。单文件补丁和原归档逐文件对比均保存，不并入MIT相机APK |
| dtc 85e5d839847af54efab170f2b1331b2a6421e647 | libfdt头部为GPL-2.0-or-later或BSD-2-Clause | 只补匹配子模块，复用设备树库，不自写 |
| keycodemapdb 6b3d716e2b6472eb7189d3220552280ef3d832ce | 归档含GPL2/BSD许可，按文件保留 | 补固定构建子模块，不复制至产品源码 |
| pkgconf 3.0.10 | 宽松许可，COPYING原文保留 | Homebrew安装未成功后源码本地安装，复用依赖发现；无全局库替换 |
| libmad 0.15.1b | GPL系，保留COPYING | QEMU必需音频依赖；静态本地构建，更新config.sub/guess并覆盖旧GCC优化选项。未验证音频功能 |
| libmad 0.16.5 | 未采用且未并入构建 | 需额外CMake，不为此扩大工具下载，改用可直接configure的旧版；下载证据保留，未用产物清理 |
| Apple clang 17.0.0、GNU Make3.81、系统Python3.9、现有glib/pixman/libjpeg | 既有主机工具/库，遵守原许可 | 复用本地环境；关闭与旧版不兼容的可选nettle/gnutls/gcrypt，不替换现有库 |

源码包、实际二进制、补丁hash和精确子模块提交见`handoff/runs/20261022T084735Z-qemu-first-boot/build-manifest.json`。最小Linux真实运行与后续Android/持久性未验证分开记录。原始固件/BusyBox派生实验根仍为本地私有资料，不因QEMU许可而公开。


## 2026-10-22｜虚拟NAND与Android服务启动复用

- 沿用ma1co/qemu `1909382c0d3533051cead7fde70ca8e84807ee14`（5.1.0，GPL系独立宿主工具），复用既有控制器命令解析和BlockBackend，补有限模式写入/擦除/flush；用自带qtest做跨进程持久性反例和正例。不并入MIT应用；没有另造通用存储模拟框架。
- 沿用fwtool.py `cdba742b73eed5981480c326aeb30033aabf0223`（MIT）生成cramfs，原版4.01内核、Android init、ext2 system、devno/osal_utm/osal_uipc保持本地私有。loop只读system与tmpfs data为实验适配，不能当真实数据分区。
- 固定OpenMemories-CI `4f8c6367a75e9afd02bc684425e3fbff424b2223`仅只读参考NAND参数字段，许可证未确认，不复制到MIT产品；约2KB参考文本之外无新网络大文件。合成SRAM/NAND不是A7R II真实dump。
- 延续LLVM objdump和Python标准库分析；Thumb gralloc与ARM OSAL分别正确反汇编。具体输入hash、宿主补丁、构建和动态对照见`handoff/runs/20261022T091300Z-qemu-storage-android/FINDINGS.md`。控制器持久性已验证，Sony FTL、完整Android与APK兼容性未验证。


## 2026-10-22｜A7R II 4.01分支配置与原生服务复用

- frozencaviar/OpenMemories-CI@423179bd095abeb3280a43d6848645fce58cfa57：固定源码缓存来自前轮，只参考电源接线、partinf布局和中断调查方法；未明确取得可复制该测试项目的许可，不复制到MIT产品。其修改QEMU10.2的CID/CRC、BOSS/LZP等能力不能套在现有5.1上；未采用固件/Loader3错误跳过、GIC优先级修补或主机伪造数据。
- ma1co/qemu@1909382c0d3533051cead7fde70ca8e84807ee14：既有GPL系独立宿主工具，保留前轮TCI/NAND补丁；本轮无新源码修改或构建。复用原有qtest/QMP，不引入测试框架。二进制SHA256仍cf823fe3a1f832a40d5c984421e2ff203fce671847d7e923502999a22313c020。
- 官方ILCE-7RM2 4.01专有固件：原样复用原生库、im/bootin、utimer/backup及MainDest默认备份，保持本地且不分发。默认备份不是机身dump。按原kemco恢复备份内存保留、按原驱动公开参数Backup_load=1初始化，未改变数据/校验。全分区FTL和设备状态适配成本仍高。
- 沿用fwtool.py@cdba742b73eed5981480c326aeb30033aabf0223（MIT）的ext2/cramfs处理、Python tarfile/JSON和本机LLVM只读反汇编；未下载依赖、未自写文件系统或运行外部分支脚本。
- 实际对照、失败和回退：`handoff/runs/20261022T100302Z-a7rii-board-alignment/FINDINGS.md`；原始输入完整性：`handoff/runs/20261022T100302Z-a7rii-board-alignment/input-integrity.json`。

## 2026-10-23｜gl_common消息依赖及只读动态调试

- 沿用ma1co/qemu@1909382c0d3533051cead7fde70ca8e84807ee14（GPL系独立工具）现有二进制；复用内置GDB协议断点与寄存器/内存读取，无新编译、无QEMU/固件错误绕过。ASLR只在guest诊断组临时关闭。固定binary hash与各组条件见本轮记录。
- 沿用fwtool.py@cdba742b73eed5981480c326aeb30033aabf0223（MIT）读写派生cramfs；仅原样增补官方4.01 grm_ma.ko、dmm.ko、osal_ulogio.ko、DmmConfig.bin，材料保持私有。拒绝把缺失ulogio配置替换成假成功回调。
- Sony-PMCA-RE@a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0（LICENSE.txt MIT）：仅导入pmca.backup.BackupFile解析本地BytesIO，核对DMM的原默认地址字段；未调用设备、platform backend或USB模块，不接机。
- frozencaviar/OpenMemories-CI@423179bd095abeb3280a43d6848645fce58cfa57仅参考已缓存作者笔记；其按地址跳过grm_ma/grm_gles初始化的做法未采用。用原回调注册和动态返回核验，不把“模块加载返回成功”当作服务可用。
- 所有版本、原始文件hash和复跑边界：`handoff/runs/20261022T225823Z-gl-common/FINDINGS.md`、`handoff/runs/20261022T225823Z-gl-common/reuse.json`；无新增产品依赖。

## 2026-10-23 日志配置恢复与虚拟相机操作台

- 继续复用ma1co/qemu@1909382c0d3533051cead7fde70ca8e84807ee14（5.1.0，GPL系独立宿主工具），本轮无新QEMU补丁，既有TCI/NAND补丁和二进制哈希不变；不移入MIT相机APK。
- 复用fwtool.py@cdba742b73eed5981480c326aeb30033aabf0223（MIT）的WBI解压和cramfs读写；只扫描本地官方4.01并恢复快照原字节，不自写压缩器/文件系统。Sony原驱动/程序和恢复配置仅作私有本地实验，无再分发授权。
- 新操作台复用Python3.9标准库http.server/subprocess/threading、原有限时QMP实验器，及浏览器原生HTML/CSS/JS。不引入前端/后端框架、素材库或依赖下载；小型自有代码仅封装本地固定实验和显示真实状态。
- 官方Sony后背部件说明只作为按钮布局参考，自写CSS，不下载/复制产品照片。OpenMemories硬件说明、iFixit原拆机及Micron型号资料作为研究事实；未能确认物理NAND容量/CPU主频，保留未知。
- 普通Android模拟器不能覆盖Sony服务和安装器；未选择以它替代原4.01。完整窗口、持久/data与APK仍缺，宿主UI不是原固件画面。来源链接及限制见docs/VIRTUAL_CAMERA.md，证据在handoff/runs/20261022T235438Z-ulogio-emulator。

## 2026-10-23｜sugilite 与 TextRM 依赖对照

- 继续使用 ma1co/qemu@1909382c0d3533051cead7fde70ca8e84807ee14（5.1.0，GPL系独立工具），内置GDB/QMP只读调试；本轮无QEMU改动、新编译或下载。未采用同机型分支的grm_gles断言跳过。
- fwtool.py@cdba742b73eed5981480c326aeb30033aabf0223（MIT）继续处理ext2/cramfs；Sony-PMCA-RE@a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0（MIT）仅导入BackupFile解析本地默认副本，未加载设备后端。复用LLVM反汇编和Python标准库，不安装capstone/pyelftools、不自研文件系统。
- 原版4.01 grm_gles、字体列表及六个字体仅本地诊断，未经再分发授权，不进入MIT产品。补环境资源优于伪造字体/返回值；图形寄存器语义未齐，未用空设备或常量寄存器替代真实模型。
- 适配成本：原顺序/节点/字体已确认，图形时钟/复位、IRQ76、任务队列与帧输出仍需实现并验证。停用本轮fixture即可回退到原操作台实验。哈希、失败/成功条件与复跑：`handoff/runs/20261023T002402Z-sugilite-window/FINDINGS.md`、`input-integrity.json`、`SESSION.md`。


## 2026-10-23｜官方CXD90014源码与控制寄存器模型

- Sony ILCE-7RM2官方页链接的ILCE-7M2/linux-kernel.tar.gz，52,882,363 bytes，SHA256 f502295d086c9e523758b86dc27134d78004a487f8ffe052cfa7d78aa3051cfa；Linux3.0.27、rt106，所用Sony平台文件GPLv2。仅离线事实校验，未替换原内核，也未引入MIT应用。官方相邻HTP寄存器语义与原驱动交叉校验，缺专有GPU手册的适配成本仍高。
- 复用ma1co/qemu@1909382c0d3533051cead7fde70ca8e84807ee14的SysBus、MemoryRegion、qtest、GDB；只增加可选六组控制字段，独立build-sugilite，新增文件GPL-2.0-or-later。未引入其他GPU实现或测试框架，未复制社区模块初始化绕过。既有TCI/NAND补丁保留。
- 原libObj/grm_gles只作本地私有只读研究；已定位SMAPH-S30字符串、提交与完成等待，未分发专有代码。DMP官方介绍仅支持产品族/API背景，不作为Sony寄存器规范；官方qemu.c的CLCD也不替代sugilite。
- 无新增产品依赖。实际构建、模型覆盖/未知初值、测试与回退见`handoff/runs/20261023T004916Z-sugilite-model/FINDINGS.md`、`model-manifest.json`、`SESSION.md`。旧操作台二进制与配置保持不变。


## 2026-10-23｜sugilite命令构建与有界取指观察

- ma1co/qemu@1909382c0d3533051cead7fde70ca8e84807ee14，继续复用MemoryRegion、address_space_read、qtest、QMP/GDB；新增GPL-2.0-or-later取指观察器，单独build-sugilite-front，不并入MIT应用。仅格式/计数来自原构建函数；GPU执行合同缺失，拒绝自造写回/完成语义。适配成本仍高。
- Sony官方内核包仍为SHA256 f502295d086c9e523758b86dc27134d78004a487f8ffe052cfa7d78aa3051cfa，仅复用本地缓存；支持IRQ76和平台信息，不提供完整命令模型。原4.01 libObj/grm_gles专有材料只在本地只读分析，无复制分发。
- devkitPro/libctru@9b55eda44cf80b971503991e0c78f9bc8fe50425，根README为zlib式许可。仅缓存gpu.c、registers.h和README约54KiB作对照：FINALIZE编号/常量相似，但数据/头顺序和0x116/117用途不兼容，拒绝照搬执行器；未把其源码复制到QEMU或MIT产品。根LICENSE的404与实际README许可来源均留档。
- 沿用本机LLVM及Python标准库，无新分析/构建框架或工具安装。补丁、来源哈希、测试和回退见`handoff/runs/20261023T012044Z-sugilite-command/model-manifest.json`、`community-sources.json`、`SESSION.md`。默认操作台不变，未知性能/时序明确保留。
