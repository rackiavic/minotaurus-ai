# DRAFT PR (c) design note: `train_every` and a preallocated replay buffer

Status: design note only. Not opened, not sent, not implemented. Branch `perf/replay-train-every`
off pinned `dc888a7` (local, not pushed) holds this note. It extends
`reports/drafts/friend-pr-note-speed.md`. **No benchmark runs while the ladder chain is active**;
the plan below runs only after the chain ends.

## Measured cost today (reports/benchmark-2026-11-26.md)

- Each step costs 1.89 ms alone and 2.9–3.1 ms with 6 seeds at once.
- `batch_size` 32 saves only 7%, so the time goes to fixed overhead on every step, not to the
  arithmetic.
- Every step calls `learn()` once (`minotaurus/trainer/dqn.py:137–143`).
- `learn()` rebuilds the batch from Python tuples (`dqn.py:120`).

## Change 1: preallocated replay buffer (no behaviour change)

- Today `remember()` (`dqn.py:100–112`) stores `(np.array obs, action, reward, np.array next,
  float done)` in a Python list ring. `learn()` (`dqn.py:114–120`) does
  `self.rng.sample(self.buffer, batch_size)` and then `np.array(col) for col in zip(*batch)`.
- Proposed: fixed arrays, allocated once in `__init__`, with `N = replay_size` and
  `L = obs_len`:
  - `obs[N,L]` float32, `nxt[N,L]` float32, `act[N]` int64, `rew[N]` float32, `done[N]` float32;
  - a write position `pos` and a fill count `size`.
- The batch: `idx = self.rng.sample(range(self.size), batch_size)`, then `obs[idx]` and so on.
- **Why the order stays the same:** `random.Random.sample(population, k)` picks positions from
  `len(population)` and the RNG state alone. For the same RNG state,
  `sample(range(n), k)` returns exactly the positions that `sample(list_of_n, k)` picks. Checked
  locally: 500 draws of 64 from 1,000, identical. The ring write order and the `pos` wrap stay as
  they are, so each position holds the same transition.
- **Why the values stay the same:**
  - obs and next obs are already float32.
  - Today the reward goes from a Python float, through a float64 array, to a float32 tensor. The
    new code rounds the same float64 to float32 once, at write time. That is the same single
    rounding.
  - Actions and done already become int64 and float32 tensors.
  - The tensors fed to the network are bit-identical.
- Memory: replay 50,000 × (2 × 82 × 4 + 8 + 4 + 4) bytes ≈ 33 MB, preallocated. Today the list of
  tuples of small arrays takes more than that, through per-object overhead.
- Out of scope: the imitation buffer (`demos`, `dqn.py:145–166`). We never use it.

## Change 2: `train_every` (documented setting, default 1 = current behaviour)

- `"dqn": {"train_every": k}`, an integer of at least 1 and **1 by default**.
- `step()` calls `learn()` only when `self.steps % k == 0`.
- `target_update` keeps counting **environment steps**, as today, so k = 1 is exactly today's code
  path.
- It is recorded in `config.json`, in `training_options` and in the `.onnx` `training` metadata,
  like the other DQN settings.
- **k > 1 changes learning:** it makes fewer gradient steps per try. For us it would be a new
  ladder rung under the protocol, never a speed setting. A config without the key, or with
  k = 1, must reproduce today's runs exactly.

## Same-seed equivalence test (must pass before any benchmark)

The test is to be added upstream with the PR and run locally. It is small: a CPU test of a few
seconds, not a benchmark.

1. **Unit, buffer:** fill the old list buffer and the new array buffer with the same 3 × N
   transitions, so the ring wraps. Give both the same `random.Random(seed)`, then draw 200
   batches. The sampled indices must be identical and the batch arrays `np.array_equal`.
2. **End to end, same seed:** train a small generated-maze config twice, once with the old buffer
   (kept as a test-only reference class) and once with the new one. Use seed 1, the r3 recipe, 2
   sizes and about 40 tries, with `eval_every` 10. Check that:
   - `metrics.jsonl` is **byte-identical**, including loss, success, `validation_success`,
     `validation_loops` and `exported_episode`;
   - the final network weights are `torch.equal`;
   - the `.onnx` bytes are identical, apart from any recorded timestamp.
3. **`train_every` default:** run the same config with no key and with `train_every: 1`. The
   outputs must be byte-identical to each other and to step 2.
4. **`train_every: 2`:** the number of gradient steps is half of the environment steps (± 1), and
   `target_update` still fires on environment-step counts.

Our local acceptance check on the pinned code adds two more:
- `logs/regress-dc888a7.json` must be reproduced unchanged;
- `eval_brain` must still reproduce B-mixed-s1 maze for maze (74.0%).

## Benchmark plan (AFTER the chain ends; owner approval first)

- Reuse `scripts/bench.sh` and the `configs/bench/` setup: r3 recipe, seed 1, 300 tries, nice 0.
  Run on a branch worktree, never `worktrees/fresh`.
- Batch A, uncontended: base (pinned), new buffer with k = 1, and new buffer with k = 2 and k = 4.
  One at a time.
- Batch B, contended: the same 4 arms plus base × 2, which makes 6 at once, the real ladder load.
- Report tries/min, steps/s, ms/step, worker RSS and minimum MemAvailable, as in
  `reports/benchmark-2026-11-26.md`.
- Pass bar for the buffer: k = 1 is identical in metrics to base (the equivalence test) and faster
  in ms/step.
- `train_every` > 1 is reported for speed only. Its wins at try 300 are secondary and decide
  nothing.
- Estimated time: about 8 min per uncontended arm, about 12 min for the contended batch, about
  45 min in all. Disk: under 100 MB.
- Nothing from the benchmark enters any rung. Adopting either change in a ladder run requires an
  upstream merge, a re-pin by the owner, and a re-run of the pre-run checks (protocol "Working
  root").
