"""Export exact readable V8 sources and deterministic release archives.

Apache-2.0. Local release tooling by sunyuxiang136, 2026-09-24.
Only the frozen V8 source is accepted; no agent code executes during export.
"""
import ast
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile
import zipfile

EXPECTED_MAIN = "d760ace37153218546ef8219db4de5ea93f69e70c48b573cc37ee000f3e0228d"
EXPECTED_BASE = "4a0dc99bbd066930faeb60bcde08ca27ddfc73e54bd04b603ca6b643746b280c"


def digest(content):
    return hashlib.sha256(content).hexdigest()


def export(folder):
    folder = Path(folder).resolve()
    source = (folder / "main.py").read_bytes()
    if digest(source) != EXPECTED_MAIN:
        raise ValueError("This exporter requires the original frozen V8 main.py")
    tree = ast.parse(source)
    compile(tree, "main.py", "exec")
    values = {node.targets[0].id: ast.literal_eval(node.value)
              for node in tree.body if isinstance(node, ast.Assign)
              and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
              and node.targets[0].id in {"_BASE_SOURCE", "_GUARD_SOURCE"}}
    if digest(values["_BASE_SOURCE"].encode()) != EXPECTED_BASE:
        raise ValueError("Embedded parent identity changed")
    readable = {"readable/base_policy.py": values["_BASE_SOURCE"].encode(),
                "readable/guard_policy.py": values["_GUARD_SOURCE"].encode()}
    for text in values.values():
        for node in ast.walk(ast.parse(text)):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id == "exec" and node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)):
                content = node.args[0].value.encode()
                readable[f"readable/embedded_{digest(content)[:16]}.py"] = content
    for name, content in readable.items():
        compile(content, name, "exec")
        target = folder / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    names = ["main.py", "LICENSE.txt", "NOTICE.txt", "README.md", "export_v8.py"] + sorted(readable)
    payload = {name: (folder / name).read_bytes() for name in names}
    manifest = {"release": "opening-stock-feedback-v8", "main_sha256": EXPECTED_MAIN,
                "strategy_modified_for_publication": False, "license": "Apache-2.0",
                "files": [{"path": name, "sha256": digest(content), "bytes": len(content)}
                          for name, content in sorted(payload.items())]}
    manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode()
    (folder / "SOURCE_MANIFEST.json").write_bytes(manifest_bytes)
    payload["SOURCE_MANIFEST.json"] = manifest_bytes
    compressed = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=compressed, mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.USTAR_FORMAT) as archive:
            for name in ("main.py", "LICENSE.txt", "NOTICE.txt"):
                info = tarfile.TarInfo(name)
                info.size = len(payload[name])
                info.mode = 0o644
                info.mtime = 0
                archive.addfile(info, io.BytesIO(payload[name]))
    archive_bytes = compressed.getvalue()
    (folder / "submission.tar.gz").write_bytes(archive_bytes)
    payload["submission.tar.gz"] = archive_bytes
    zipped = io.BytesIO()
    with zipfile.ZipFile(zipped, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(payload.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 24, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    (folder / "opening_stock_v8_source.zip").write_bytes(zipped.getvalue())
    with tarfile.open(folder / "submission.tar.gz") as archive:
        if archive.getnames() != ["main.py", "LICENSE.txt", "NOTICE.txt"]:
            raise ValueError("Unexpected submission files")
        if archive.extractfile("main.py").read() != source:
            raise ValueError("Archive changed the strategy source")
    return {"main_sha256": EXPECTED_MAIN, "submission_sha256": digest(archive_bytes),
            "source_zip_sha256": digest(zipped.getvalue()), "readable_modules": len(readable)}


if __name__ == "__main__":
    print(json.dumps(export(Path(__file__).resolve().parent), indent=2))
