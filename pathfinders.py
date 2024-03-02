from collections import deque

import pygame

from maze import Maze
from utils import PathFinder


class Bfs(PathFinder):
    def __init__(self, maze: Maze):
        self.maze = maze
        self.start = maze.start
        self.target = maze.target
        self.queue = deque([(maze.start, [maze.start])])
        self.visited = set([maze.start])
        self.path = [self.start]
        self.finished = False

    def next_step(self):
        if not self.queue:
            self.finished = True
            return

        pos, self.path = self.queue.pop()

        if pos == self.target:
            self.finished = True
            return

        for cell in self.maze.next_cells(pos):
            if cell not in self.visited:
                self.queue.appendleft((cell, self.path + [cell]))
                self.visited.add(cell)

    def has_finished(self):
        return self.finished

    def restart(self):
        self.queue = deque([(self.start, [self.start])])
        self.visited = set([self.start])
        self.path = []
        self.finished = False

    def draw(
        self,
        surface: pygame.Surface,
        xnode_count: int,
        cell_size: int,
        rect: pygame.Rect,
        visited_color: pygame.Color,
        path_color: pygame.Color,
    ):
        if self.finished:
            for c in self.path:
                cell_pos = c[1] * cell_size + rect.x, c[0] * cell_size + rect.y
                pygame.draw.rect(
                    surface,
                    path_color,
                    (cell_pos[0], cell_pos[1], cell_size, cell_size),
                )
        else:
            for c in self.visited:
                cell_pos = c[1] * cell_size + rect.x, c[0] * cell_size + rect.y
                pygame.draw.rect(
                    surface,
                    visited_color,
                    (cell_pos[0], cell_pos[1], cell_size, cell_size),
                )
