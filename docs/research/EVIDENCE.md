# 证据与资料索引

更新：2026-10-23。本页用于回答“这个结论在哪得到、是什么级别的证据、怎么继续核对”。原厂材料、详细反汇编、运行日志和私人环境不公开；因此公开读者可以核对方法、来源和文件身份，但不能只凭本仓库独立复跑全部固件实验。

## 本地研究记录的检索表

本地维护者按 `handoff/runs/<run-id>/` 查找 `FINDINGS.md`、`SESSION.md` 和表中结果文件。以下路径是检索编号，不是公开下载链接。公开副本故意不提供这些原始目录。

| ID | run-id / 主题 | 关键证据文件或对象 | 支持范围 |
|---|---|---|---|
| R01 | `20261022T021116Z-video-encoder-feasibility` | 录像入口、Sony 字节码、原生调用 | 排除未经证明的直接替换输入办法；静态 |
| R02 | `20261022T032031Z-rec-pin-dsp-geometry` | `evidence-manifest.json`、端口配置与发送读取 | RecPin 映射、动态连接机制、DSP/SCALE 区别；静态 |
| R03 | `20261022T034123Z-movie-peer-scale-backend` | 原模式表、MovieEncoder 请求、SDF 工厂/队列 | 特定录像模式接收端、真实缩放后端；静态 |
| R04 | `20261022T073608Z-sdf-lifecycle-emulator` | `evidence-manifest.json`、ownership/resize-flow | 票据/YC/像素生命周期、时序缺口；静态 |
| R05 | `20261022T075951Z-install-boot-lab` | 场景结果、方法轨迹、替身清单 | 24 个有条件回放/故障注入案例；不是整机运行 |
| R06 | `20261022T084735Z-qemu-first-boot` | boot probe、串口与检查记录 | 原内核 + 实验根实际进入 shell |
| R07 | `20261022T091300Z-qemu-storage-android` | `test_nand_persistence.py`、NAND 补丁、Android 记录 | 控制器跨进程持久性、Android 服务实际停点 |
| R08 | `20261022T100302Z-a7rii-board-alignment` | `native-assertion.json`、原保留内存与启动对照 | 原 backup/bootin/im/libObj 推进；未完成 Android |
| R09 | `20261022T225823Z-gl-common` | 原指令断点、消息返回与日志区依赖 | -1020/-9999/-2 各层错误定位 |
| R10 | `20261022T235438Z-ulogio-emulator` | 暖启动恢复清单、原驱动/池创建观察 | 匹配日志配置与有限初始化通过 |
| R11 | `20261023T002402Z-sugilite-window` | 输入/字体/图形分组实验 | 窗口表面及原 GPU 上电断言停点 |
| R12 | `20261023T004916Z-sugilite-model` | `sugilite-control.patch`、控制检查与客体记录 | 有限 MMIO 模型、原驱动加载；无执行完成 |
| R13 | `20261023T012044Z-sugilite-command` | `sugilite-frontend.patch`、三次提交、前端检查 | 4×8 字节首包与只读取指解包 |
| R14 | `20261023T015609Z-sugilite-semantics` | DWARF/符号、只读断点、293 项寄存器枚举对照 | 首包空同步提交及 128 字节对象用途 |
| R15 | `20261023T055215Z-boss-gpu-protocol` | `protocol-evidence.json` | BOSS 加载/邮箱/握手的 CPU 侧规则；静态 |
| R16 | `20261023T061322Z-boss-fingerprint` | `wbi-module-header.json`、`fingerprint-results.json` | 52 字节设备信息来源、有限搜索阴性、fence 消费端 |
| R17 | `20261023T090601Z-pica-memory-contract`；`20261023T093109Z-cache-state-contract` | 寄存器对应、屏障与 `state-evidence.json` | 54 个对应位置、部分状态位及 Sony 缓存语义冲突 |
| R18 | `20261023T114711Z-loader-source-delta` | `delta-evidence.json` | pformat 输入、safe_list 生成、写入依赖 |
| R19 | `20261023T121316Z-config-driver-origin` | `actual-driver-comparison.json`、`a6000-driver-origin.json` / `rx100v-driver-origin.json` | 三机原驱动比较、更新包命名载荷清单 |
| R20 | `20261023T123445Z-dmp-library-comparison` | `library-comparison.json`、`evidence-audit.json`、`adjacent-evidence.json`、`validation.json` | 三机原库、62+56 项静态核查、离线重读及保护哈希 |
| R21 | `20261023T132539Z-ma-window-contract` | `contract-evidence.json`、`functions.json`、`mapping-01/operand-buffer.json`、`validation.json` | MA/stream 缓存属性、原生实际映射、窗口管理区及私有格式；45 项核查与一次只读客体观察 |
| R22 | `20261023T135110Z-native-window-server` | `server-links.json`、`server-evidence.json`、`window-01/window-observation.json`、`validation.json` | 原生管理区注册/线程/命令1–2；39 项核查与一次首提交顺序观察 |
| R23 | `20261023T140711Z-native-submit-cache` | `cache-01/cache-observation.json`、`cache-01/result.json`、`record-review.json`、`validation.json` | 首包提交到等待的已记录顺序；MA cache入口读取E14、观察器失败，不支持“没有缓存调用”结论 |
| R24 | `20261023T142814Z-ma-cache-location` | `context-evidence.json`、`locations-01/result.json`、`context-01/context-observation.json`、`validation.json` | 原MA入口位置、用户/内核调试上下文对照与限定窗口零命中；两轮客体、50项核查，非GPU完成证明 |
| R25 | `20261023T144549Z-boss-candidate-provenance` | `candidate-provenance.json`、`candidate-evidence.json`、`goal-audit.json`、`validation.json` | 两个WBI候选匹配ARSC数组、ODEX命中为字符串索引；26项核查，剩余弱候选未认证，完整目标仍受阻 |
| R26 | `20261023T150817Z-a6000-new-leads` | `new-evidence.json`、`boss-driver-comparison.json`、`driver-origin.json` / `driver-offline.json` | A6000原BOSS协议/4.01 PBM差异、SA外壳、43项静态与保护核查；协议模型仍候选 |
| R27 | `20261023T153511Z-boss-operation-contract` | `operation-inventory.json`、`contract-evidence.json`、`boot-evidence.json`、`boot-control-01` / `boot-profile-01`、`validation.json` | 18类操作归属、PBI布局、76项静态检查及两次隔离启动；初始坏块指针无效，GPU/BOSS仍未完成 |
| R28 | `20261023T160247Z-boot-input-origin` | `snapshot-search.json`、`recovered-inputs.json`、`input-evidence.json`、`init-replay-01`、`validation.json` | 恢复20+200字节原参数副本，原驱动回放生成匹配52字节信息；53项检查、一次限定初始化启动，非完整存储/Android |
| R29 | `20261023T162612Z-nand-ecc-contract` | `FINDINGS.md`、`evidence.json`、`config-before-03`、`config-after-01`、`validation.json` | 四配置读回修复；55项核查、六组控制器测试；ECC拒绝边界、BOSS页组布局；挂载仍未通过 |
| R30 | `20261023T225319Z-ecc-raw-layout` | `FINDINGS.md`、`extract_and_audit.py`、`evidence.json`、`public-search.json` | 54项静态核查；extra布局、状态0边界、DMA等待及Cadence差异；无新启动，BOSS仍缺 |
| R31 | 20261024T021006Z-extra-consumers | FINDINGS.md、audit_consumers.py、evidence.json、public-search.json | 39项静态核查；逻辑块/LTU/循环代次、ECC归一化与逐项筛选；无新启动，BOSS仍缺 |
| R32 | 20261024T022834Z-extra-flags-dma | FINDINGS.md、audit_flags_dma.py、evidence.json、dma-test-result.json、new-sources.json | 53项静态核查、5项CPU暂停控制器用例；bit1/2恢复分支、DMA参数、Spectra差异；无新固件启动 |

静态检查数只是该轮断言数量，不是功能覆盖率。每轮 validation 要与其检查对象一起读；主机检查退出码 0 不覆盖 Sony 窗口、Android 桌面或真实相机。

早期入口 `20261023T130029Z-memory-window-contract` 仅有符号清单；后续行为核查和运行观察在 R21，不能混用两轮结果。文档整理与同步记录在 `20261023T130744Z-research-handbook-publication`。


## 原文件身份：只发布摘要，不发布载荷

以下为 SHA-256，用于辨别是否在讨论同一文件。相同哈希不证明另一机型的硬件、配置或整个系统兼容。

| 文件 / 固件 | SHA-256 |
|---|---|
| A7R II 4.01 `grm_gles.ko` | `bfd931f314a3fabfb83ee9e5e7bb2bc1b3324f26d8b3557acd4a23e22aa87ace` |
| A6000 3.21 `grm_gles.ko` | `b040ded8b712dcb4a2396ee39ddd6db24974265782feef877c7957e434853233` |
| RX100 V 2.00 `grm_gles.ko` | `10201a4e74dd927c05cb78d0979967edc269929c7e67c57dde66d3a1c74237d9` |
| 4.01 / RX100 V `libDMPSUGIRM.so` | `f6ab83b7cf0402908f9c0be5a261d81e299a978887a9061749ddea9a1caefeb6` |
| 4.01 / RX100 V `libEGL_dmp.so` | `670255dc1d4c3869ea55e0df0a4e378b5b5aa2072a6b18f4c8ed2c51bbc651ec` |
| 4.01 / RX100 V `libGLESv2_dmp.so` | `d9b10cc2fcbb018eeaf462b510dc294318eab77159049f633811c006105c40a9` |
| A6000 `libDMPSUGIRM.so` | `29249bfc99516cd66529e94220d4dc521c89ccaea696b8b2605e430463f85834` |
| A6000 `libEGL_dmp.so` | `f1b26d4f11f862f0cbcff43ea2421750df56f0fa3eb47f1a24fd5881b6ed2ac2` |
| A6000 `libGLESv2_dmp.so` | `633f8b3041c4b51ad744dec807a42ef9f14fdd5cf958d70d1666426622c627ce` |
| A7R II 4.01 `lld.ko` | `4f6768b6d58be7d08bae896a2400edbaf9739a1f147ad6bd8f34aebc64302cff` |
| A6000 3.21 `lld.ko` | `113c1b1f97ef2339b804c88d8924bc5ac7acc81f775fe4ccf27da73625e6840e` |
| A7R II 4.01 `nand.ko` | `679e3dddafc4fa5808565bb627c22942b443ab7c732badf7a9287b5026cb239b` |
| A6000 3.21 `nand.ko` | `2169b84deee1a424539255affbdff499c4094e0913eeefe49339f3d47cbe6faa` |

A6000 六库与固定公开清单匹配。RX100 V 三库与已有 4.01 原文件做了整文件比较。外机输入用官方更新包的小范围读取，保留范围长度、ETag、分块解密和 FDAT 头检查，并进行禁网离线重读；没有验证外机完整更新 EXE 签名/整个包 CRC，不能用这些范围缓存刷机。

## 官方与原作者资料

这些是已用于研究的来源，不是自动下载清单。优先复用已固定的本地文本；滚动网页应记录新查阅日期。链接到上游不表示本项目重新许可或验证了上游全部内容。

| 来源 | 用途与边界 |
|---|---|
| [Sony A7R II 帮助指南](https://helpguide.sony.net/ilc/1520/v1/en/index.html)；[后背部件](https://helpguide.sony.net/ilc/1520/v1/en/contents/TP0001097508.html) | 交互布局与官方使用说明，不提供 GPU 寄存器协议 |
| [Sony 许可说明](https://helpguide.sony.net/ilc/1520/v1/fr/contents/TP0001077616.html) | 固件包含多种许可；GPL/LGPL 告知不使整个固件变成开源 |
| [Sony A6000 更新入口](https://support.d-imaging.sony.co.jp/www/cscs/firm/?area=jp&lang=jp&mdl=ILCE-6000)；[RX100 V 更新入口](https://support.d-imaging.sony.co.jp/www/cscs/firm/?area=jp&lang=jp&mdl=DSC-RX100M5) | 分别固定 3.21、2.00 原厂输入；不自动获取整包 |
| [OpenMemories 硬件记录](https://openmemories.readthedocs.io/hardware.html) | 平台/处理器线索，与原固件核对；不是 Sony 官方时序规范 |
| [iFixit 原始拆机](https://www.ifixit.com/Teardown/Sony+a7R+II+Teardown/45597) | 芯片标识与物理布局；不能由外观推断完整容量/主频 |
| [QEMU Arm 系统仿真文档](https://www.qemu.org/docs/master/system/target-arm.html) | 板型、外设与固件的关系；滚动文档不取代固定源码 |
| [EGL_KHR_fence_sync](https://registry.khronos.org/EGL/extensions/KHR/EGL_KHR_fence_sync.txt) | 完成可见性与 `0x30f2` 的标准含义；没有 Sugilite IRQ 寄存器规则 |

## 社区项目：固定版本与取舍

| 项目 / 固定提交 | 贡献或线索 | 采用边界 |
|---|---|---|
| [ma1co/qemu · 1909382c](https://github.com/ma1co/qemu/tree/1909382c0d3533051cead7fde70ca8e84807ee14) | BIONZ/CXD90014、BOSS/NAND 板级基础 | 实际构建基线；公开补丁按原文件 GPL/LGPL 许可，缺专有启动输入 |
| [ma1co/OpenMemories-CI · 4f8c6367](https://github.com/ma1co/OpenMemories-CI/tree/4f8c6367a75e9afd02bc684425e3fbff424b2223) | RX100M5 更新/内核测试及所需输入列表 | 不是 A7R II 正常 Android 桌面通过记录 |
| [frozencaviar/OpenMemories-CI · 423179bd](https://github.com/frozencaviar/OpenMemories-CI/tree/423179bd095abeb3280a43d6848645fce58cfa57) | A7R II 4.01 电源、存储、启动实验 | 逐项比较；不采用跳错、假返回或未证实中断修复 |
| [ma1co/fwtool.py · cdba742b](https://github.com/ma1co/fwtool.py/tree/cdba742b73eed5981480c326aeb30033aabf0223) | 容器、解密、LZ77、ext2/WBI 研究工具 | MIT 工具用于私有输入分析；不随手册分发固件或解密载荷 |
| [OpenMemories-Framework · f8df3504](https://github.com/ma1co/OpenMemories-Framework/tree/f8df3504d8684433a331ee869e64f67cc8be9730) | Sony API 封装及普通 Android dummy 思路 | MIT；替身不能当原机硬件行为 |
| [nzzlinh/A6000 研究 · 72dd5904](https://github.com/nzzlinh/sony-a6000-firmware-research/tree/72dd59048b5d17a3c6cddfe3a1874680d0b2d286) | 文件哈希与同代平台资料 | 脚本 MIT、文档 CC BY 4.0；只按来源核对，不把原厂材料视为 MIT |
| [nicolvus/A6000 · 2ebc1436](https://github.com/nicolvus/a6000-fw-decomp/tree/2ebc1436e026be4611ed373ecad4b53c16b63f3d) | 原作者日志、符号/ELF 元数据 | 只读事实，未采用代码；公共日志不是本机独立复现 |
| [JEF1056/RX100V · 83616a6d](https://github.com/JEF1056/RX100V-Firmware/tree/83616a6dca6ea8b7a7ef701506ea298e2f50f9cc) | 同代存储与研究入口 | 作者 MIT 材料范围；布局不可直接套用，原库另取自官方包 |
| [Azahar · ac4a97e2](https://github.com/azahar-emu/azahar/tree/ac4a97e27723a501fbd79db75e94a5a8b3cbb8b1)；[libctru · 9b55eda4](https://github.com/devkitPro/libctru/tree/9b55eda44cf80b971503991e0c78f9bc8fe50425) | PICA 寄存器/命令比较 | GPLv2-or-later / zlib 式许可；位置对应不等于 Sony 语义，未移植完成逻辑 |
| [Panda3DS · 92e53d26](https://github.com/wheremyfoodat/Panda3DS/tree/92e53d26b898eb89d865f8407460900a88e7c0fa) | 另一 PICA 模型 | GPLv3；有限完成近似不作 Sony 硬件规范，未采用实现 |
| [fujihack/ffqemu · 1be303f1](https://github.com/fujihack/ffqemu/tree/1be303f1300880252786d42441f53e1e6b8c4609) | X-T5 SMAPH-H 模型 | 所查根目录/文件无明确许可，且协议不同；仅事实比较，不复制 |
| [A7C II Tools 研究 · 78278564](https://github.com/QAQLeonard/a7c2-fl23-research/tree/782785641ca9f8b984940c7274b48706219e0da4) | 修改与服务入口恢复的条件 | 新代码 MIT，原厂派生另计；不同 SoC，不能证明 A7R II 可恢复 |
| [A7S III 归档报告 · 6ba9ac62](https://github.com/oxunjonuz/aiodam-sony-a7siii-firmware-audit/blob/6ba9ac6285526e14d52cd3ce97a6be4666431ff0/ROUND_278.md) | 另一代 `nor_loader.tar`/pformat 来源线索 | 报告 CC BY 4.0、原创代码 MIT；未取得其原归档，不能构造本机配置 |

这些结论是对指定版本、指定片段的审阅，后续更新不能自动继承本次许可或技术判断。Film Studio、Recipe Lab 等应用对照的完整取舍保留在[复用台账](../01_REUSE_AUDIT.md)；默认非商用材料不能并入本项目 MIT 代码。

## 证据可复核规则

1. 先固定型号/固件/文件 SHA-256，再讨论地址。ELF VMA、模块 `.text` 偏移、文件偏移、运行地址不可混用。
2. 函数名需由符号、重定位、调用与日志等交叉确认；“最近公共符号”不是函数归属证明。
3. 分开保存输入身份、分析方法、原观察、结论与未验证项。阴性检索必须说明目录、容器、字节范围和匹配规则。
4. 复用其他机型时同时记录一致处和差异；共同消费者不能补出未知生产者。
5. 分享技术事实和自有工具前检查来源许可；不得把带 hash 的专有文件误认为可以公开分发。

R21 补充来源：本地既有 Sony 官方 GPL 内核包（SHA-256 `f502295d086c9e523758b86dc27134d78004a487f8ffe052cfa7d78aa3051cfa`），只取页保护、DMA、内存映射和打开标志相关文件；AOSP `android-4.1.2_r1` 的 gralloc.h 与 graphics.h，Apache-2.0 告知保留于私有来源缓存。两份文本共 13,816 字节；URL 与文件摘要在 R21 的 public-inputs.json。仅引用接口事实，未引入其实现。

R26新增固定资料：[nicolvus A6000启动缺口](https://github.com/nicolvus/a6000-fw-decomp/blob/f4dc706262de807f6a9502cd5abc37af469747e0/docs/boot-and-recovery.md)、[NEX-3N项目的DSP代际对照](https://github.com/pylypenko-pavlo/nex3-filmgrain-project/blob/4b5f95b0a5a8481825e85a8034bbadff863e7751/notes/sony-dsp-generations.md)、[unixtract FDAT解析](https://github.com/theubusu/unixtract/blob/51e50742e6bcbc8381de2fad8f4d4d1f2074d9f6/src/formats/fdat/mod.rs)。A6000原厂输入仍取Sony官方3.21更新包，整包签名/CRC未验，仅固定范围与原文件hash比对；输入哈希与全部限制保存在私有R26记录。未复制上述项目代码或发布原厂数据。
