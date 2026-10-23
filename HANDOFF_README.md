# 幕野 CineVista｜交接包入口

交接日期：2026-09-19。工程基线v0.6；相机0.4-probe；Studio软件原型0.2。**不包含APK，不是相机成品。**

## 交给Codex

将本文件所在的 `cinevista-pmca/` 作为项目工作目录，把 `CODEX_START_PROMPT.md` 的内容粘贴给Codex。

完整说明看 `CODEX_HANDOFF.md`；任务细分看 `handoff/EXECUTION_BACKLOG.md`；相机配合步骤看 `handoff/DEVICE_TEST_CARD.md`（必须等实际APK和安全前置就绪后）。

本包已包含v0.6全部源码与既有文档，不需再合并任何旧工程ZIP。191个原文件逐字节保留；新增交接资料与独立主机复跑日志。没有修改相机代码，没有加入未经许可的Film Studio代码或素材。

`MANIFEST.sha256` 是原v0.6的清单；`HANDOFF_MANIFEST.sha256` 是交接后完整清单（不含清单自身）。这两份清单用途不同，不要把原清单当新增文件已经被它覆盖。

Mac可用系统 `shasum -a 256 -c HANDOFF_MANIFEST.sha256` 核对文件。校验通过只证明包内文件完整，不证明机身兼容。
