from wardogs_trainer.handlers.godmode import GodModeHandler
from wardogs_trainer.models.player import PlayerState


class FakeMem:
    base_address = 0x140000000

    def __init__(self):
        self.values = {}

    def read_float(self, addr):
        return self.values.get(addr, 0.0)

    def write_float(self, addr, val):
        self.values[addr] = val


class FakeOffsets:
    def __init__(self):
        self.data = {"player_base": 0x1000, "health": 0x10, "armor": 0x14}

    def __getitem__(self, k):
        return self.data[k]


def test_godmode_tops_up_health():
    mem = FakeMem()
    player = FakeMem.base_address + 0x1000
    mem.values[player + 0x10] = 42.0
    mem.values[player + 0x14] = 10.0

    handler = GodModeHandler(mem, FakeOffsets(), {"enabled": True})
    handler.tick()

    assert mem.values[player + 0x10] == 100.0
    assert mem.values[player + 0x14] == 100.0


def test_player_state_apply_godmode():
    state = PlayerState(health=12.0, armor=8.0, ammo_primary=30, ammo_reserve=90, pos=(0, 0, 0))
    state.apply_godmode()
    assert state.health == 100.0 and state.armor == 100.0