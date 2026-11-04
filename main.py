"""
Ludo Realms - Mobile Android Pygame Test Application
Compatible with Android (via python-for-android/Buildozer) and Desktop.
"""

import sys
import random
import time
import pygame

# Initialize Pygame and Font Engine
pygame.init()
if not pygame.font.get_init():
    pygame.font.init()

# Color definitions
COLOR_BG = (20, 24, 33)
COLOR_PANEL = (30, 38, 54)
COLOR_BORDER = (58, 69, 94)
COLOR_TEXT_MAIN = (245, 247, 250)
COLOR_TEXT_MUTED = (145, 158, 175)
COLOR_ACCENT = (255, 193, 7)

# Realm Theme Colors
REALMS = [
    {"name": "Crimson Citadel", "color": (229, 62, 62), "tokens": 0},
    {"name": "Verdant Outpost", "color": (56, 161, 105), "tokens": 0},
    {"name": "Golden Sanctuary", "color": (214, 158, 46), "tokens": 0},
    {"name": "Azure Bastion", "color": (49, 130, 206), "tokens": 0},
]


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


def main():
    # Detect display resolution
    info = pygame.display.Info()
    # On Android, native resolution is reported; fallback for desktop test
    width = info.current_w if info.current_w > 0 else 450
    height = info.current_h if info.current_h > 0 else 800

    # On desktop, cap window size to a comfortable portrait ratio
    if width > 600:
        width = 450
    if height > 900:
        height = 800

    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Ludo Realms")

    clock = pygame.time.Clock()

    # Fonts
    font_large = pygame.font.SysFont(None, max(28, width // 14))
    font_medium = pygame.font.SysFont(None, max(22, width // 20))
    font_small = pygame.font.SysFont(None, max(16, width // 28))

    # Game state
    dice_value = 6
    is_rolling = False
    roll_start_time = 0.0
    roll_duration = 0.45
    current_turn = 0
    total_rolls = 0
    message = "Tap the dice to roll!"
    ripple_pos = None
    ripple_radius = 0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        now = time.time()
        w, h = screen.get_size()

        # Handle rolling animation
        if is_rolling:
            dice_value = random.randint(1, 6)
            if now - roll_start_time >= roll_duration:
                is_rolling = False
                final_roll = random.randint(1, 6)
                dice_value = final_roll
                total_rolls += 1
                # Advance realm progress
                REALMS[current_turn]["tokens"] += dice_value
                active_realm = REALMS[current_turn]["name"]
                message = f"{active_realm} rolled a {dice_value}!"
                current_turn = (current_turn + 1) % len(REALMS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Support ESC / Android BACK button
                if event.key in (pygame.K_ESCAPE, getattr(pygame, "K_AC_BACK", 1073742094)):
                    running = False
                elif event.key == pygame.K_SPACE and not is_rolling:
                    is_rolling = True
                    roll_start_time = now
            elif event.type in (pygame.MOUSEBUTTONDOWN, getattr(pygame, "FINGERDOWN", None)):
                # Normal mouse click or touch on Android
                pos = getattr(event, "pos", None)
                if pos is None and hasattr(event, "x") and hasattr(event, "y"):
                    pos = (int(event.x * w), int(event.y * h))

                if pos:
                    ripple_pos = pos
                    ripple_radius = 5

                    # Check if dice was tapped
                    dice_size = min(w // 3, 140)
                    dice_rect = pygame.Rect(
                        (w - dice_size) // 2,
                        int(h * 0.58),
                        dice_size,
                        dice_size,
                    )
                    if dice_rect.collidepoint(pos) and not is_rolling:
                        is_rolling = True
                        roll_start_time = now

        # ---------------- RENDER ----------------
        screen.fill(COLOR_BG)

        # 1. Header Banner
        header_h = int(h * 0.12)
        pygame.draw.rect(screen, COLOR_PANEL, (0, 0, w, header_h))
        pygame.draw.line(screen, COLOR_BORDER, (0, header_h), (w, header_h), 2)

        title_surf = font_large.render("LUDO REALMS", True, COLOR_ACCENT)
        title_rect = title_surf.get_rect(center=(w // 2, header_h * 0.42))
        screen.blit(title_surf, title_rect)

        sub_surf = font_small.render("Pygame Android Compilation Test Build", True, COLOR_TEXT_MUTED)
        sub_rect = sub_surf.get_rect(center=(w // 2, header_h * 0.78))
        screen.blit(sub_surf, sub_rect)

        # 2. Realm Cards (4 Quadrants)
        grid_top = int(header_h + 15)
        card_w = (w - 45) // 2
        card_h = int(h * 0.15)

        for i, realm in enumerate(REALMS):
            row = i // 2
            col = i % 2
            cx = 15 + col * (card_w + 15)
            cy = grid_top + row * (card_h + 12)

            # Card background
            card_rect = pygame.Rect(cx, cy, card_w, card_h)
            is_active = (i == current_turn)
            border_col = realm["color"] if is_active else COLOR_BORDER
            border_w = 3 if is_active else 1

            pygame.draw.rect(screen, COLOR_PANEL, card_rect, border_radius=12)
            pygame.draw.rect(screen, border_col, card_rect, width=border_w, border_radius=12)

            # Realm indicator dot
            pygame.draw.circle(screen, realm["color"], (cx + 18, cy + 22), 8)

            name_surf = font_medium.render(realm["name"], True, COLOR_TEXT_MAIN)
            screen.blit(name_surf, (cx + 34, cy + 12))

            pts_surf = font_small.render(f"Distance: {realm['tokens']} steps", True, COLOR_TEXT_MUTED)
            screen.blit(pts_surf, (cx + 18, cy + 42))

            # Progress bar
            bar_w = card_w - 36
            bar_h = 6
            bar_rect = pygame.Rect(cx + 18, cy + card_h - 18, bar_w, bar_h)
            pygame.draw.rect(screen, (40, 50, 70), bar_rect, border_radius=3)
            fill_w = min(bar_w, int(bar_w * ((realm["tokens"] % 50) / 50.0)))
            if fill_w > 0:
                fill_rect = pygame.Rect(cx + 18, cy + card_h - 18, fill_w, bar_h)
                pygame.draw.rect(screen, realm["color"], fill_rect, border_radius=3)

        # 3. Active Turn Indicator & Status
        turn_y = int(grid_top + 2 * (card_h + 12) + 10)
        active_color = REALMS[current_turn]["color"]
        turn_text = f"Turn: {REALMS[current_turn]['name']}"
        turn_surf = font_medium.render(turn_text, True, active_color)
        turn_rect = turn_surf.get_rect(center=(w // 2, turn_y + 15))
        screen.blit(turn_surf, turn_rect)

        msg_surf = font_small.render(message, True, COLOR_TEXT_MUTED)
        msg_rect = msg_surf.get_rect(center=(w // 2, turn_y + 40))
        screen.blit(msg_surf, msg_rect)

        # 4. Interactive Dice Center
        dice_size = min(w // 3, 130)
        dice_rect = pygame.Rect(
            (w - dice_size) // 2,
            int(h * 0.58),
            dice_size,
            dice_size,
        )

        # Glow ring around dice for current turn
        glow_rect = dice_rect.inflate(14, 14)
        pygame.draw.rect(screen, active_color, glow_rect, width=2, border_radius=22)

        draw_dice(screen, dice_rect, dice_value, is_rolling)

        hint_surf = font_small.render("TAP DICE TO ROLL" if not is_rolling else "ROLLING...", True, COLOR_TEXT_MAIN)
        hint_rect = hint_surf.get_rect(center=(w // 2, dice_rect.bottom + 25))
        screen.blit(hint_surf, hint_rect)

        # 5. Bottom System Diagnostics
        footer_y = h - 45
        diag_text = f"FPS: {int(clock.get_fps())} | Rolls: {total_rolls} | Res: {w}x{h}"
        diag_surf = font_small.render(diag_text, True, (90, 105, 125))
        diag_rect = diag_surf.get_rect(center=(w // 2, footer_y))
        screen.blit(diag_surf, diag_rect)

        # Touch Ripple Effect
        if ripple_pos:
            ripple_radius += int(60 * dt)
            if ripple_radius < 40:
                pygame.draw.circle(screen, (255, 255, 255), ripple_pos, ripple_radius, 2)
            else:
                ripple_pos = None

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

