"""Extract agent sources from Kaggle notebooks without executing notebook code.

Handles `%%writefile main.py` blocks, base85/zlib-encoded payloads, and plain
`def agent(` cells. Writes each artifact verbatim so SHA256 reflects the author's
exact bytes.
"""
import base64
import hashlib
import json
import os
import re
import sys
import zlib


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return h, len(text)


def strip_magic(src):
    lines = src.split("\n")
    if lines and lines[0].strip().startswith("%%"):
        return "\n".join(lines[1:])
    return src


def extract(nb_path, outdir):
    nb = json.load(open(nb_path, encoding="utf-8"))
    found = []
    for i, c in enumerate(nb.get("cells", [])):
        if c.get("cell_type") != "code":
            continue
        src = "".join(c.get("source", []))
        if not src.strip():
            continue

        # %%writefile main.py  -> the literal submission artifact
        m = re.match(r"\s*%%writefile\s+([\w\-./]+)", src)
        if m:
            name = os.path.basename(m.group(1))
            body = strip_magic(src)
            # Cell magic consumes the whole cell, so re-add the trailing newline
            # that IPython would have produced.
            if not body.endswith("\n"):
                body += "\n"
            p = os.path.join(outdir, name)
            h, n = write(p, body)
            found.append((p, h, n, i, "writefile"))
            continue

        # base85/zlib blobs
        if re.search(r"b85decode|zlib\.decompress", src):
            for j, blob in enumerate(re.findall(r'"""(.*?)"""', src, re.S)):
                s = blob.strip()
                if not s:
                    continue
                for dec in ("b85", "zlib_b85", "plain"):
                    try:
                        if dec == "b85":
                            data = base64.b85decode(s.encode())
                        elif dec == "zlib_b85":
                            data = zlib.decompress(base64.b85decode(s.encode()))
                        else:
                            data = base64.b64decode(s.encode())
                        t = data.decode("utf-8")
                        if "def agent" in t or "def agent(" in t:
                            p = os.path.join(outdir, f"decoded_c{i}_{j}_{dec}.py")
                            h, n = write(p, t)
                            found.append((p, h, n, i, dec))
                            break
                    except Exception:
                        continue

        # plain agent cells
        if re.search(r"^def agent\(", src, re.M) and "writefile" not in src[:60]:
            p = os.path.join(outdir, f"agent_cell_{i}.py")
            h, n = write(p, src)
            found.append((p, h, n, i, "plain"))

    for p, h, n, i, kind in found:
        print(f"  cell {i:3d} [{kind:9s}] {n:7d} chars  {h[:16]}  {p}")
    if not found:
        print("  no agent source found")
    return found


if __name__ == "__main__":
    for nb in sys.argv[1:]:
        out = os.path.join(os.path.dirname(nb), "extracted")
        print(f"=== {nb}")
        extract(nb, out)
        print()