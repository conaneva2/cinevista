"""A7R II launcher gate over real aapt 30.0.3 dumps; no device access.

Conservative probe policy: direct plain PNG icons in every configuration,
Activity-only application, no explicit process or persistence declarations.
Unknown forms fail closed. aapt handles binary XML/resources and PNG decoding.
"""
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile
import zipfile


def sdk_aapt():
    sdk = os.environ.get('ANDROID_SDK_ROOT') or os.environ.get('ANDROID_HOME')
    if not sdk:
        raise ValueError('real Android SDK required for launcher inspection')
    return Path(sdk) / 'build-tools/30.0.3' / ('aapt.exe' if os.name == 'nt' else 'aapt')


def _run(aapt, *args):
    return subprocess.run([str(aapt), *map(str, args)], check=True,
                          capture_output=True, text=True).stdout


def _manifest_icons(text):
    stack = []
    icons = []
    applications = activities = 0
    for line in text.splitlines():
        element = re.fullmatch(r'(\s*)E: ([\w-]+) \(line=\d+\)', line)
        if element:
            depth, name = len(element[1]), element[2]
            while stack and stack[-1][0] >= depth:
                stack.pop()
            parent = stack[-1][1] if stack else None
            if name == 'application':
                if parent != 'manifest': raise ValueError('unexpected application nesting')
                applications += 1
            if parent == 'application':
                if name != 'activity':
                    raise ValueError('component outside Activity-only whitelist: ' + name)
                activities += 1
            stack.append((depth, name))
            continue
        attr = re.fullmatch(r'\s*A: ([\w:]+)(?:\(0x[0-9a-fA-F]+\))?=(.*)', line)
        if attr and stack:
            name, value = attr[1], attr[2]
            if name in ('android:process', 'android:persistent'):
                raise ValueError('explicit process/persistent declaration rejected')
            if name == 'android:icon':
                if not re.fullmatch(r'@0x[0-9a-fA-F]{8}', value):
                    raise ValueError('unsupported icon reference')
                icons.append((stack[-1][1], int(value[1:], 16)))
        elif line.strip() and not line.lstrip().startswith('N: '):
            raise ValueError('unsupported aapt manifest dump line: ' + line.strip())
    if applications != 1 or not activities or not any(n == 'application' for n, _ in icons):
        raise ValueError('application, activity and explicit application icon required')
    return sorted({rid for _, rid in icons})


def _icon_paths(text, ids):
    lines = text.splitlines()
    paths = set()
    seen = set()
    for i, line in enumerate(lines):
        match = re.match(r'\s*resource (0x[0-9a-fA-F]+) .*', line)
        if not match or int(match[1], 16) not in ids:
            continue
        seen.add(int(match[1], 16))
        if 't=0x03 ' not in line or i + 1 == len(lines):
            raise ValueError('unsupported icon resource (aliases and complex values rejected)')
        value = re.fullmatch(r'\s*\(string(?:8|16)\) "([^"\\]+)"', lines[i + 1])
        if not value:
            raise ValueError('unsupported icon resource value')
        path = value[1]
        if not re.fullmatch(r'res/(?:drawable|mipmap)(?:-[a-zA-Z0-9-]+)?/[a-z0-9_]+\.png', path):
            raise ValueError('icon must be direct plain PNG in every configuration: ' + path)
        paths.add(path)
    if seen != set(ids):
        raise ValueError('missing or unsupported icon resource')
    return sorted(paths)


def _reject_nine_patch(data):
    # PNG container inspection only; actual decoding is delegated to SDK aapt.
    if not data.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('icon is not PNG data')
    pos = 8
    while pos + 12 <= len(data):
        size = struct.unpack_from('>I', data, pos)[0]
        kind = data[pos + 4:pos + 8]
        if kind in (b'npTc', b'npLb', b'npOl'):
            raise ValueError('compiled NinePatch icon rejected')
        pos += size + 12
        if pos > len(data): raise ValueError('truncated PNG chunk')
        if kind == b'IEND':
            if pos != len(data): raise ValueError('trailing PNG data')
            return
    raise ValueError('missing PNG end')


def inspect_launcher(path, aapt=None):
    aapt = aapt or sdk_aapt()
    manifest = _run(aapt, 'dump', 'xmltree', path, 'AndroidManifest.xml')
    resources = _run(aapt, 'dump', '--values', 'resources', path)
    icons = _icon_paths(resources, _manifest_icons(manifest))
    with zipfile.ZipFile(path) as archive, tempfile.TemporaryDirectory() as temp:
        if len(archive.namelist()) != len(set(archive.namelist())):
            raise ValueError('duplicate ZIP entries')
        root = Path(temp); src = root / 'in'; out = root / 'out'
        (src / 'drawable').mkdir(parents=True); out.mkdir()
        for i, name in enumerate(icons):
            if name not in archive.namelist(): raise ValueError('icon file missing: ' + name)
            data = archive.read(name)
            _reject_nine_patch(data)
            (src / 'drawable' / f'icon_{i}.png').write_bytes(data)
        _run(aapt, 'crunch', '-S', src, '-C', out)
    return {'contract': 'cinevista.a7rii-launcher/1', 'icon_paths': icons,
            'components': 'activity-only', 'device_execution_verified': False}


if __name__ == '__main__':
    import sys
    try:
        print(json.dumps(inspect_launcher(sys.argv[1]), indent=2))
    except (ValueError, OSError, subprocess.CalledProcessError, zipfile.BadZipFile) as error:
        print('REJECTED:', str(error), file=sys.stderr)
        sys.exit(2)
