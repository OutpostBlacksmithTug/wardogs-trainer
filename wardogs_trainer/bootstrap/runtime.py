import time
from pathlib import Path

from wardogs_trainer.config.loader import load_config
from wardogs_trainer.core.attacher import ProcessAttacher
from wardogs_trainer.core.memory import MemoryReaderWriter
from wardogs_trainer.core.offsets import OffsetTable
from wardogs_trainer.handlers.aimbot import AimbotHandler
from wardogs_trainer.handlers.esp import ESPHandler
from wardogs_trainer.handlers.godmode import GodModeHandler
from wardogs_trainer.handlers.infinite_ammo import InfiniteAmmoHandler


class TrainerRuntime:
    def __init__(self, config_path: Path, logger):
        self.config = load_config(config_path)
        self.logger = logger
        self.attacher = ProcessAttacher(process_name=self.config["game"]["process_name"])
        self.mem: MemoryReaderWriter | None = None
        self.offsets: OffsetTable | None = None
        self.handlers: list = []

    def attach(self, pid: int | None = None) -> None:
        self.attacher.attach(pid=pid)
        self.mem = MemoryReaderWriter(self.attacher.handle)
        self.offsets = OffsetTable.load(self.config["game"]["offsets_file"])
        self.logger.info("attached to pid=%s, base=0x%X",
                         self.attacher.pid, self.mem.base_address)

        self.handlers = [
            GodModeHandler(self.mem, self.offsets, self.config["features"]["godmode"]),
            InfiniteAmmoHandler(self.mem, self.offsets, self.config["features"]["infinite_ammo"]),
            ESPHandler(self.mem, self.offsets, self.config["features"]["esp"]),
            AimbotHandler(self.mem, self.offsets, self.config["features"]["aimbot"]),
        ]

    def run(self) -> None:
        tick = self.config["runtime"]["tick_ms"] / 1000.0
        self.logger.info("trainer loop started, tick=%.3fs", tick)
        while True:
            for handler in self.handlers:
                handler.tick()
            time.sleep(tick)

    def detach(self) -> None:
        for handler in self.handlers:
            handler.shutdown()
        self.attacher.detach()