from enum import Enum
from random import randint
from typing import Callable

import pygame


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


def get_graph_edges(graph: list[list[int]]) -> list[tuple[int, int, int]]:
    edges = []
    for i in range(len(graph)):
        for j in range(i, len(graph[i])):
            if graph[i][j]:
                edges.append((i, j, graph[i][j]))

    return edges


class Algorithms(Enum):
    PRIM = 0
    KRUSKAL = 1
    BORUVKA = 2


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
        self.generation_mode = Algorithms.KRUSKAL

        # KRUSKAL
        self.edges = get_graph_edges(self.grid_graph)
        self.edges.sort(key=lambda edge: edge[2])
        self.sets = list(range(len(self.grid_graph)))
        self.replace_set = None
        self.edge = 0
        self.selected_edges: list[tuple[int, int, int]] = []

        # PRIM
        self.root = randint(0, len(self.grid_graph) - 1)
        self.cost = [i if i else self.max_cost + 1 for i in self.grid_graph[self.root]]
        self.parents = [self.root if i else None for i in self.grid_graph[self.root]]
        self.q = [False] * len(self.grid_graph)
        self.q[self.root] = True
        self.parents[self.root] = self.root
        self.prim_walls = 0

        # BORUVKA
        self.components = list(range(len(self.grid_graph)))
        self.component_count = len(self.components)
        self.rank = [0] * len(self.grid_graph)
        self.cheapest = [None] * len(self.grid_graph)
        self.boruvka_walls: list[tuple[int, int, int]] = []
        self.curr_comp = 0
        self.boruvka_end = False

    def __prim_wall(self):
        v = self.cost.index(min(self.cost))
        self.cost[v] = self.max_cost + 1
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

    def __union(self, union_set, child_set):
        for i in range(len(self.sets)):
            if self.sets[i] == child_set:
                self.sets[i] = union_set

    def __kruskal_wall(self):
        while self.edge < len(self.edges):
            edge = self.edges[self.edge]
            if self.sets[edge[0]] != self.sets[edge[1]]:
                self.replace_set = self.sets[edge[1]]
                self.__union(self.sets[edge[0]], self.sets[edge[1]])
                self.selected_edges.append(edge)
                self.edge += 1
                break

            self.edge += 1

    def __boruvka_wall(self):
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
                self.boruvka_end = True
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
            for i in range(len(self.components)):
                self.components[i] = (
                    componentv
                    if self.components[i] == componentw
                    else self.components[i]
                )

        elif self.rank[componentw] > self.rank[componentv]:
            for i in range(len(self.components)):
                self.components[i] = (
                    componentw
                    if self.components[i] == componentv
                    else self.components[i]
                )
        else:
            for i in range(len(self.components)):
                self.components[i] = (
                    componentv
                    if self.components[i] == componentw
                    else self.components[i]
                )
            self.rank[componentv] += 1

        self.curr_comp += 1

    def new_wall(self):
        match self.generation_mode:
            case Algorithms.PRIM:
                self.__prim_wall()
            case Algorithms.KRUSKAL:
                self.__kruskal_wall()
            case Algorithms.BORUVKA:
                self.__boruvka_wall()

    def is_fully_created(self) -> bool:
        match self.generation_mode:
            case Algorithms.PRIM:
                return self.prim_walls == len(self.grid_graph)
            case Algorithms.KRUSKAL:
                return len(self.selected_edges) == len(self.grid_graph) - 1
            case Algorithms.BORUVKA:
                return self.boruvka_end

    def __draw_prim(self, surface: pygame.Surface):
        for i, v in enumerate(self.parents):
            if v is None or not self.q[i]:
                continue
            from_node = (
                v % self.xcell_count * self.cell_size + self.rect.x,
                v // self.xcell_count * self.cell_size + self.rect.y,
            )
            to_node = (
                i % self.xcell_count * self.cell_size + self.rect.x,
                i // self.xcell_count * self.cell_size + self.rect.y,
            )
            pygame.draw.line(surface, self.color, from_node, to_node)

    def __draw_kruskal(self, surface: pygame.Surface):
        for i in self.selected_edges:
            from_node = (
                i[0] % self.xcell_count * self.cell_size + self.rect.x,
                i[0] // self.xcell_count * self.cell_size + self.rect.y,
            )
            to_node = (
                i[1] % self.xcell_count * self.cell_size + self.rect.x,
                i[1] // self.xcell_count * self.cell_size + self.rect.y,
            )
            pygame.draw.line(surface, self.color, from_node, to_node)

    def __draw_boruvka(self, surface: pygame.Surface):
        for i in self.boruvka_walls:
            from_node = (
                i[0] % self.xcell_count * self.cell_size + self.rect.x,
                i[0] // self.xcell_count * self.cell_size + self.rect.y,
            )
            to_node = (
                i[1] % self.xcell_count * self.cell_size + self.rect.x,
                i[1] // self.xcell_count * self.cell_size + self.rect.y,
            )
            pygame.draw.line(surface, self.color, from_node, to_node)

    def draw_maze(self, surface: pygame.Surface):
        match self.generation_mode:
            case Algorithms.PRIM:
                self.__draw_prim(surface)
            case Algorithms.KRUSKAL:
                self.__draw_kruskal(surface)
            case Algorithms.BORUVKA:
                self.__draw_boruvka(surface)

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
                self.root = randint(0, len(self.grid_graph) - 1)
                self.cost = [
                    i if i else self.max_cost + 1 for i in self.grid_graph[self.root]
                ]
                self.parents = [
                    self.root if i else None for i in self.grid_graph[self.root]
                ]
                self.q = [False] * len(self.grid_graph)
                self.q[self.root] = True
                self.parents[self.root] = self.root
                self.prim_walls = 0
            case Algorithms.KRUSKAL:
                self.sets = list(range(len(self.grid_graph)))
                self.replace_set = None
                self.edge = 0
                self.selected_edges = []
            case Algorithms.BORUVKA:
                self.boruvka_end = False
                self.boruvka_walls = []
                self.cheapest = [None] * len(self.components)
                self.component_count = len(self.components)
                self.components = list(range(len(self.grid_graph)))


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
