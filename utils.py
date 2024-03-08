from enum import Enum

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
