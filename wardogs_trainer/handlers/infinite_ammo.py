from wardogs_trainer.handlers.base import BaseHandler


class InfiniteAmmoHandler(BaseHandler):
    name = "infinite_ammo"
    MAGAZINE_MIN = 30

    def tick(self) -> None:
        if not self.enabled:
            return
        try:
            player = self.mem.base_address + self.offsets["player_base"]
            mag = player + self.offsets["ammo_primary"]
            reserve = player + self.offsets["ammo_reserve"]
            if self.mem.read_int32(mag) < self.MAGAZINE_MIN:
                self.mem.write_int32(mag, self.MAGAZINE_MIN)
            if self.mem.read_int32(reserve) < 300:
                self.mem.write_int32(reserve, 300)
        except OSError:
            pass