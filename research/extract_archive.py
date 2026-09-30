"""Recover agents that are packaged inside notebooks as gzip/base64 tarballs.

Some Kaggriculture notebooks ship the submission archive as an inline blob rather
than a `%%writefile` cell. This extracts the archive and unpacks it to disk so
the exact submitted bytes can be validated.
"""
import base64
import gzip
import io
import json
import hashlib
import os
import re
import sys
import tarfile
import zlib


def blobs_from_cell(src):
    out = []
    for m in re.finditer(r"""(['"'])([A-Za-z0-9+/=\s]{200,}?)\1""", src, re.S):
        out.append(m.group(2).strip())
    return out


def try_decode(s):
    for dec in ("b64", "b85"):
        try:
            raw = base64.b64decode(s) if dec == "b64" else base64.b85decode(s)
        except Exception:
            continue
        for stage in ("raw", "gzip", "zlib"):
            try:
                data = raw if stage == "raw" else (
                    gzip.decompress(raw) if stage == "gzip" else zlib.decompress(raw))
            except Exception:
                continue
            if data[:2] == b"\x1f\x8b":
                try:
                    data = gzip.decompress(data)
                except Exception:
                    pass
            if data[:2] == b"\x1f\x8b" or data[:4] == b"PK\x03\x04" or len(data) > 1000:
                return dec, stage, data
    return None


def main(path, outdir):
    nb = json.load(open(path, encoding="utf-8"))
    os.makedirs(outdir, exist_ok=True)
    found = 0
    for i, c in enumerate(nb.get("cells", [])):
        if c.get("cell_type") != "code":
            continue
        src = "".join(c.get("source", []))
        for s in blobs_from_cell(src):
            r = try_decode(s)
            if not r:
                continue
            dec, stage, data = r
            h = hashlib.sha256(data).hexdigest()
            p = os.path.join(outdir, f"cell{i}_{dec}_{stage}.bin")
            open(p, "wb").write(data)
            print(f"  cell {i}: {dec}/{stage} -> {len(data)} bytes  {h[:16]}  {p}")
            if data[:2] == b"\x1f\x8b":
                try:
                    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
                        for m in tf.getmembers():
                            if m.isfile():
                                m.name = os.path.basename(m.name)
                                tf.extract(m, outdir)
                                print(f"      unpacked {m.name} ({m.size} bytes)")
                                found += 1
                except Exception as exc:  # noqa: BLE001
                    print(f"      (gzip but not a tar: {exc})")
    if not found:
        print("  no archive members recovered")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])