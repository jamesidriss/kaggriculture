"""Artifact registry: digest-addressed identity, licence and provenance gating.

The single most valuable invariant in the whole audit was that identity is the
content digest. Filenames lie, labels collide, and directories get stale; a
SHA256 over normalised source does not.
"""
import csv
import hashlib
import json
import os


class Agent:
    """One registered artifact. Immutable once registered."""

    def __init__(self, name, path, sha256, size, author="", license_="",
                 source="", verbatim=False, lineage="", league_eligible=True,
                 reason="", notes=""):
        self.name = name
        self.path = path
        self.sha256 = sha256
        self.size = size
        self.author = author
        self.license = license_
        self.source = source
        self.verbatim = verbatim
        self.lineage = lineage
        self.league_eligible = league_eligible
        self.reason = reason
        self.notes = notes

    @property
    def short(self):
        return self.sha256[:16]

    def __repr__(self):
        return f"<Agent {self.name} {self.short} {'ok' if self.league_eligible else 'INELIGIBLE'}>"

    def read(self):
        path = self.path
        if os.path.isdir(path):
            path = os.path.join(path, "main.py")
        return open(path, "rb").read()

    def normalised_digest(self):
        """Digest that ignores line-ending differences.

        A CRLF copy of an LF agent is the same agent. Without this, a Windows
        checkout silently produces a phantom second entry and a fake 24/24
        tie, which is exactly the contamination this registry exists to stop.
        """
        return hashlib.sha256(
            self.read().decode("utf-8", "replace").replace("\r\n", "\n").encode()
        ).hexdigest()

    def verify(self):
        """Recompute the digest from disk. Returns a list of problems."""
        p = []
        path = self.path
        # A registry path may name either the artifact file or the
        # digest-addressed directory that contains it.
        if os.path.isdir(path):
            path = os.path.join(path, "main.py")
        if not os.path.exists(path):
            return [f"{self.name}: file missing at {self.path}"]
        raw = open(path, "rb").read()
        got = hashlib.sha256(raw).hexdigest()
        if got != self.sha256:
            p.append(f"{self.name}: digest drift, recorded {self.sha256[:12]} "
                     f"but file is {got[:12]}")
        if len(raw) != self.size:
            p.append(f"{self.name}: size drift, recorded {self.size} "
                     f"got {len(raw)}")
        return p


def digest_of(path):
    raw = open(path, "rb").read()
    return hashlib.sha256(raw).hexdigest(), len(raw)


class Registry:
    """A collection of agents loaded from a JSON config and/or a CSV manifest."""

    FIELDS = ["name", "path", "sha256", "size", "author", "license", "source",
              "verbatim", "lineage", "league_eligible", "reason", "notes"]

    def __init__(self, config_path=None):
        self.agents = {}
        self.config = {}
        if config_path:
            with open(config_path, encoding="utf-8") as fh:
                self.config = json.load(fh)
            self.load_config(config_path)
            # Manifest paths are relative to the CONFIG, like agent paths.
            # Resolving them against the process CWD made the framework only
            # work when launched from the repository root.
            base = os.path.dirname(os.path.abspath(config_path))
            for man in self.config.get("manifests", []):
                p = man if os.path.isabs(man) else os.path.normpath(
                    os.path.join(base, man))
                if not os.path.exists(p):
                    raise FileNotFoundError(
                        f"manifest declared in {config_path} not found: {p}")
                self.load_manifest(p)

    # ---- loading ---------------------------------------------------------
    def add(self, name, path, **kw):
        sha, size = digest_of(path)
        kw.setdefault("league_eligible", True)
        a = Agent(name=name, path=path, sha256=sha, size=size, **kw)
        self.agents[a.name] = a
        return a

    def load_config(self, path):
        base = os.path.dirname(os.path.abspath(path))
        for e in self.config.get("agents", []):
            e = dict(e)
            p = e.pop("path")
            e["verbatim"] = bool(e.get("verbatim", False))
            e["league_eligible"] = bool(e.get("league_eligible", True))
            e["license_"] = e.pop("license", "")
            if not os.path.isabs(p):
                p = os.path.normpath(os.path.join(base, p))
            self.add(e.pop("name"), p, **e)

    def load_manifest(self, path):
        for row in csv.DictReader(open(path, encoding="utf-8")):
            self.agents[row["name"]] = Agent(
                name=row["name"], path=row["path"],
                sha256=row["sha256"], size=int(row.get("bytes") or row.get("size") or 0),
                author=row.get("author", ""), license_=row.get("license", ""),
                source=row.get("source", ""),
                verbatim=row.get("verbatim", "") in ("yes", "true", "True"),
                lineage=row.get("lineage", ""),
                league_eligible=row.get("league_eligible", "yes") in ("yes", "true", "True"),
                reason=row.get("reason", ""), notes=row.get("notes", ""),
            )

    # ---- invariants ------------------------------------------------------
    def problems(self):
        """Every reason a league built from this registry is not trustworthy."""
        p = []
        for a in self.agents.values():
            p += a.verify()
        # duplicate content
        by_raw, by_norm = {}, {}
        for a in self.agents.values():
            by_raw.setdefault(a.sha256, []).append(a.name)
            by_norm.setdefault(a.normalised_digest(), []).append(a.name)
        for d, names in by_raw.items():
            if len(names) > 1:
                p.append(f"byte-identical agents: {names} ({d[:12]})")
        for d, names in by_norm.items():
            if len(names) > 1 and len(set(names)) > 1:
                p.append(f"identical modulo line endings: {names} ({d[:12]})")
        # provenance on league-eligible agents
        for a in self.agents.values():
            if not a.league_eligible:
                continue
            if not a.license.strip():
                p.append(f"{a.name}: league-eligible but no licence declared")
            if not a.author.strip() or a.author.strip().upper() == "UNKNOWN":
                p.append(f"{a.name}: league-eligible but author unknown")
            if not a.source.strip():
                p.append(f"{a.name}: league-eligible but no source URL/ID")
        return p

    def verify(self, strict=True):
        p = self.problems()
        for x in p:
            print(f"  {'FAIL' if strict else 'warn'}  {x}")
        if not p:
            print(f"  registry OK: {len(self.agents)} agents, all digests and "
                  f"provenance intact")
        return p

    # ---- access ----------------------------------------------------------
    def eligible(self):
        return [a for a in self.agents.values() if a.league_eligible]

    def get(self, name):
        if name in self.agents:
            return self.agents[name]
        # tolerate a digest prefix or a unique substring
        hits = [a for a in self.agents.values()
                if a.sha256.startswith(name) or name in a.name]
        if len(hits) == 1:
            return hits[0]
        raise KeyError(f"{name!r} matches {len(hits)} agents; use a full name "
                       f"or digest")

    def lineages(self):
        out = {}
        for a in self.eligible():
            out.setdefault(a.lineage or "UNKNOWN", []).append(a.name)
        return out
