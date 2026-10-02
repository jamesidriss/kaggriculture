"""Load policy constants without redistributing raw competition trajectories."""
import ast
import base64
import json
import os
from pathlib import Path
import zlib

ROOT = Path(__file__).resolve().parent
_VALUES = None
_UPSTREAM = None

def value(key):
    global _VALUES, _UPSTREAM
    if _VALUES is None:
        _VALUES = json.loads((ROOT / 'policy_parameters.json').read_text())
        private = os.environ.get('KAGGRICULTURE_PRIVATE_ASSETS')
        if private:
            _VALUES.update(json.loads(Path(private).read_text()))
    if key not in _VALUES:
        spec = json.loads((ROOT / 'dependency_spec.json').read_text()).get(key)
        if spec is None:
            raise FileNotFoundError('Observed Production requires its authorized 24-episode task library. See DATA_ACCESS.md; no substitute is silently used.')
        if _UPSTREAM is None:
            explicit = os.environ.get('KAGGRICULTURE_UPSTREAM_MAIN')
            paths = [Path(explicit)] if explicit else list(Path('/kaggle/input').rglob('main.py'))
            _UPSTREAM = []
            for path in paths:
                if path.is_relative_to(ROOT):
                    continue
                try:
                    for node in ast.walk(ast.parse(path.read_text())):
                        if isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value) > 1024:
                            _UPSTREAM.append(node.value)
                except (SyntaxError, UnicodeError):
                    continue
        matches = {v for v in _UPSTREAM if len(v) == spec['characters'] and v.startswith(spec['prefix'])}
        if len(matches) != 1:
            raise FileNotFoundError('Attach the documented upstream Kaggle notebook output, or set KAGGRICULTURE_UPSTREAM_MAIN. Required constant missing or ambiguous: '+key)
        _VALUES[key] = matches.pop()
    result = _VALUES[key]
    return ast.literal_eval(result['python_literal']) if isinstance(result, dict) and set(result) == {'python_literal'} else result

def source(relative_path, encoding):
    text = (ROOT / relative_path).read_text()
    if encoding == 'text':
        return text
    data = zlib.compress(text.encode())
    return (base64.b85encode(data) if encoding == 'b85z' else base64.b64encode(data)).decode()

def load_policy(name):
    if name not in ('observed_56713902', 'last_dance_56720309'):
        raise ValueError('Unknown policy')
    path = ROOT / 'policies' / (name + '.py')
    namespace = {'__name__': name, '__file__': str(path)}
    exec(compile(path.read_text(), str(path), 'exec'), namespace)
    return [v for v in namespace.values() if callable(v)][-1]
