# Security Policy

WARDOGS Trainer is an **external, single-player only** trainer. It is intended
for the offline campaign and private lobbies. Using it in online multiplayer
is against the game's ToS and is explicitly out of scope for this project.

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.4.x   | yes       |
| < 1.4   | no        |

## Reporting a vulnerability

Please do **not** open a public issue for a security problem. Email the
maintainers listed in `pyproject.toml` or open a private security advisory
on the GitHub repo.

In scope:

- Arbitrary code execution via malformed `config/*.toml` or `offsets.json`.
- Privilege escalation through the `utils/syscalls.py` NT wrappers.
- DLL / package hijacking in the packaged release.

Out of scope:

- VAC / EAC / BattlEye detection of the trainer (this is external and only
  intended for single-player).
- Anti-cheat bypasses, spoofer requests, or online-game functionality.
- "My game got banned" reports from using this in multiplayer.

## Responsible use

You are responsible for how you run this tool. Read the disclaimer in
`README.md`. The maintainers will not help patch around anti-cheat.