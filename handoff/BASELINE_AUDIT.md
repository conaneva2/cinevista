# 基线审计与独立复跑记录

日期：2026-09-19。对象：已提供的 `CineVista_Native_Persistence_v0.6_20260919.zip`。这次只形成交接材料，不改变已有产品实现。

## 1．可复核基线

- 原ZIP SHA256：`f7d160e018d0c0ccbe41822cfa60692b4f8a5c96e889fce7cfffe4d49507feb0`。
- 原ZIP共有191个文件；其中190个文件由原 `MANIFEST.sha256` 覆盖。核验190/190通过。
- 所有191个原文件与新交接包同路径文件逐字节比较相同；新资料仅追加。
- 原包未发现字体文件、APK、JKS/keystore/PEM/key文件；交接没有加入这些内容。
- 完整逐文件比对：`evidence/baseline-file-comparison.json`。

## 2．本次实际执行

在独立工作副本执行，避免脚本覆盖原包中的历史证据。新日志仅放本目录 `evidence/`。

| 命令 | 退出码 | 结果与范围 |
|---|---:|---|
| `python3 tools/cv.py doctor` | 0 | 环境诊断运行；无SDK可构建资格 |
| `python3 tools/cv.py check` | 0 | 主机/规范/源码语法回归通过 |
| `python3 tools/cv.py android` | 2 | doctor发现缺API10 jar、aapt、zipalign、apksigner、d8.jar而阻断；未开始真实APK编译 |
| `python3 tools/cv.py release-check` | 2 | 14项必需门禁unknown、工具链未完成资格；按预期阻断 |

环境是Linux x86_64 / Python3.13.5 / OpenJDK21.0.11 / Node22.16.0。不是用户Mac，不是JDK17/21远端CI验证。未连接USB/相机、未新增APK、未复跑浏览器交互。

主机check实际包括49项Node颜色/契约测试、23项工程规范测试、44项Java测试（其中1项包含10000随机案例）、3000组Java/Python几何对照、14项Python测试，以及17个相机Java文件的语法解析。语法解析明确没有Android类型解析。测试数量不换算为相机成功概率。

## 3．实际源码约束与后续变更入口

### A01：JNI仍被纯Java探针检查禁止

`tools/check_app_source.py` 扫描并拒绝 `Backup_write/Backup_sync_all` 文本；`tools/inspect_apk.py` 拒绝所有 `lib/` 文件。v0.6文档已允许受审查持久化研究，但检查器仍处于无JNI阶段。应在真正引入已审查库时扩展构建profile与白名单，而不是立刻全局放开。

新检查必须拒绝未批准ABI/库/来源、伪装Sony实现类和不明写入。代码文本检查只是辅助，不能当完整二进制安全审计。

### A02：一些测试永久断言“没有实现”

`tests/tools/test_native_persistence_contract.py` 当前对生产JSON直接断言 implemented=false、模型=false、profiles=[]、固件=null、门禁unknown，并对界面断言“发布器尚未完成”。这是基线快照，不适合随着实现完成永久保留。

改法：固定旧基线fixture继续测历史状态；生产状态用证据驱动一致性约束。只有实现+匹配报告满足时允许true；假verified、空报告、不匹配机身仍必须失败。不能通过删除测试假装完成，也不能坚持原断言导致项目无法前进。

### A03：发布门禁尚只是最低文件存在检查

`tools/release_check.py` 检查state、evidence非空和文件存在、工具链qualification。它不完整验证证据语义/身份/hash；`optional_features` 尚未按启用功能执行。下一阶段需升级数据schema、相对路径边界、哈希/构建/机型/固件/计划绑定及人工验收来源。存在一张图片文件不等于图像内容证明成功。

### A04：设备和文件系统读数不完整

`sony/.../DeviceProbe.java` 固件行仍为NOT READ；显示像素比例来自运行时报值，不是光学校准。`ImageProbeActivity` 输出仍用标准Android外部存储目录，只处理自制人工靶。这不代表Sony照片卷、原生回放或高分辨率管线已经打通。

### A05：源码是探针，不是正式相机UI

Manifest为`0.4-probe`、versionCode4、debuggable=true；捕获每次页面访问一张；Guide按未验证fit假设画框。升级时新增源确认、真实显示校准和产品状态机，不直接删除“UNVERIFIED”文字。

### A06：固定日志文件可能覆盖历史

`tools/doctor.py` 写`evidence/environment-v0.4.json`；构建/测试也写固定结果名。本次特意在隔离副本跑。继续开发时先建独立运行目录；若重构证据结构，同时更新消费者，不能伪造历史日期。

### A07：版本锁和远端CI未完成资格

toolchain qualification=false，部分分发hash/null和依赖版本待实际鉴定。`.github`是配置文件，不是已经在GitHub启用的分支保护或CI成果。新增构建产物上传/签名保存时不要将私钥暴露给不可信PR。

### A08：复用和原生模型大部分仍是计划

Recipe Lab在台账里adopt，但included_code=false；Film Studio只读研究，原生模型/发布器未有实现。现有Studio software-LUT可继续编辑，但不得改名伪装原生预览。所有已研究/已导入/已编译/已机测要分级记录。

## 4．基线和新证据的关系

`evidence/v0.6/`属于上一轮；`handoff/evidence/`属于本次交接复跑。两者都没有硬件通过记录。原SHA清单只描述原包，`HANDOFF_MANIFEST.sha256`覆盖新增交接后的全包。交接加入文档不升级相机版本，不引入任何新的颜色或持久化能力。
