# A7R II 固件留存与连接环境

> **故障未恢复，机身写入暂停。** 电源复位无效；纠正缺-l的问题后，用户确认通电的复测102次快照未捕捉Sony。离线发现原APK图标与4.01启动器类型约束不兼容，因果仍待日志。当前操作以故障恢复暂停卡为准。

本轮复盘加入仅电池OFF后仍重复的观察；已区分安装器成功进度与未确认的最终握手。断线因果尚未知，不把图标作为唯一原因。详见`handoff/runs/20260920T024526Z-install-forensic-review/FINDINGS.md`。

当前被动观察入口为`python3 tools/macos/observe_usb.py --seconds 10`，不导入PMCA/PyUSB、不打开USB接口；仅读取OS已有注册表。仅在与用户协调一次通电观察时运行；数据中不含序列号。


核查日期：2026-09-20。型号ILCE-7RM2，不是ILCE-7M2。

## 最新实测

A7R II实际MTP基础与扩展型号读取通过，model_code=0032828070。用户在机身菜单确认固件4.01（非工具精确读取）。PMCA原info重复初始化触发Access denied；单次包装会话查询成功，新增白名单只读适配入口与6项生命周期/反向测试。上游源码、系统安全设置均未修改。APK安装和启动仍未验证。

入口现在只用一次上游SonyMtpExtCmdDevice初始化，再读基础/扩展型号并关闭会话；不调用updater，不读序列号到输出，不吞掉权限错误。仅允许一台ILCE-7RM2及上游识别的Sony MTP协议，其他设备拒绝。firmware字段明确为not_queried。下方工具准备描述为历史。

## 官方固件

索尼中国目前提供4.01（2019-05-16）：[中文Mac下载说明](https://service.sony.com.cn/download/firm/00002733.html)。同时复核[索尼型号支持页](https://www.sony.com/electronics/support/digital-cameras-interchangeable-lens-cameras/ilce-7rm2)，仍列4.01。

当前离线分析副本：`.local/recovery-research/Update_ILCE7RM2V401.dmg`。旧下载路径本轮已不存在，已从同一Sony地址重新获取并核对先前哈希。

- 大小267199906字节。
- SHA256：`a72f8e3ad329ac8fdb916e9db1a82b02f6d0c9a698c130658d6ab7a7a5a5a1ed`。
- 官方中国页JSON返回下载地址，HTTPS重定向到di.update.sony.net；hdiutil verify内部校验通过。
- 此SHA256是本机计算值，不是与索尼公布SHA256对照；未验证安装器代码签名。本轮仅只读挂载镜像复制DAT后卸载；从未运行升级器。
- 中国支持页下载不等于跨地区中文解锁包，不能承诺把日版等机身改成中文菜单。
- 中国页只列macOS10.12–10.14，未列macOS27/Apple Silicon。因此本Mac的固件升级环境不能标为兼容或就绪。不安装旧内核驱动，不改SIP/Gatekeeper/启动安全策略。

固件升级需要海量存储器模式；下方应用连接使用MTP。两条路线不要混用。先读取现有版本，已经4.01无需重复升级。此次只下载留存，升级需另行明确操作范围并确认支持的宿主环境。

## 已准备的应用连接环境

- Python3.12.10 ARM64，独立venv：`.local/connection/venv`。
- 已存在的Homebrew libusb1.0.30 ARM64，实际PyUSB后端加载通过；没有安装系统驱动。
- Sony-PMCA-RE，MIT，上游`ma1co/Sony-PMCA-RE`，固定提交`a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0`，原源码无修改。
- CLI运行依赖已安装并冻结，见`config/camera-connection.lock.json`和本地requirements-qualified.txt；包归档留.local。未安装仅用于分发打包的PyInstaller、Windows依赖。
- pip首次证书链失败；使用现有`/etc/ssl/cert.pem`后成功。未使用trusted-host或关闭TLS校验，未修改全局证书/配置。
- `--help`、`info -d libusb`、`pip check`通过。info报告无设备且退出0，这是上游行为，不能解读为连接成功。

已审查范围是CLI分派、驱动装配、设备枚举、info和安装入口，不是完整工具安全认证。info在普通设备上读取相机信息，并调用updater.init/getFirmwareVersion查询；不是完全被动的USB描述符读取，但不调用固件写入。info在App安装模式有单独通信路径。未连接设备情况下只执行到枚举；实际协议/权限/安装尚待验证。

## 历史连接操作（故障期间暂停，不执行）

1. A7R II装充足电量电池，保留原照片与RAW设置；用可传数据的micro-USB线连接这台Mac。
2. 相机“USB连接”选择 **MTP**。关闭占用该相机的照片导入程序。macOS若正常询问是否允许USB附件，可允许这台相机。
3. 仓库根目录运行：

```sh
sh tools/macos/camera_info.sh
```

入口固定为白名单单会话MTP型号查询，并检查上游提交和跟踪源码无修改；拒绝额外参数。输出可能含序列号/GPS，仅保留本机，分享时脱敏。入口的保护不是通用沙箱；不要自行改为firmware/updatershell/serviceshell。

4. 记录型号、当前固件和USB模式；读取成功后，再明确安排开发APK安装。不要打开下载的固件升级器来测试MTP连接。

当前ILCE-7RM2的MTP型号查询已通过，用户菜单确认固件4.01；APK安装、字体/取景尚未验证。具体APK与相机集中步骤见[操作卡](../handoff/DEVICE_TEST_CARD.md)。
