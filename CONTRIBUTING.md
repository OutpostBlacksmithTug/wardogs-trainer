# Contributing to WARDOGS Trainer

Thanks for your interest. This is a community-driven single-player trainer for
WARDOGS. Contributions that add new feature handlers, update offsets for
new game builds, or improve the overlay integration are welcome.

## Layout

- `wardogs_trainer/bootstrap/` — attach + run loop
- `wardogs_trainer/core/` — process attacher, memory R/W, offset loader
- `wardogs_trainer/handlers/` — one file per cheat feature (godmode, aimbot, esp, ...)
- `wardogs_trainer/services/` — cross-cutting scanners (entity scanner, ...)
- `wardogs_trainer/models/` — typed state objects (player, entity)
- `wardogs_trainer/utils/` — logger, geometry, ntdll syscall wrappers
- `config/` — default TOML + per-build offsets JSON

## Adding a feature

1. Subclass `BaseHandler` under `wardogs_trainer/handlers/`.
2. Register it in `bootstrap/runtime.py::attach`.
3. Add the option block to `config/default.toml`.
4. Add a unit test under `tests/` using `FakeMem`.

## Updating offsets

When WARDOGS ships a new build:

1. Dump the new offsets into `config/offsets.json` under a new `build` value.
2. Update `core/memory.py::_module_base` if the IL2CPP base changed.
3. Open a PR titled `offsets: <version>`.

## Style

- Python 3.10+, `from __future__` not required.
- Line length 100, black-compatible formatting.
- Handlers must never raise out of `tick()` — swallow `OSError` and log.

## Reporting issues

Attach the `--verbose` log. Do NOT attach memory dumps of WARDOGS to the
public tracker; DM a maintainer instead.