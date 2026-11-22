import pygame

def draw_dice(surface, rect, value, is_rolling=False):
    """Renders an interactive dice with pip patterns."""
    bg_color = (255, 235, 170) if is_rolling else (248, 249, 250)
    pygame.draw.rect(surface, bg_color, rect, border_radius=18)
    pygame.draw.rect(surface, (100, 110, 130), rect, width=3, border_radius=18)

    cx, cy = rect.centerx, rect.centery
    ox = rect.width // 4
    oy = rect.height // 4
    pip_radius = max(5, rect.width // 14)
    pip_color = (33, 37, 41)

    pip_positions = {
        1: [(0, 0)],
        2: [(-1, -1), (1, 1)],
        3: [(-1, -1), (0, 0), (1, 1)],
        4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
        5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)],
        6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)],
    }

    for dx, dy in pip_positions.get(value, [(0, 0)]):
        px = cx + dx * ox
        py = cy + dy * oy
        pygame.draw.circle(surface, pip_color, (px, py), pip_radius)
