# QEMU source-only experimental patch set

Base: [ma1co/qemu](https://github.com/ma1co/qemu/tree/1909382c0d3533051cead7fde70ca8e84807ee14), commit 1909382c0d3533051cead7fde70ca8e84807ee14 (QEMU 5.1.0 lineage).

This directory preserves the emulator source changes from the local research environment. It contains no Sony firmware, proprietary code, binaries, RAM images, graphics assets or device logs. Apply the seven patches in filename order to the exact base source; review before using another QEMU version.

| Patch | Scope | License |
|---|---|---|
| 0001-tci-nonexec-buffer.patch | Non-executable bytecode buffers only when CONFIG_TCG_INTERPRETER is enabled; native TCG policy unchanged | LGPL-2.1-or-later |
| 0002-nand-persistence.patch | Virtual NAND program/erase persistence; flush before existing completion path | GPL-2.0-or-later |
| 0003-sugilite-control.patch | Optional limited clock/reset MMIO model; no graphics execution or interrupts | GPL-2.0-or-later |
| 0004-sugilite-frontend.patch | Optional RAM command-format observer; no opcode side effects, DMA writes, rendering or completion | GPL-2.0-or-later |
| 0005-nand-reset-profile.patch | Previously tested single-bank reset plus opt-in native IRQ/reset-mask profile; Sony reset defaults remain unverified | GPL-2.0-or-later |
| 0006-nand-config-ecc-guard.patch | Four verified writable configuration latches and opt-in refusal of unmodeled ECC transfers; no ECC execution or new completion | GPL-2.0-or-later |
| 0007-nand-memory-transaction-guard.patch | Refuse host-model memory transaction failures before normal completion; no guessed Sony fault bits or IRQs | GPL-2.0-or-later |

QEMU [LICENSE](LICENSE), [GPLv2](COPYING) and [LGPLv2.1](COPYING.LIB) are copied unmodified from the base. Existing notices remain in upstream files. translate-all.c credits Fabrice Bellard (2003); files without a specific license follow the QEMU root notice. Project-authored modifications: Copyright (c) 2026 CineVista contributors, under the corresponding per-file license above. The root CineVista MIT license does not override these licenses. Patches are dated 2026-10-22/25; no executable is redistributed here.

The graphics models are opt-in devices bionz_sugilite_ctrl and bionz_sugilite_frontend. Observed fetch is not execution. Power-on values and timing are not calibrated against physical hardware. NAND tests cover synthetic controller-level media only, not ECC, bad blocks, Sony FTL, mounted Android /data or APK persistence.

test_nand_persistence.py is an archived project-authored MIT host test. It expects a privately prepared fixture and QEMU under .local; it is not a standalone installer and is not run automatically. It creates synthetic media; never point experimental storage commands at physical devices or valuable images. Proprietary boot inputs are intentionally absent.

Remaining blockers include the GPU completion contract, window service, native storage initialization and APK lifecycle validation. No assertions are disabled and no artificial GPU-completion signals are implemented.

For R29 storage research, explicitly set `-global bionz_nand.strict-ecc=on`. ECC-enabled DMA/PIO reads then terminate with an unsupported-model diagnostic before touching buffers/media or producing completion. This is a research boundary, not an emulation of Sony hardware error reporting. The legacy default remains compatible with archived synthetic non-ECC tests and must not be used as ECC validation. Configuration registers reset to deterministic lab zeros; physical power-on defaults and codeword layout are not established. Native boot probes additionally use the experimental `native-irq` and `reset-irq-enable` properties; these are not promoted to hardware facts.

R36 reproduced false completion for unmapped main/extra destinations and a read-only descriptor. Patch 0007 checks QEMU MemTxResult on descriptor fetch/writeback, data destination writes and program-source reads. A failure terminates the model with a diagnostic; earlier writes are not rolled back. It does not implement Sony error status, ECC or bus timing. The isolated candidate passed five memory-fault cases plus normal-transfer and strict-ECC controls with guest CPUs paused. No full firmware boot was run.

All seven patches apply to the pinned source; the resulting NAND source matches the tested local source. Five of the six patched source files match the current local tree. The local tree also contains a pre-existing bootcon serial-backend routing change outside this patch series, so the entire local build is not claimed to be reproduced by this series alone. The NAND tests use a multiplexed serial backend. No binaries are distributed.
