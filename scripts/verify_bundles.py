"""Verify every bundle of a run and record it in the run manifest.

Usage (pinned interpreter, isolated):
  /mnt/d/Minotaur/worktrees/fresh/.venv/bin/python -I verify_bundles.py RUN_DIR [--expect-unsigned]
  /mnt/d/Minotaur/worktrees/fresh/.venv/bin/python -I verify_bundles.py --bundle TAR ONNX [--expect-unsigned]

Per bundle: the server's own read_bundle() checks pass; sha256(brain.onnx inside the tar) equals
manifest.brain_id and the manifest's file entry; it equals sha256 of the seed's brain.onnx on disk
(the file scripts/eval_brain.py scores); if an arena-check-2 result exists for that seed, its sha256
matches too. With --expect-unsigned, a signature.json fails the check. Results go into
RUN_DIR/manifest.json under "bundles" (bundle sha256 included) and are printed as a table.
Exit 1 on any mismatch.
"""
import hashlib, json, os, sys
from pathlib import Path


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def check(tar: Path, onnx: Path, ac2: Path | None, expect_unsigned: bool) -> dict:
    from minotaurus.bundle import BundleError, read_bundle
    data = tar.read_bytes()
    row = {"bundle": str(tar), "bundle_sha256": sha(data), "onnx_on_disk": str(onnx)}
    try:
        b = read_bundle(data)
    except BundleError as exc:
        row.update(read_bundle="FAIL: " + str(exc), match=False)
        return row
    inside = sha(b.files["brain.onnx"])
    entry = next(e.sha256 for e in b.manifest.files if e.name == "brain.onnx")
    disk = sha(onnx.read_bytes())
    row.update(read_bundle="ok", onnx_sha256_in_tar=inside, manifest_brain_id=b.manifest.brain_id,
               manifest_entry_sha256=entry, onnx_sha256_on_disk=disk, signer=b.signer)
    ok = inside == b.manifest.brain_id == entry == disk
    if ac2 is not None and ac2.is_file():
        row["eval_sha256"] = json.loads(ac2.read_text())["sha256"]
        ok = ok and row["eval_sha256"] == disk
    if expect_unsigned and b.signer is not None:
        row["unsigned_check"] = "FAIL: bundle is signed"
        ok = False
    row["match"] = ok
    return row


def main():
    args = sys.argv[1:]
    unsigned = "--expect-unsigned" in args
    args = [a for a in args if a != "--expect-unsigned"]
    rows = []
    if args[0] == "--bundle":
        rows.append(check(Path(args[1]), Path(args[2]), None, unsigned))
        manifest = None
    else:
        run = Path(args[0])
        for seed_dir in sorted(run.glob("**/seed-*")):
            tars = sorted(seed_dir.glob("bundle*.tar"))
            if not tars:
                rows.append({"bundle": f"{seed_dir}: NO BUNDLE", "match": False}); continue
            n = seed_dir.name.split("-")[1]
            rows.append(check(tars[0], seed_dir / "brain.onnx", run / f"ac2-s{n}.json", unsigned))
        manifest = run / "manifest.json"
    print("| bundle | onnx sha (in tar) | manifest sha | onnx on disk | match |")
    print("|---|---|---|---|---|")
    for r in rows:
        f = lambda k: (r.get(k) or "-")[:12]
        print(f"| {r['bundle']} | {f('onnx_sha256_in_tar')} | {f('manifest_brain_id')} | {f('onnx_sha256_on_disk')} | {r['match']} |")
    if manifest is not None and manifest.is_file():
        d = json.loads(manifest.read_text()); d["bundles"] = rows
        tmp = manifest.with_suffix(".tmp"); tmp.write_text(json.dumps(d, indent=2)); os.replace(tmp, manifest)
    sys.exit(0 if all(r["match"] for r in rows) else 1)


if __name__ == "__main__":
    main()
