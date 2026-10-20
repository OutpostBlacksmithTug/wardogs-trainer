import math

from wardogs_trainer.handlers.base import BaseHandler


class AimbotHandler(BaseHandler):
    name = "aimbot"

    def tick(self) -> None:
        if not self.enabled:
            return
        try:
            target = self._closest_target()
            if target is None:
                return
            self._snap_view(target)
        except OSError:
            pass

    def _closest_target(self) -> tuple[float, float] | None:
        base = self.mem.base_address + self.offsets["entity_list"]
        stride = self.offsets["entity_size"]
        best: tuple[float, float] | None = None
        best_d = self.options["fov"] ** 2
        for i in range(64):
            ent = base + i * stride
            hp = self.mem.read_float(ent + self.offsets["entity_health"])
            if hp <= 0:
                continue
            dx = self.mem.read_float(ent + 0x60) - self.mem.read_float(ent + 0x60)
            dy = self.mem.read_float(ent + 0x64)
            d = dx * dx + dy * dy
            if d < best_d:
                best_d = d
                best = (dx, dy)
        return best

    def _snap_view(self, target: tuple[float, float]) -> None:
        smoothing = float(self.options.get("smoothing", 1.0)) or 1.0
        player = self.mem.base_address + self.offsets["player_base"]
        angles = player + self.offsets["view_angles"]
        yaw = self.mem.read_float(angles)
        pitch = self.mem.read_float(angles + 0x4)
        target_yaw = math.degrees(math.atan2(target[1], target[0]))
        delta = (target_yaw - yaw) / smoothing
        self.mem.write_float(angles, yaw + delta)
        self.mem.write_float(angles + 0x4, pitch)