from wardogs_trainer.handlers.base import BaseHandler
from wardogs_trainer.utils.geometry import world_to_screen


class ESPHandler(BaseHandler):
    name = "esp"
    MAX_ENTITIES = 64

    def tick(self) -> None:
        if not self.enabled:
            return
        try:
            base = self.mem.base_address + self.offsets["entity_list"]
            stride = self.offsets["entity_size"]
            head_off = self.offsets["entity_bone_head"]
            for i in range(self.MAX_ENTITIES):
                ent = base + i * stride
                head_world = (
                    self.mem.read_float(ent + head_off + 0x0),
                    self.mem.read_float(ent + head_off + 0x4),
                    self.mem.read_float(ent + head_off + 0x8),
                )
                if head_world == (0.0, 0.0, 0.0):
                    continue
                screen = world_to_screen(head_world, self.options["draw_distance"])
                if screen is not None:
                    self._emit_marker(screen, self.mem.read_float(ent + self.offsets["entity_health"]))
        except OSError:
            pass

    def _emit_marker(self, screen: tuple[float, float], hp: float) -> None:
        # overlay renderer consumes this via stdout pipe / IPC in real build
        _ = (screen, hp)