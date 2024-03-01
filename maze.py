from random import randint

import pygame

from generators import Boruvka, Generator, Kruskal, Prim, PrimMaze
from utils import Algorithms


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

        self.prim: Prim | None = Prim(self.grid_graph)
        self.boruvka: Boruvka | None = None
        self.kruskal: Kruskal | None = None
        self.prim_maze: PrimMaze | None = None
        self.curr_alg: Generator = self.prim

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
