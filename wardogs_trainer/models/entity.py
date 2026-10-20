from dataclasses import dataclass


@dataclass
class Entity:
    index: int
    address: int
    health: float
    world_pos: tuple[float, float, float]
    is_visible: bool = False

    @property
    def alive(self) -> bool:
        return self.health > 0.0