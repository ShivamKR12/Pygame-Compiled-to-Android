import sys
import random
import time
import pygame
from settings import (
    COLOR_BG, COLOR_PANEL, COLOR_BORDER, COLOR_TEXT_MAIN,
    COLOR_TEXT_MUTED, COLOR_ACCENT, REALMS
)
from dice import draw_dice

class LudoRealmsGame:
    def __init__(self):
        pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()

        info = pygame.display.Info()
        width = info.current_w if info.current_w > 0 else 450
        height = info.current_h if info.current_h > 0 else 800

        if width > 600:
            width = 450
        if height > 900:
            height = 800

        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Ludo Realms")

        self.clock = pygame.time.Clock()

        # Fonts
        self.font_large = pygame.font.SysFont(None, max(28, width // 14))
        self.font_medium = pygame.font.SysFont(None, max(22, width // 20))
        self.font_small = pygame.font.SysFont(None, max(16, width // 28))

        # Game state
        self.realms = [dict(r) for r in REALMS]
        self.dice_value = 6
        self.is_rolling = False
        self.roll_start_time = 0.0
        self.roll_duration = 0.45
        self.current_turn = 0
        self.total_rolls = 0
        self.message = "Tap the dice to roll!"
        self.ripple_pos = None
        self.ripple_radius = 0

    def trigger_roll(self, now, dice_rect):
        if not self.is_rolling:
            self.is_rolling = True
            self.roll_start_time = now
            self.ripple_pos = dice_rect.center
            self.ripple_radius = 5

    def update(self, now):
        if self.is_rolling:
            elapsed = now - self.roll_start_time
            if elapsed < self.roll_duration:
                self.dice_value = random.randint(1, 6)
            else:
                self.is_rolling = False
                self.dice_value = random.randint(1, 6)
                self.total_rolls += 1
                active_realm = self.realms[self.current_turn]
                active_realm["tokens"] += self.dice_value
                self.message = f"{active_realm['name']} marched +{self.dice_value} leagues!"
                self.current_turn = (self.current_turn + 1) % len(self.realms)

        if self.ripple_pos:
            self.ripple_radius += 18
            if self.ripple_radius > 160:
                self.ripple_pos = None
                self.ripple_radius = 0

    def draw(self, w, h, dice_rect):
        self.screen.fill(COLOR_BG)

        # Header Banner
        header_rect = pygame.Rect(16, 16, w - 32, max(60, h // 11))
        pygame.draw.rect(self.screen, COLOR_PANEL, header_rect, border_radius=14)
        pygame.draw.rect(self.screen, COLOR_BORDER, header_rect, width=2, border_radius=14)

        title_surf = self.font_large.render("LUDO REALMS", True, COLOR_ACCENT)
        sub_surf = self.font_small.render(f"Round Rolls: {self.total_rolls}", True, COLOR_TEXT_MUTED)
        self.screen.blit(title_surf, (header_rect.x + 16, header_rect.y + 8))
        self.screen.blit(sub_surf, (header_rect.x + 16, header_rect.y + header_rect.height - 24))

        # Realms Status Cards
        panel_y = header_rect.bottom + 14
        card_gap = 10
        card_h = max(55, (h // 2 - panel_y - card_gap * 4) // 4)

        for i, realm in enumerate(self.realms):
            is_active = i == self.current_turn
            card_rect = pygame.Rect(16, panel_y + i * (card_h + card_gap), w - 32, card_h)

            bg_c = (38, 48, 68) if is_active else COLOR_PANEL
            border_c = COLOR_ACCENT if is_active else COLOR_BORDER
            pygame.draw.rect(self.screen, bg_c, card_rect, border_radius=12)
            pygame.draw.rect(self.screen, border_c, card_rect, width=2 if is_active else 1, border_radius=12)

            token_circle_x = card_rect.x + 22
            token_circle_y = card_rect.centery
            pygame.draw.circle(self.screen, realm["color"], (token_circle_x, token_circle_y), 12)

            name_color = COLOR_TEXT_MAIN if is_active else (200, 205, 215)
            r_name = self.font_medium.render(realm["name"], True, name_color)
            self.screen.blit(r_name, (token_circle_x + 20, card_rect.centery - r_name.get_height() // 2))

            pts = self.font_medium.render(f"{realm['tokens']} pts", True, COLOR_ACCENT if is_active else COLOR_TEXT_MUTED)
            self.screen.blit(pts, (card_rect.right - pts.get_width() - 16, card_rect.centery - pts.get_height() // 2))

        # Bottom Arena - Interactive Dice Section
        arena_top = panel_y + 4 * (card_h + card_gap) + 10
        arena_rect = pygame.Rect(16, arena_top, w - 32, h - arena_top - 16)
        pygame.draw.rect(self.screen, COLOR_PANEL, arena_rect, border_radius=16)
        pygame.draw.rect(self.screen, COLOR_BORDER, arena_rect, width=2, border_radius=16)

        msg_surf = self.font_medium.render(self.message, True, COLOR_TEXT_MAIN)
        self.screen.blit(msg_surf, (arena_rect.centerx - msg_surf.get_width() // 2, arena_rect.y + 14))

        if self.ripple_pos:
            pygame.draw.circle(self.screen, (255, 193, 7, 70), self.ripple_pos, self.ripple_radius, width=3)

        draw_dice(self.screen, dice_rect, self.dice_value, self.is_rolling)

        hint = "ROLLING..." if self.is_rolling else "TAP TO ROLL"
        hint_surf = self.font_small.render(hint, True, COLOR_ACCENT if self.is_rolling else COLOR_TEXT_MUTED)
        self.screen.blit(hint_surf, (dice_rect.centerx - hint_surf.get_width() // 2, dice_rect.bottom + 12))

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            now = time.time()
            w, h = self.screen.get_size()

            header_rect_height = max(60, h // 11)
            panel_y = 16 + header_rect_height + 14
            card_gap = 10
            card_h = max(55, (h // 2 - panel_y - card_gap * 4) // 4)
            arena_top = panel_y + 4 * (card_h + card_gap) + 10
            arena_rect = pygame.Rect(16, arena_top, w - 32, h - arena_top - 16)

            dice_size = max(80, min(140, arena_rect.height // 2, arena_rect.width // 3))
            dice_rect = pygame.Rect(
                arena_rect.centerx - dice_size // 2,
                arena_rect.centery - dice_size // 2 + 10,
                dice_size,
                dice_size,
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_AC_BACK):
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if dice_rect.collidepoint(event.pos):
                        self.trigger_roll(now, dice_rect)
                elif event.type == pygame.FINGERDOWN:
                    px = int(event.x * w)
                    py = int(event.y * h)
                    if dice_rect.collidepoint((px, py)):
                        self.trigger_roll(now, dice_rect)

            self.update(now)
            self.draw(w, h, dice_rect)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
