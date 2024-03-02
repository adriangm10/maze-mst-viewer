from enum import Enum
from typing import Callable

import pygame


class Algorithms(Enum):
    PRIM = 0
    KRUSKAL = 1
    BORUVKA = 2
    PRIM_MAZE = 3


class PathFinder:
    def next_step(self):
        raise NotImplementedError

    def has_finished(self):
        raise NotImplementedError

    def restart(self):
        raise NotImplementedError

    def draw(
        self,
        surface: pygame.Surface,
        xnode_count: int,
        cell_size: int,
        rect: pygame.Rect,
        visited_color: pygame.Color,
        path_color: pygame.Color,
    ):
        raise NotImplementedError


class Button:
    def __init__(
        self,
        rect: pygame.Rect,
        font: pygame.font.Font,
        label: str = "",
        border_radius: int = -1,
        onClick: Callable | None = None,
        colors: dict[str, tuple[int, int, int]] = {
            "bg": (112, 128, 144),
            "fg": (255, 255, 255),
            "hover": (83, 104, 120),
        },
    ):
        self.rect = rect
        self.label = label
        self.border_radius = border_radius
        self.font = font
        self.colors = colors
        self.onClick = onClick
        self.was_clicked = False
        self.hovered = False
        self.active = True

    def set_active(self, active: bool):
        self.active = active

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(
            surface,
            self.colors["hover"] if self.hovered else self.colors["bg"],
            self.rect,
            border_radius=self.border_radius,
        )
        label = self.font.render(self.label, True, self.colors["fg"])
        surface.blit(
            label,
            (
                self.rect.centerx - label.get_width() / 2,
                self.rect.centery - label.get_height() / 2,
            ),
        )

    def process(self, *args):
        if not self.active:
            return

        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.hovered = True
            if (
                clicked := pygame.mouse.get_pressed(num_buttons=3)[0]
            ) and not self.was_clicked:
                if self.onClick is not None:
                    self.onClick(*args)
                self.was_clicked = True
            else:
                self.was_clicked = clicked
        else:
            self.hovered = False
