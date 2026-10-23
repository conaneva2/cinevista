# 相机集中操作卡｜T03故障恢复暂停

当前：A7R II（用户菜单确认4.01）黑屏循环重启，恢复未完成。安装后至今没有通过的应用启动/原生取景测试。

## 本轮相机前操作

保持关机、取出电池。刚才的被动观察已结束，不需要再开机、插卡或尝试组合键。保存原片与存储卡；不格式化。

官方通用电源复位已试，无效。修正USB工具的第二次观察中用户确认通电，102次有效快照未捕捉Sony。安装、固件升级、模式切换与任意恢复写入继续暂停。

## 最新观察与复盘

用户确认USB已拔掉、仅靠电池，OFF后仍重复数次。本轮只核查历史命令、安装器控制流和固件静态实现；没有再次监听或要求开机。安装/同步收尾异常与资源兼容故障仍并列；未刷固件不等于安装不改变启动相关状态。最新记录：`handoff/runs/20260920T024526Z-install-forensic-review/FINDINGS.md`。

## 已发现与待确认

官方ILCE-7RM2 4.01固件已在Mac离线解包。启动器IconCache.cacheLocked在loadIcon后无保护地强转BitmapDrawable；原安装APK的图标是XML layer-list，存在具体类型不兼容。该静态缺陷是循环重启的重要嫌疑，但缺相机崩溃日志与恢复验证，不能宣称已确认根因或硬件损坏。原APK继续隔离，没有生成或安装修正版。

下一步是查验恢复通道与最小卸载可行性；主机兼容性修复不能替代故障机恢复。旧基础探针操作卡已存入`handoff/runs/20260920T022824Z-firmware-offline-analysis/DEVICE_TEST_CARD_BEFORE.md`，不是当前可执行步骤。

详细调查：`handoff/runs/20260920T022824Z-firmware-offline-analysis/FINDINGS.md`。
可交给维修方的事实说明：`handoff/runs/20260920T022824Z-firmware-offline-analysis/RECOVERY_NOTE.md`；尚未外发。
