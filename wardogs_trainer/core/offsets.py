import json
from pathlib import Path


class OffsetTable:
    def __init__(self, data: dict):
        self._data = data
        self.build = data.get("build", "unknown")

    @classmethod
    def load(cls, path: str | Path) -> "OffsetTable":
        with Path(path).open("r", encoding="utf-8") as fh:
            return cls(json.load(fh))

    def __getitem__(self, key: str) -> int:
        raw = self._data[key]
        return int(raw, 16) if isinstance(raw, str) else int(raw)

    def get(self, key: str, default: int = 0) -> int:
        if key not in self._data:
            return default
        return self[key]