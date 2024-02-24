from random import randint
from typing import Callable

import pygame

from algs import Algorithms, Boruvka, Kruskal, Prim


def generate_grid_graph(
    xcell_count: int, ycell_count: int, max_cost: int
) -> list[list[int]]:
    graph = [
        [0 for _ in range(xcell_count * ycell_count)]
        for _ in range(xcell_count * ycell_count)
    ]
    for i in range(ycell_count):
        for j in range(xcell_count):
            node = i * xcell_count + j
            if i > 0:
                graph[node][node - xcell_count] = randint(1, max_cost)
                graph[node - xcell_count][node] = graph[node][node - xcell_count]
            if j > 0:
                graph[node][node - 1] = randint(1, max_cost)
                graph[node - 1][node] = graph[node][node - 1]
            if i < ycell_count - 1:
                graph[node][node + xcell_count] = randint(1, max_cost)
                graph[node + xcell_count][node] = graph[node][node + xcell_count]
            if j < xcell_count - 1:
                graph[node][node + 1] = randint(1, max_cost)
                graph[node + 1][node] = graph[node][node + 1]
    return graph


class Maze:
    def __init__(
        self,
        rect: pygame.Rect,
        cell_size: int,
        max_cost: int = 10,
        color: pygame.Color = pygame.Color(255, 255, 255),
    ):
        self.cell_size = cell_size
        self.xcell_count = rect.width // cell_size + 1
        self.ycell_count = rect.height // cell_size + 1
        self.max_cost = max_cost
        self.grid_graph = generate_grid_graph(
            self.xcell_count, self.ycell_count, max_cost
        )
        self.rect = rect
        self.color = color
        self.generation_mode = Algorithms.PRIM

        self.prim: Prim | None = Prim(self.grid_graph)
        self.boruvka: Boruvka | None = None
        self.kruskal: Kruskal | None = None

    def set_generation_mode(self, alg: Algorithms):
        self.generation_mode = alg
        match alg:
            case Algorithms.PRIM:
                if self.prim is None:
                    self.prim = Prim(self.grid_graph)
            case Algorithms.KRUSKAL:
                if self.kruskal is None:
                    self.kruskal = Kruskal(self.grid_graph)
            case Algorithms.BORUVKA:
                if self.boruvka is None:
                    self.boruvka = Boruvka(self.grid_graph)

    def new_wall(self):
        match self.generation_mode:
            case Algorithms.PRIM:
                self.prim.new_wall()
            case Algorithms.KRUSKAL:
                self.kruskal.new_wall()
            case Algorithms.BORUVKA:
                self.boruvka.new_wall()

    def is_fully_created(self) -> bool:
        match self.generation_mode:
            case Algorithms.PRIM:
                return self.prim.finished() if self.prim is not None else False
            case Algorithms.KRUSKAL:
                return self.kruskal.finished() if self.kruskal is not None else False
            case Algorithms.BORUVKA:
                return self.boruvka.finished() if self.boruvka is not None else False

    def draw_maze(self, surface: pygame.Surface):
        match self.generation_mode:
            case Algorithms.PRIM:
                if self.prim is not None:
                    self.prim.draw(
                        surface, self.xcell_count, self.cell_size, self.rect, self.color
                    )
            case Algorithms.KRUSKAL:
                if self.kruskal is not None:
                    self.kruskal.draw(
                        surface, self.xcell_count, self.cell_size, self.rect, self.color
                    )
            case Algorithms.BORUVKA:
                if self.boruvka is not None:
                    self.boruvka.draw(
                        surface, self.xcell_count, self.cell_size, self.rect, self.color
                    )

    def draw_grid(self, surface: pygame.Surface):
        for i, node in enumerate(self.grid_graph):
            for j, edge in enumerate(node):
                from_node = (
                    i % self.xcell_count * self.cell_size + self.rect.x,
                    i // self.xcell_count * self.cell_size + self.rect.y,
                )
                to_node = (
                    j % self.xcell_count * self.cell_size + self.rect.x,
                    j // self.xcell_count * self.cell_size + self.rect.y,
                )
                if edge:
                    pygame.draw.line(surface, self.color, from_node, to_node)

    def draw_grid_points(self, surface: pygame.Surface):
        for i in range(self.ycell_count):
            for j in range(self.xcell_count):
                pygame.draw.circle(
                    surface,
                    self.color,
                    (
                        j * self.cell_size + self.rect.x,
                        i * self.cell_size + self.rect.y,
                    ),
                    1,
                )

    def restart(self):
        match self.generation_mode:
            case Algorithms.PRIM:
                if self.prim is not None:
                    self.prim.restart()
            case Algorithms.KRUSKAL:
                if self.kruskal is not None:
                    self.kruskal.restart()
            case Algorithms.BORUVKA:
                if self.boruvka is not None:
                    self.boruvka.restart()


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
