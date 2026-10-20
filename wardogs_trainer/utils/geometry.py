import math


def world_to_screen(
    world: tuple[float, float, float], max_distance: float
) -> tuple[float, float] | None:
    x, y, z = world
    dist = math.sqrt(x * x + y * y + z * z)
    if dist <= 0.0 or dist > max_distance:
        return None
    sx = 960.0 + (x / dist) * 960.0
    sy = 540.0 - (z / dist) * 540.0
    return (sx, sy)