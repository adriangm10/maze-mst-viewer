#!/bin/python3

from time import sleep

import pygame

from utils import Algorithms, Button, Maze

pygame.init()

WIDTH = 1000
HEIGHT = 800
pause = False

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("maze_generator")

arial = pygame.font.SysFont("arial", 14)


def pause_continue(button: Button):
    global pause
    pause = not pause
    button.label = "Pause" if not pause else "Continue"


def restart_maze(maze: Maze):
    maze.restart()


def change_generation_alg(maze: Maze, alg: Algorithms):
    maze.set_generation_mode(alg)


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
    maze = Maze(pygame.Rect(10, 10, WIDTH - 20, 500), 20, max_cost=1000)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not maze.is_fully_created() and not pause:
            maze.new_wall()
            sleep(0.01)

        pause_button.process(pause_button)
        restart_button.process(maze)
        kruskal_button.process(maze, Algorithms.KRUSKAL)
        prim_button.process(maze, Algorithms.PRIM)
        boruvka_button.process(maze, Algorithms.BORUVKA)

        maze.draw_maze(window)
        pause_button.draw(window)
        restart_button.draw(window)
        kruskal_button.draw(window)
        boruvka_button.draw(window)
        prim_button.draw(window)
        pygame.display.update()

        window.fill((0, 0, 0))

    pygame.quit()
