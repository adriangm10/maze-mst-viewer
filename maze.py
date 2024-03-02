from random import randint

import pygame

from generators import Boruvka, Generator, Kruskal, Prim, PrimMaze
from utils import Algorithms, PathFinder


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
        self.generation_mode = Algorithms.PRIM

        self.start = (0, 0)
        self.target = (self.ynode_count - 2, self.xnode_count - 2)
        self.path_finder: PathFinder | None = None

    def set_generation_mode(self, alg: Algorithms):
        self.generation_mode = alg
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
        if self.path_finder is not None:
            self.path_finder.restart()

    def theres_wall(self, cell1: tuple[int, int], cell2: tuple[int, int]) -> bool:
        assert isinstance(self.curr_alg, PrimMaze)

        return self.curr_alg.theres_wall(cell1, cell2)

    def next_cells(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        moves = []

        for move in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_pos = pos[0] + move[0], pos[1] + move[1]
            if next_pos[0] < 0 or next_pos[0] > self.ynode_count - 2:
                continue

            elif next_pos[1] < 0 or next_pos[1] > self.xnode_count - 2:
                continue

            if not self.theres_wall(pos, next_pos):
                moves.append(next_pos)

        return moves

    def set_path_finder(self, path_finder: PathFinder):
        self.path_finder = path_finder

    # Makes a step in the path finder and draws the current state of the algorithm
    def solve_step(self):
        if self.generation_mode != Algorithms.PRIM_MAZE or not self.is_fully_created():
            print("[WARNING] trying to solve an MST or a maze that is not finished")
            return
        if self.path_finder is None:
            print("[WARNING] trying to solve a maze without setting self.path_finder")
            return

        if not self.path_finder.has_finished():
            self.path_finder.next_step()

    def draw_solution(self, surface: pygame.Surface):
        if self.path_finder is None:
            return

        self.path_finder.draw(
            surface,
            self.xnode_count,
            self.cell_size,
            self.rect,
            pygame.Color(255, 0, 0),
            pygame.Color(0, 255, 0),
        )
