from enum import Enum
from math import inf
from random import randint

import pygame


class Algorithms(Enum):
    PRIM = 0
    KRUSKAL = 1
    BORUVKA = 2


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
