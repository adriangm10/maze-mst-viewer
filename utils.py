from random import randint
from typing import Callable

import pygame

from generators import Algorithms, Boruvka, Kruskal, Prim, PrimMaze


def generate_grid_graph(
    xnode_count: int, ynode_count: int, max_cost: int
) -> list[list[int]]:
    graph = [
        [0 for _ in range(xnode_count * ynode_count)]
        for _ in range(xnode_count * ynode_count)
    ]
    for i in range(ynode_count):
        for j in range(xnode_count):
            node = i * xnode_count + j
            if i > 0:
                graph[node][node - xnode_count] = randint(1, max_cost)
                graph[node - xnode_count][node] = graph[node][node - xnode_count]
            if j > 0:
                graph[node][node - 1] = randint(1, max_cost)
                graph[node - 1][node] = graph[node][node - 1]
            if i < ynode_count - 1:
                graph[node][node + xnode_count] = randint(1, max_cost)
                graph[node + xnode_count][node] = graph[node][node + xnode_count]
            if j < xnode_count - 1:
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
        self.xnode_count = rect.width // cell_size + 1
        self.ynode_count = rect.height // cell_size + 1
        self.max_cost = max_cost
        self.grid_graph = generate_grid_graph(
            self.xnode_count, self.ynode_count, max_cost
        )
        self.rect = rect
        self.color = color
        print(self.ynode_count, self.xnode_count)

        self.prim: Prim | None = Prim(self.grid_graph)
        self.boruvka: Boruvka | None = None
        self.kruskal: Kruskal | None = None
        self.prim_maze: PrimMaze | None = None
        self.curr_alg: Prim | Boruvka | Kruskal | PrimMaze = self.prim

    def set_generation_mode(self, alg: Algorithms):
        match alg:
            case Algorithms.PRIM:
                if self.prim is None:
                    self.prim = Prim(self.grid_graph)
                self.curr_alg = self.prim
            case Algorithms.KRUSKAL:
                if self.kruskal is None:
                    self.kruskal = Kruskal(self.grid_graph)
                self.curr_alg = self.kruskal
            case Algorithms.BORUVKA:
                if self.boruvka is None:
                    self.boruvka = Boruvka(self.grid_graph)
                self.curr_alg = self.boruvka
            case Algorithms.PRIM_MAZE:
                if self.prim_maze is None:
                    self.prim_maze = PrimMaze(
                        self.grid_graph, self.xnode_count, self.ynode_count
                    )
                self.curr_alg = self.prim_maze

    def new_wall(self):
        self.curr_alg.new_wall()

    def is_fully_created(self) -> bool:
        return self.curr_alg.finished()

    def draw_maze(self, surface: pygame.Surface):
        self.curr_alg.draw(
            surface, self.xnode_count, self.cell_size, self.rect, self.color
        )

    def draw_grid(self, surface: pygame.Surface):
        for i, node in enumerate(self.grid_graph):
            for j, edge in enumerate(node):
                from_node = (
                    i % self.xnode_count * self.cell_size + self.rect.x,
                    i // self.xnode_count * self.cell_size + self.rect.y,
                )
                to_node = (
                    j % self.xnode_count * self.cell_size + self.rect.x,
                    j // self.xnode_count * self.cell_size + self.rect.y,
                )
                if edge:
                    pygame.draw.line(surface, self.color, from_node, to_node)

    def draw_grid_points(self, surface: pygame.Surface):
        for i in range(self.ynode_count):
            for j in range(self.xnode_count):
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
        self.curr_alg.restart()


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
