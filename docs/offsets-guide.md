# Finding offsets for a new WARDOGS build

1. Attach Cheat Engine to `WARDOGS.exe`.
2. Scan for the local player health float (single-player: take damage,
   scan for `decreased value`, repeat).
3. Pointer-scan back to the module base to obtain `player_base`.
4. Offsets within the player struct are stable between builds — only
   `player_base` and `entity_size` typically shift.
5. Fill `config/offsets.json` and open a PR.

Common pitfalls:

- WARDOGS uses IL2CPP; the module base is fixed at `0x140000000`.
- Entity list is a contiguous array of structs — do NOT assume it's a
  pointer list.
- The build string must match the one in the game's `version.txt` or the
  trainer will refuse to load offsets.