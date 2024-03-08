from typing import Callable

import pygame


class Button:
    """
    possible options in colors:
        "bg": background color,
        "fg": foreground color,
        "hover": color when mouse hover,
        "border": border color,
    """

    def __init__(
        self,
        rect: pygame.Rect,
        font: pygame.font.Font,
        colors: dict[str, tuple[int, int, int]],
        label: str = "",
        border_radius: int = -1,
        onClick: Callable | None = None,
        border_width: int = 1,
    ):
        self.rect = rect
        self.label = label
        self.border_radius = border_radius
        self.font = font
        self.colors = colors.copy()
        self.border_width = border_width
        self.onClick = onClick
        self.was_clicked = False
        self.hovered = False
        self.active = True

    def set_active(self, active: bool):
        self.active = active

    def set_border_color(self, color: tuple[int, int, int]):
        self.colors["border"] = color

    def set_bg_color(self, color: tuple[int, int, int]):
        self.colors["bg"] = color

    def set_fg_color(self, color: tuple[int, int, int]):
        self.colors["fg"] = color

    def set_hover_color(self, color: tuple[int, int, int]):
        self.colors["hover"] = color

    def get_border_color(self) -> tuple[int, int, int]:
        return self.colors["border"]

    def get_bg_color(self) -> tuple[int, int, int]:
        return self.colors["bg"]

    def get_fg_color(self) -> tuple[int, int, int]:
        return self.colors["fg"]

    def get_hover_color(self) -> tuple[int, int, int]:
        return self.colors["hover"]

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(
            surface,
            self.colors["hover"] if self.hovered else self.colors["bg"],
            self.rect,
            border_radius=self.border_radius,
        )
        pygame.draw.rect(surface, self.colors["border"], self.rect, self.border_width)

        if self.active:
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
                    self.onClick(self, *args)
                self.was_clicked = True
            else:
                self.was_clicked = clicked
        else:
            self.hovered = False


class Scale:
    """
    possible options in colors:
        "fill": color for filling the line,
        "line": line color,
        "slider": color of the button that slides,
        "fg": foreground color,
    """

    def __init__(
        self,
        min_value: float,
        max_value: float,
        size: int,
        pos: tuple[int, int],
        button_size: float,
        font: pygame.font.Font,
        padding: float = 10,
        onClick: Callable | None = None,
        colors: dict[str, tuple[int, int, int]] = {
            "fill": (0, 184, 255),
            "line": (255, 255, 255),
            "slider": (255, 255, 255),
            "fg": (255, 255, 255),
        },
    ):
        self.max_value = max_value
        self.min_value = min_value
        self.size = size
        self.colors = colors
        self.pos = pos
        self.scale = 1
        self.button_size = button_size
        self.active = True
        self.font = font
        self.padding = padding
        self.onClick = onClick

        label = font.render(f"{self.max_value:.2f}", True, colors["fg"])
        self.margin = label.get_width(), font.get_height() / 2
        del label

        self.button_pos = (
            self.pos[0] + self.size * self.scale + self.margin[0] + self.padding,
            self.pos[1] + self.margin[1],
        )
        self.line_rect = pygame.Rect(
            self.pos[0] + self.margin[0] + self.padding,
            self.pos[1],
            self.size,
            self.button_size * 2,
        )

        self.value = self.min_value + (self.max_value - self.min_value) * self.scale

    def set_active(self, active: bool):
        self.active = active

    def set_slider_color(self, color: tuple[int, int, int]):
        self.colors["slider"] = color

    def set_fill_color(self, color: tuple[int, int, int]):
        self.colors["fill"] = color

    def set_line_color(self, color: tuple[int, int, int]):
        self.colors["line"] = color

    def set_value(self, value):
        assert value >= self.min_value and value <= self.max_value

        self.value = value
        self.scale = (value - self.min_value) / (self.max_value - self.min_value)
        self.button_pos = (
            self.pos[0] + self.size * self.scale + self.margin[0] + self.padding,
            self.pos[1] + self.margin[1],
        )

    def draw(self, surface: pygame.Surface):
        label = self.font.render(
            f"{self.value:.2f}",
            True,
            self.colors["fg"],
        )
        surface.blit(label, self.pos)

        pygame.draw.line(
            surface,
            self.colors["fill"],
            (
                self.pos[0] + label.get_width() + self.padding,
                self.pos[1] + label.get_height() / 2,
            ),
            self.button_pos,
        )

        pygame.draw.line(
            surface,
            self.colors["line"],
            self.button_pos,
            (
                self.pos[0] + self.size + label.get_width() + self.padding,
                self.pos[1] + label.get_height() / 2,
            ),
        )

        if self.active:
            pygame.draw.circle(
                surface, self.colors["slider"], self.button_pos, self.button_size
            )
        else:
            pygame.draw.circle(
                surface, (128, 128, 128), self.button_pos, self.button_size
            )

    def process(self, *args):
        if not self.active:
            return

        mouse = pygame.mouse.get_pos()
        if self.line_rect.collidepoint(mouse):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_pos = mouse[0], self.button_pos[1]
                self.scale = (
                    self.button_pos[0] - self.pos[0] - self.padding - self.margin[0]
                ) / self.size
                self.value = (
                    self.min_value + (self.max_value - self.min_value) * self.scale
                )

                if self.onClick is not None:
                    self.onClick(self, *args)
        else:
            self.hovered = False
