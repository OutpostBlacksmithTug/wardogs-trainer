from wardogs_trainer.models.entity import Entity


class EntityScanner:
    def __init__(self, mem, offsets, max_entities: int = 64):
        self.mem = mem
        self.offsets = offsets
        self.max_entities = max_entities

    def scan(self) -> list[Entity]:
        out: list[Entity] = []
        base = self.mem.base_address + self.offsets["entity_list"]
        stride = self.offsets["entity_size"]
        for i in range(self.max_entities):
            addr = base + i * stride
            try:
                hp = self.mem.read_float(addr + self.offsets["entity_health"])
            except OSError:
                continue
            if hp <= 0.0:
                continue
            pos = (
                self.mem.read_float(addr + 0x60),
                self.mem.read_float(addr + 0x64),
                self.mem.read_float(addr + 0x68),
            )
            out.append(Entity(index=i, address=addr, health=hp, world_pos=pos))
        return out