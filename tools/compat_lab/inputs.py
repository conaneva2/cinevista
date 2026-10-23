"""Local input verification; never download or regenerate pins implicitly."""
import hashlib
import json
import re
from .vm import Method, Unsupported


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_inputs(root, config):
    for name, expected in config['files'].items():
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()): raise Unsupported('input outside repository')
        if not path.is_file() or digest(path) != expected: raise Unsupported('missing or changed pinned input: ' + name)


def load(root, config):
    verify_inputs(root, config)
    methods = {key: Method.parse((root / spec['path']).read_text(), spec['path'], spec['signature'])
               for key, spec in config['methods'].items()}
    hierarchy = {}
    for name in config['hierarchy_files']:
        text = (root / name).read_text()
        child = re.search(r'^\.class .* (L[^;]+;)$', text, re.M)[1]
        parent = re.search(r'^\.super (L[^;]+;)$', text, re.M)[1]
        hierarchy[child] = parent
    return methods, hierarchy
