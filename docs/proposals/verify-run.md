# DRAFT PR (b): one local verify command (bundles + pool overlap)

Status: draft proposal only. Not opened, not sent, not implemented. Branch `feat/verify-run` off
pinned `dc888a7` (local, not pushed) holds this note.

## Why

We run two helper scripts after every run, outside the package:
- `scripts/verify_bundles.py` checks bundles: manifest, sha256 and `brain_id`.
- `scripts/overlap_check.py` checks that no training pool shares a layout with the held-out sets.

Both use only public package functions:
- `minotaurus.bundle.read_bundle`
- `minotaurus.engine.generate.generated_level_from_id`
- `minotaurus.engine.pools.walls`
- `ConfigFile.resolve_pools`

One documented command would let anyone repeat the same checks without our scripts.

## Proposed command

```
minotaurus verify-run RUN_DIR [--config CONFIG.json] [--against SET.json ...]
                              [--expect-unsigned] [--json OUT.json]
```

Usage text (as `--help` would print it):

```
Usage: minotaurus verify-run RUN_DIR [OPTIONS]

  Check a finished training run: every seed's bundle, and (with --config and
  --against) that no practice/check/test maze shares a wall layout with a
  held-out maze set. Reads files only; never trains, scores or changes anything.

Bundles (always; every RUN_DIR/**/seed-*/):
  - the server's own read_bundle() checks pass;
  - sha256 of brain.onnx inside the tar == manifest brain_id
    == the manifest's file entry for brain.onnx == the seed's brain.onnx on disk.

Overlap (with --config and at least one --against):
  - rebuilds the config's practice/check/test pools with the installed generator;
  - rebuilds every maze in each SET.json from its id, checks the grid matches,
    and compares wall layouts with walls(), the function the pools use;
  - only maze ids and grids are read from SET.json, never any score.

Options:
  --config PATH        The run's config.json (seeds and parallel are ignored).
  --against PATH       A held-out maze set ({"<size>": [{"id", "grid"}, ...]}).
                       Repeatable, e.g. arena-check-2 and final-test.
  --expect-unsigned    Fail if any bundle carries a signature.json.
  --json PATH          Also write every check as JSON (nothing is written by default).

Exit codes: 0 all checks pass; 1 any mismatch or shared layout; 2 bad arguments
or unreadable file.
```

Example (our ladder):

```
minotaurus verify-run runs/F5/<time> \
  --config configs/ladder/approved/F5.json \
  --against protocol/arena-check-2-mazes.json \
  --against ~/minotaur-research/2026-11-25-head-to-head/final-test-mazes.json \
  --expect-unsigned
```

Output: one Markdown table per part (bundles: bundle, onnx sha in tar, manifest sha, on disk,
match; overlap: pool, mazes per size, shared per set). The last line is `OK` or `FAILED: <n>
problems`.

## Differences from today's scripts

- It does **not** edit `manifest.json`; `verify_bundles.py` does. Recording results stays our
  launcher's job, through `--json`.
- It does not check the `eval_brain.py` sha. That file is ours and not part of the package.
  `launch.sh` keeps that one extra check.
- The paths of the held-out sets are always passed in with `--against`, never hard-coded.

## Files it would touch upstream

- New `minotaurus/cli/verify_run.py`, one `app.command("verify-run", …)` line in
  `minotaurus/cli/__init__.py`, and a short TRAINING.md / README section.
- Tests: a good bundle passes, a tampered `brain.onnx` fails, a signed bundle fails with
  `--expect-unsigned`, and a set that shares a layout fails.
- `minotaurus/cli/` files other than train/check_brain/pack/sign/keygen are not on our drift watch
  list, but the TRAINING.md edit is. If it is merged, the drift guard reports CHANGED-RELEVANT. We
  stay pinned at dc888a7 until the owner decides.
