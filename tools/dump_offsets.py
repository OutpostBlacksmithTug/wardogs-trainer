"""Helper script: dump a candidate offset table to config/offsets.json."""

import json
import sys
from pathlib import Path

from wardogs_trainer.core.attacher import ProcessAttacher
from wardogs_trainer.core.memory import MemoryReaderWriter


def main() -> int:
    attacher = ProcessAttacher(process_name="WARDOGS.exe")
    attacher.attach()
    mem = MemoryReaderWriter(attacher.handle)
    print(f"attached pid={attacher.pid} base=0x{mem.base_address:X}")

    table = {
        "build": sys.argv[1] if len(sys.argv) > 1 else "unknown",
        "player_base": hex(mem.base_address),
    }
    out = Path("config/offsets.json")
    out.write_text(json.dumps(table, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    attacher.detach()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())