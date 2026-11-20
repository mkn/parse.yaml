#! /usr/bin/env python3
"""
mkn.manifest.yml for a parse.yaml release, see .github/workflows/release.yml

    manifest.py collect <out dir> <key> <mkn version>
        copies this build's libraries from bin/static and bin/shared into <out dir> with short names,
        and writes <out dir>/<os>-<arch>.json: per mode, the files with their sha256
    manifest.py merge <out file> <version> <commit> <fragment.json>...
        mkn.manifest.yml from every build's fragment

A key names what a binary needs to match, e.g. "os=nix;arch=x86_64;cxxrt=libstdc++;libc=manylinux_2_28".
maiken adds ";profile=<profile, @ for the top level>;mode=<static|shared>" to it.
"""

import hashlib
import json
import os
import shutil
import sys

NAME = "parse.yaml"
LIBS = (".a", ".so", ".dylib", ".lib", ".dll")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def collect(out, key, mkn):
    fields = dict(f.split("=", 1) for f in key.split(";"))
    stem = f"{NAME}-{fields['os']}-{fields['arch']}"
    os.makedirs(out, exist_ok=True)
    bins = {}
    for mode in ("static", "shared"):
        d = os.path.join("bin", mode)
        files = []
        for f in sorted(os.listdir(d)):
            ext = os.path.splitext(f)[1]
            if ext not in LIBS or not os.path.isfile(os.path.join(d, f)):
                continue
            name = f"{stem}-{mode}{ext}"
            shutil.copyfile(os.path.join(d, f), os.path.join(out, name))
            files.append({"file": name, "sha256": sha256(os.path.join(out, name))})
        if not files:
            sys.exit(f"no libraries in {d}")
        # profile=@: bin/static and bin/shared are the top level built in each mode
        bins[f"{key};profile=@;mode={mode}"] = files
    with open(os.path.join(out, f"{fields['os']}-{fields['arch']}.json"), "w") as f:
        json.dump({"mkn": mkn, "bins": bins}, f, indent=2)


def merge(out, version, commit, fragments):
    lines = ["format: 1", f"name: {NAME}", f"version: {version}", f"commit: {commit}", "bins:"]
    for path in fragments:
        with open(path) as f:
            fragment = json.load(f)
        for key, files in fragment["bins"].items():
            lines.append(f'  "{key}":')
            lines.append(f"    mkn: {fragment['mkn']}")
            lines.append("    files:")
            for file in files:
                lines.append(f"    - file: {file['file']}")
                lines.append(f"      sha256: {file['sha256']}")
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")


def main():
    if len(sys.argv) == 5 and sys.argv[1] == "collect":
        collect(*sys.argv[2:])
    elif len(sys.argv) >= 6 and sys.argv[1] == "merge":
        merge(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
