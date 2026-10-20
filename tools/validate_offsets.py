import json
import sys
from pathlib import Path

REQUIRED = {
    "build", "player_base", "health", "armor",
    "ammo_primary", "ammo_reserve",
    "entity_list", "entity_size", "entity_health",
}


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "config/offsets.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = REQUIRED - data.keys()
    if missing:
        print(f"missing keys: {sorted(missing)}", file=sys.stderr)
        return 1
    print(f"{path}: ok ({len(data)} keys, build={data['build']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())