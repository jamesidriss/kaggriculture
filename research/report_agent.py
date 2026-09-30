"""Report version strings and hashes for candidate agent artifacts."""
import hashlib
import re
import sys

for f in sys.argv[1:]:
    src = open(f, encoding="utf-8").read()
    h = hashlib.sha256(src.encode("utf-8")).hexdigest()
    v = re.search(r'__version__\s*=\s*["\']([^"\']+)', src)
    doc = src.lstrip()[:300].replace("\n", " ")
    print(f"{f}")
    print(f"   bytes   {len(src)}")
    print(f"   sha256  {h}")
    print(f"   version {v.group(1) if v else '(none)'}")
    print(f"   doc     {doc[:220]}")
    print()