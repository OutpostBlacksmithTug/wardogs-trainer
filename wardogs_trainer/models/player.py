from dataclasses import dataclass


@dataclass
class PlayerState:
    health: float
    armor: float
    ammo_primary: int
    ammo_reserve: int
    pos: tuple[float, float, float]

    def apply_godmode(self, cap: float = 100.0) -> None:
        if 0.0 < self.health < cap:
            self.health = cap
        if self.armor < cap:
            self.armor = cap