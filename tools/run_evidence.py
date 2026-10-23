"""Append-only evidence per invocation; inherited by child commands, never history."""
from datetime import datetime, timezone
from pathlib import Path
import os
import uuid
ROOT = Path(__file__).resolve().parents[1]

def run_dir():
    value = os.environ.get('CINEVISTA_RUN_DIR')
    if value:
        directory = Path(value).resolve()
    else:
        name = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-') + uuid.uuid4().hex[:8]
        directory = ROOT / 'evidence/runs' / name
        os.environ['CINEVISTA_RUN_DIR'] = str(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory

def write_evidence(name, text):
    if Path(name).name != name:
        raise ValueError('evidence name must be a basename')
    path = run_dir() / name
    with path.open('x', encoding='utf-8') as stream:
        stream.write(text)
    return path
