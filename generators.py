from enum import Enum
from math import inf
from random import randint

import pygame


class Algorithms(Enum):
    PRIM = 0
    KRUSKAL = 1
    BORUVKA = 2
    PRIM_MAZE = 3


def get_graph_edges(graph: list[list[int]]) -> list[tuple[int, int, int]]:
    edges = []
    for i in range(len(graph)):
        for j in range(i, len(graph[i])):
            if graph[i][j]:
                edges.append((i, j, graph[i][j]))

    return edges


class Prim:
    def __init__(self, graph: list[list[int]]):
        self.grid_graph = graph
        self.root = randint(0, len(self.grid_graph) - 1)
        self.cost = [i if i else inf for i in self.grid_graph[self.root]]
        self.parents = [self.root if i else None for i in self.grid_graph[self.root]]
        self.q = [False] * len(self.grid_graph)
        self.q[self.root] = True
        self.parents[self.root] = self.root
        self.prim_walls = 0

    def finished(self):
        return self.prim_walls == len(self.grid_graph)

    def new_wall(self):
        v = self.cost.index(min(self.cost))
        self.cost[v] = inf
        self.q[v] = True
        self.prim_walls += 1

        for n in range(len(self.grid_graph[v])):
            if (
                self.grid_graph[v][n] < self.cost[n]
                and not self.q[n]
                and self.grid_graph[v][n]
            ):
                self.parents[n] = v
                self.cost[n] = self.grid_graph[v][n]

    def draw(
        self,
        surface: pygame.Surface,
        xcell_count: int,
        cell_size: int,
        rect: pygame.Rect,
        color: pygame.Color,
    ):
        for i, v in enumerate(self.parents):
            if v is None or not self.q[i]:
                continue
            from_node = (
                v % xcell_count * cell_size + rect.x,
                v // xcell_count * cell_size + rect.y,
            )
            to_node = (
                i % xcell_count * cell_size + rect.x,
                i // xcell_count * cell_size + rect.y,
            )
            pygame.draw.line(surface, color, from_node, to_node)

    def restart(self):
        self.root = randint(0, len(self.grid_graph) - 1)
        self.cost = [i if i else inf for i in self.grid_graph[self.root]]
        self.parents = [self.root if i else None for i in self.grid_graph[self.root]]
        self.q = [False] * len(self.grid_graph)
        self.q[self.root] = True
        self.parents[self.root] = self.root
        self.prim_walls = 0


class Kruskal:
    def __init__(self, graph: list[list[int]]):
        self.grid_graph = graph
        self.edges = get_graph_edges(self.grid_graph)
        self.edges.sort(key=lambda edge: edge[2])
        self.sets = list(range(len(self.grid_graph)))
        self.replace_set = None
        self.edge = 0
        self.selected_edges: list[tuple[int, int, int]] = []

    def finished(self):
        return len(self.selected_edges) == len(self.grid_graph) - 1

    def union(self, union_set, child_set):
        for i in range(len(self.sets)):
            if self.sets[i] == child_set:
                self.sets[i] = union_set

    def new_wall(self):
        while self.edge < len(self.edges):
            edge = self.edges[self.edge]
            if self.sets[edge[0]] != self.sets[edge[1]]:
                self.replace_set = self.sets[edge[1]]
                self.union(self.sets[edge[0]], self.sets[edge[1]])
                self.selected_edges.append(edge)
                self.edge += 1
                break

            self.edge += 1

    def draw(
        self,
        surface: pygame.Surface,
        xcell_count: int,
        cell_size: int,
        rect: pygame.Rect,
        color: pygame.Color,
    ):
        for i in self.selected_edges:
            from_node = (
                i[0] % xcell_count * cell_size + rect.x,
                i[0] // xcell_count * cell_size + rect.y,
            )
            to_node = (
                i[1] % xcell_count * cell_size + rect.x,
                i[1] // xcell_count * cell_size + rect.y,
            )
            pygame.draw.line(surface, color, from_node, to_node)

    def restart(self):
        self.sets = list(range(len(self.grid_graph)))
        self.replace_set = None
        self.edge = 0
        self.selected_edges = []


class Boruvka:
    def __init__(self, graph: list[list[int]]):
        self.grid_graph = graph
        self.edges = get_graph_edges(self.grid_graph)
        self.components = list(range(len(self.grid_graph)))
        self.component_count = len(self.components)
        self.rank = [0] * len(self.grid_graph)
        self.cheapest = [None] * len(self.grid_graph)
        self.boruvka_walls: list[tuple[int, int, int]] = []
        self.curr_comp = 0
        self.is_finished = False

    def finished(self):
        return self.is_finished

    # v -> v union w
    def union(self, componentv: int, componentw: int):
        for i in range(len(self.components)):
            self.components[i] = (
                componentv if self.components[i] == componentw else self.components[i]
            )

    def new_wall(self):
        if self.curr_comp == self.component_count:
            self.cheapest = [None] * self.component_count
            self.curr_comp = 0

            for v, w, c in self.edges:
                componentv = self.components[v]
                componentw = self.components[w]

                if componentv == componentw:
                    continue

                if (
                    self.cheapest[componentv] is None
                    or self.cheapest[componentv][2] > c
                ):
                    self.cheapest[componentv] = (v, w, c)

                if (
                    self.cheapest[componentw] is None
                    or self.cheapest[componentw][2] > c
                ):
                    self.cheapest[componentw] = (v, w, c)

            if all([i is None for i in self.cheapest]):
                self.is_finished = True
                return

        while self.cheapest[self.curr_comp] is None:
            self.curr_comp += 1
            if self.curr_comp == self.component_count:
                return

        v, w, c = self.cheapest[self.curr_comp]
        self.boruvka_walls.append((v, w, c))
        componentv = self.components[v]
        componentw = self.components[w]

        if self.rank[componentv] > self.rank[componentw]:
            self.union(componentv, componentw)

        elif self.rank[componentw] > self.rank[componentv]:
            self.union(componentw, componentv)

        else:
            self.union(componentv, componentw)
            self.rank[componentv] += 1

        self.curr_comp += 1

    def draw(
        self,
        surface: pygame.Surface,
        xcell_count: int,
        cell_size: int,
        rect: pygame.Rect,
        color: pygame.Color,
    ):
        for i in self.boruvka_walls:
            from_node = (
                i[0] % xcell_count * cell_size + rect.x,
                i[0] // xcell_count * cell_size + rect.y,
            )
            to_node = (
                i[1] % xcell_count * cell_size + rect.x,
                i[1] // xcell_count * cell_size + rect.y,
            )
            pygame.draw.line(surface, color, from_node, to_node)

    def restart(self):
        self.components = list(range(len(self.grid_graph)))
        self.component_count = len(self.components)
        self.rank = [0] * len(self.grid_graph)
        self.cheapest = [None] * len(self.grid_graph)
        self.boruvka_walls = []
        self.curr_comp = 0
        self.is_finished = False


class PrimMaze:
    def __init__(self, grid: list[list[int]], xnode_count: int, ynode_count: int):
        self.grid = grid
        self.cell_dims = (ynode_count - 1, xnode_count - 1)  # (rows, columns)
        self.xnode_count = xnode_count
        self.ynode_count = ynode_count
        self.walls = self.cell_walls((0, 0))
        self.visited_cells: set[tuple[int, int]] = set([(0, 0)])
        self.grid_walls = set([(v, w) for v, w, _ in get_graph_edges(self.grid)])
        self.selected_walls = self.grid_walls.copy()
        self.selected_walls.remove((0, 1))
        self.selected_walls.remove((len(grid) - 2, len(grid) - 1))

    # cell = i, j coords of the cell (i = row, j = column)
    def cell_walls(self, cell: tuple[int, int]) -> list[tuple[int, int]]:
        n = cell[0] * self.xnode_count + cell[1]
        walls = [(n, i) for i in range(n + 1, len(self.grid[0])) if self.grid[n][i]]
        n = (cell[0] + 1) * self.xnode_count + cell[1] + 1
        walls += [(i, n) for i in range(n) if self.grid[n][i]]
        return walls

    def splited_cells(
        self, wall: tuple[int, int]
    ) -> tuple[tuple[int, int] | None, tuple[int, int] | None]:
        cell1 = wall[0] // self.xnode_count, wall[0] % self.xnode_count
        if cell1[0] > self.cell_dims[0] - 1 or cell1[1] > self.cell_dims[1] - 1:
            return None, None

        if wall[1] - wall[0] == 1:
            cell2 = cell1[0] - 1, cell1[1]
            if cell2[0] < 0 or cell2[0] > self.cell_dims[0] - 1:
                return cell1, None
        else:
            cell2 = cell1[0], cell1[1] - 1
            if cell2[1] < 0 or cell2[1] > self.cell_dims[1] - 1:
                return cell1, None

        return cell1, cell2

    def new_wall(self):
        if not self.walls:
            return

        wall = self.walls.pop(randint(0, len(self.walls) - 1))
        cells = self.splited_cells(wall)

        if cells[0] is None:
            return
        if cells[1] is None:
            self.visited_cells.add(cells[0])
            return

        if cells[0] not in self.visited_cells:
            self.selected_walls.remove(wall)
            self.visited_cells.add(cells[0])
            self.walls.extend(self.cell_walls(cells[0]))
        elif cells[1] not in self.visited_cells:
            self.selected_walls.remove(wall)
            self.visited_cells.add(cells[1])
            self.walls.extend(self.cell_walls(cells[1]))

    def finished(self) -> bool:
        return not bool(self.walls)

    def draw(
        self,
        surface: pygame.Surface,
        xcell_count: int,
        cell_size: int,
        rect: pygame.Rect,
        color: pygame.Color,
    ):
        for i in self.selected_walls:
            from_node = (
                i[0] % xcell_count * cell_size + rect.x,
                i[0] // xcell_count * cell_size + rect.y,
            )
            to_node = (
                i[1] % xcell_count * cell_size + rect.x,
                i[1] // xcell_count * cell_size + rect.y,
            )
            pygame.draw.line(surface, color, from_node, to_node)

    def restart(self):
        self.walls = self.cell_walls((0, 0))
        self.visited_cells = set([(0, 0)])
        self.selected_walls = self.grid_walls.copy()
        self.selected_walls.remove((0, 1))
        self.selected_walls.remove((len(self.grid) - 2, len(self.grid) - 1))
