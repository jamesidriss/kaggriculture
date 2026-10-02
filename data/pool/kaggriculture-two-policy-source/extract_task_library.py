"""Extract the task library from an authorized local Observed main.py.

This utility does not download data or grant redistribution rights. Keep the
result outside public notebook outputs and public datasets.
"""
import argparse,ast,base64,json,zlib
from pathlib import Path

def extract(path, output):
    tree=ast.parse(Path(path).read_text())
    sources=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name)and t.id=='_CO30_SOURCES'for t in n.targets))
    expert=ast.parse(zlib.decompress(base64.b85decode(sources[1])).decode())
    assignment=next(n for n in expert.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='_DATA'for t in n.targets))
    blob=next(n.value for n in ast.walk(assignment.value)if isinstance(n,ast.Constant)and isinstance(n.value,str))
    library=json.loads(zlib.decompress(base64.b85decode(blob)))
    if len(library)!=24 or not all(set(r)=={'actions','states','tasks'}and len(r['actions'])==719 for r in library):
        raise ValueError('This is not the expected Observed task library')
    Path(output).write_text(json.dumps({'observed_56713902_009_010':blob}))
    return len(library)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('main_py',type=Path);parser.add_argument('private_output',type=Path)
    args=parser.parse_args();print('Reference episodes:',extract(args.main_py,args.private_output))
