#!/bin/python3

from enum import Enum
from time import sleep

import pygame

from maze import Maze
from pathfinders import Astar, Bfs, Dfs, manhattan_distance
from utils import Algorithms, Button

pygame.init()

WIDTH = 1000
HEIGHT = 800
pause = False

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("maze_generator")

arial = pygame.font.SysFont("arial", 14)


class State(Enum):
    CREATING = 0
    SOLVING = 1


state = State.CREATING


def pause_continue(button: Button):
    global pause
    pause = not pause
    button.label = "Pause" if not pause else "Continue"


def restart_maze(maze: Maze):
    global state
    state = State.CREATING
    maze.restart()


def change_generation_alg(maze: Maze, alg: Algorithms):
    global state
    state = State.CREATING
    maze.set_generation_mode(alg)


def solve_bfs(maze: Maze):
    global state
    state = State.SOLVING
    bfs = Bfs(maze)
    maze.set_path_finder(bfs)


def solve_dfs(maze: Maze):
    global state
    state = State.SOLVING
    bfs = Dfs(maze)
    maze.set_path_finder(bfs)


def solve_astar(maze: Maze):
    global state
    state = State.SOLVING
    bfs = Astar(maze, manhattan_distance)
    maze.set_path_finder(bfs)


if __name__ == "__main__":
    running = True
    kruskal_button = Button(
        pygame.Rect(WIDTH / 2 - 300, 600, 100, 25),
        arial,
        label="Kruskal",
        onClick=change_generation_alg,
    )
    prim_button = Button(
        pygame.Rect(WIDTH / 2 - 150, 600, 100, 25),
        arial,
        label="Prim",
        onClick=change_generation_alg,
    )
    boruvka_button = Button(
        pygame.Rect(WIDTH / 2 - 150, 700, 100, 25),
        arial,
        label="Boruvka",
        onClick=change_generation_alg,
    )
    prim_maze_button = Button(
        pygame.Rect(WIDTH / 2 - 300, 700, 100, 25),
        arial,
        label="Prim Maze",
        onClick=change_generation_alg,
    )
    pause_button = Button(
        pygame.Rect(WIDTH / 2 + 50, 600, 100, 25),
        arial,
        label="Pause",
        onClick=pause_continue,
    )
    restart_button = Button(
        pygame.Rect(WIDTH / 2 + 200, 600, 100, 25),
        arial,
        label="Restart",
        onClick=restart_maze,
    )
    bfs_button = Button(
        pygame.Rect(WIDTH / 2 + 50, 700, 100, 25),
        arial,
        label="Solve bfs",
        onClick=solve_bfs,
    )
    dfs_button = Button(
        pygame.Rect(WIDTH / 2 + 200, 700, 100, 25),
        arial,
        label="Solve dfs",
        onClick=solve_dfs,
    )
    astar_button = Button(
        pygame.Rect(WIDTH / 2 + 200, 750, 100, 25),
        arial,
        label="Solve A*",
        onClick=solve_astar,
    )
    maze = Maze(pygame.Rect(10, 10, WIDTH - 20, 500), 20, max_cost=1000)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not maze.is_fully_created() and not pause:
            bfs_button.set_active(False)
            dfs_button.set_active(False)
            astar_button.set_active(False)
            maze.new_wall()
            sleep(0.001)
        else:
            if maze.generation_mode == Algorithms.PRIM_MAZE and maze.is_fully_created():
                bfs_button.set_active(True)
                dfs_button.set_active(True)
                astar_button.set_active(True)
                if state == State.SOLVING and not pause:
                    maze.solve_step()
                maze.draw_solution(window)
                sleep(0.01)

        pause_button.process(pause_button)
        restart_button.process(maze)
        kruskal_button.process(maze, Algorithms.KRUSKAL)
        prim_button.process(maze, Algorithms.PRIM)
        boruvka_button.process(maze, Algorithms.BORUVKA)
        prim_maze_button.process(maze, Algorithms.PRIM_MAZE)
        bfs_button.process(maze)
        dfs_button.process(maze)
        astar_button.process(maze)

        maze.draw_maze(window)
        pause_button.draw(window)
        restart_button.draw(window)
        kruskal_button.draw(window)
        boruvka_button.draw(window)
        prim_button.draw(window)
        prim_maze_button.draw(window)
        bfs_button.draw(window)
        dfs_button.draw(window)
        astar_button.draw(window)

        pygame.display.update()
        window.fill((0, 0, 0))

    pygame.quit()
