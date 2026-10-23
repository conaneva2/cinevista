#!/bin/sh
# Fixed info-only entry point. No forwarding of arbitrary PMCA commands.
set -eu
if [ "$#" -ne 0 ]; then
    echo '此入口只读取设备信息，不接受安装、升级或其他参数。' >&2
    exit 2
fi
CV_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
CV_PMCA="$CV_ROOT/.local/connection/Sony-PMCA-RE"
CV_PYTHON="$CV_ROOT/.local/connection/venv/bin/python"
CV_COMMIT=a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0
if [ ! -x "$CV_PYTHON" ] || [ ! -d "$CV_PMCA/.git" ]; then
    echo '连接环境未配置；请阅读 docs/CAMERA_CONNECTION.md。' >&2
    exit 2
fi
if [ "$(git -C "$CV_PMCA" rev-parse HEAD)" != "$CV_COMMIT" ] || [ -n "$(git -C "$CV_PMCA" status --porcelain --untracked-files=no)" ]; then
    echo 'PMCA源码与已审查版本不符，停止连接。' >&2
    exit 2
fi
# Output may include a serial number; keep reports local.
exec "$CV_PYTHON" "$CV_ROOT/tools/macos/camera_info.py"
