#!/usr/bin/env python3
"""Loopback-only console for bounded, fixed offline QEMU experiments.

No USB backend, arbitrary shell, APK execution or firmware framebuffer is
implemented. The camera-shaped controls currently operate the host console.
"""
import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import secrets
import signal
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'tools/virtual_camera_ui'


def safe_asset(path):
    return {'/': 'index.html', '/style.css': 'style.css', '/app.js': 'app.js'}.get(path)


def boot_status(serial, running):
    lines = set(serial.replace('\r', '').splitlines())
    error = any(x in serial for x in ('Entering exception monitor.', 'Kernel panic', 'Out of memory:'))
    completed = 'CV_LAB_DONE' in lines
    return {
        'state': 'stopped_at_error' if error else 'running' if running else 'probe_finished' if completed else 'off',
        'linux': 'CV_STORAGE_LAB_READY' in lines,
        'ulogio': 'ULOGIO_INSMOD_STATUS=0' in lines,
        'dmm': 'DMM_INSMOD_STATUS=0' in lines,
        'ma': 'GRM_MA_INSMOD_STATUS=0' in lines,
        # These require explicit independent acceptance evidence. Neither driver
        # success nor a short quiet log constitutes Android or APK success.
        'android': False, 'apk': False, 'firmware_buttons': False,
        'error': error, 'completed': completed,
    }


class Console:
    def __init__(self, root=ROOT):
        self.root = root
        self.config = json.loads((root / 'config/virtual-camera.lock.json').read_text())
        self.process = None
        self.output = None
        self.log = None
        self.user_stopped = False
        self.lock = threading.Lock()
        self.token = secrets.token_urlsafe(24)

    def running(self):
        return self.process is not None and self.process.poll() is None

    def start(self):
        with self.lock:
            if self.running():
                raise ValueError('模拟器已经在运行。')
            if not (self.root / '.local/CAMERA_WRITE_HOLD').exists():
                raise ValueError('缺少相机操作暂停标记，已停止。')
            for name, digest in self.config['inputs'].items():
                p = self.root / name
                if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != digest:
                    raise ValueError('实验输入缺失或已变化：' + name)
            name = 'console-' + time.strftime('%Y%m%dT%H%M%S') + '-' + secrets.token_hex(3)
            runner = self.root / self.config['runner']
            self.output = runner.parent / name
            command = [sys.executable, str(runner), name, '110',
                       str(self.root / self.config['commands']), *self.config['flags']]
            if self.log:
                self.log.close()
            self.log = (runner.parent / (name + '.host.log')).open('w')
            self.user_stopped = False
            self.process = subprocess.Popen(command, cwd=self.root, stdin=subprocess.DEVNULL,
                                            stdout=self.log, stderr=self.log, start_new_session=True)

    def stop(self):
        with self.lock:
            if self.running():
                self.user_stopped = True
                # This group belongs only to this console run. SIGINT allows
                # the bounded runner's finally block to close its sockets.
                os.killpg(self.process.pid, signal.SIGINT)
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(self.process.pid, signal.SIGKILL)
                    self.process.wait(timeout=2)
            if self.log:
                self.log.close()
                self.log = None

    def status(self):
        serial = ''
        if self.output and (self.output / 'serial.log').exists():
            serial = (self.output / 'serial.log').read_text(errors='replace')
        result = boot_status(serial, self.running())
        result.update(token=self.token, profile=self.config['profile'], running=self.running(),
                      session=self.output.name if self.output else None)
        # Keep real lines only, excluding the kernel's long loading spinner.
        lines = [re.sub(r'[\x00-\x08\x0b-\x1f]', '', line) for line in serial.splitlines()
                 if len(line) < 300]
        result['log'] = '\n'.join(lines[-65:])
        if not result['error'] and not result['running']:
            if self.user_stopped:
                result['state'] = 'stopped_by_user'
            elif self.process is not None:
                if self.process.poll() != 0:
                    result['state'] = 'host_error'
                elif not result['completed']:
                    result['state'] = 'probe_incomplete'
        return result


def serve(port):
    console = Console()

    class Handler(BaseHTTPRequestHandler):
        def reply(self, status, data, kind='application/json; charset=utf-8'):
            body = json.dumps(data, ensure_ascii=False).encode() if isinstance(data, dict) else data
            self.send_response(status)
            self.send_header('Content-Type', kind)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; frame-ancestors 'none'; object-src 'none'")
            self.end_headers()
            self.wfile.write(body)

        def allowed(self):
            return self.headers.get('Host') == '127.0.0.1:' + str(self.server.server_port)

        def do_GET(self):
            if not self.allowed():
                return self.reply(403, {'error': '仅接受本机入口。'})
            if self.path == '/api/status':
                return self.reply(200, console.status())
            asset = safe_asset(self.path)
            if not asset:
                return self.reply(404, {'error': '没有此入口。'})
            kind = {'html': 'text/html', 'js': 'text/javascript', 'css': 'text/css'}[asset.rsplit('.', 1)[1]]
            self.reply(200, (ASSETS / asset).read_bytes(), kind + '; charset=utf-8')

        def do_POST(self):
            origin = self.headers.get('Origin')
            expected = 'http://127.0.0.1:' + str(self.server.server_port)
            if not self.allowed() or origin not in (None, expected) or self.headers.get('X-Console-Token') != console.token:
                return self.reply(403, {'error': '请从本机控制台操作。'})
            if self.path not in ('/api/start', '/api/stop') or self.headers.get('Content-Length', '0') != '0':
                return self.reply(400, {'error': '不支持此操作。'})
            try:
                console.start() if self.path.endswith('start') else console.stop()
                self.reply(200, console.status())
            except (ValueError, OSError) as exc:
                self.reply(409, {'error': str(exc)})

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print('虚拟相机控制台：http://127.0.0.1:' + str(server.server_port), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        console.stop()
        server.server_close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='本地 A7R II 模拟器实验控制台')
    parser.add_argument('--port', type=int, default=8765)
    serve(parser.parse_args().port)
