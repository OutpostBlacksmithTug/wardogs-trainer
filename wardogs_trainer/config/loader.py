from pathlib import Path
import tomli

DEFAULTS = {
    "game": {"process_name": "WARDOGS.exe", "offsets_file": "config/offsets.json"},
    "runtime": {"tick_ms": 50},
    "features": {
        "godmode": {"enabled": True},
        "infinite_ammo": {"enabled": True},
        "esp": {"enabled": False, "draw_distance": 350.0},
        "aimbot": {"enabled": False, "fov": 12.0, "smoothing": 3.0, "bone": "head"},
    },
}


def _merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path: Path) -> dict:
    if not path.exists():
        return DEFAULTS
    with path.open("rb") as fh:
        data = tomli.load(fh)
    return _merge(DEFAULTS, data)