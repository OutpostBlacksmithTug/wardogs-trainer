from pathlib import Path

from wardogs_trainer.core.offsets import OffsetTable


def test_load_offsets_table():
    table = OffsetTable.load(Path("config/offsets.json"))
    assert table.build.startswith("1.0.")
    assert table["health"] == 0x1A4
    assert table["player_base"] == 0x02A4F1C0
    assert table.get("missing_key", 0xDEAD) == 0xDEAD