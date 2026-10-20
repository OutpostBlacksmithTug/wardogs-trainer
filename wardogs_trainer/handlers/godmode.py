from wardogs_trainer.handlers.base import BaseHandler


class GodModeHandler(BaseHandler):
    name = "godmode"
    HEALTH_CAP = 100.0

    def tick(self) -> None:
        if not self.enabled:
            return
        try:
            player = self.mem.base_address + self.offsets["player_base"]
            health_addr = player + self.offsets["health"]
            current = self.mem.read_float(health_addr)
            if 0.0 < current < self.HEALTH_CAP:
                self.mem.write_float(health_addr, self.HEALTH_CAP)
            armor_addr = player + self.offsets["armor"]
            if self.mem.read_float(armor_addr) < self.HEALTH_CAP:
                self.mem.write_float(armor_addr, self.HEALTH_CAP)
        except OSError:
            pass