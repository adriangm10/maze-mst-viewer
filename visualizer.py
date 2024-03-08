#!/bin/python3

from enum import Enum
from time import sleep

import pygame

from maze import Maze
from pathfinders import Astar, Bfs, Dfs
from utils import Algorithms
from widgets import Button, Scale

pygame.init()

WIDTH = 1000
HEIGHT = 800
pause = False

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("maze_generator")

public_pixel = pygame.font.Font("fonts/PublicPixel-z84yD.ttf", 14)


class State(Enum):
    CREATING = 0
    SOLVING = 1


state = State.CREATING

button_colors = {
    "bg": (0, 0, 0),
    "fg": (255, 255, 255),
    "hover": (83, 104, 120),
    "border": (112, 128, 144),
}
GREEN = (0, 255, 159)
RED = (255, 18, 65)
PINK = (234, 0, 217)

MST_ALGS_POSX = 25
MAZE_ALGS_POSX = 200
PATHFINDER_POSX = 400
SETTINGS_POSX = 600


def pause_continue(button: Button):
    global pause
    pause = not pause
    button.label = "Pause" if not pause else "Continue"


def restart_maze(button: Button, maze: Maze):
    global state
    state = State.CREATING
    maze.restart()


def change_generation_alg(button: Button, maze: Maze, alg: Algorithms):
    global state
    state = State.CREATING
    maze.set_generation_mode(alg)


def solve_bfs(button: Button, maze: Maze):
    global state
    state = State.SOLVING
    button.set_border_color(PINK)
    dfs_button.set_border_color(button_colors["border"])
    astar_button.set_border_color(button_colors["border"])
    bfs = Bfs(maze)
    maze.set_path_finder(bfs)


def solve_dfs(button: Button, maze: Maze):
    global state
    state = State.SOLVING
    button.set_border_color(PINK)
    bfs_button.set_border_color(button_colors["border"])
    astar_button.set_border_color(button_colors["border"])
    bfs = Dfs(maze)
    maze.set_path_finder(bfs)


def solve_astar(button: Button, maze: Maze):
    global state
    state = State.SOLVING
    button.set_border_color(PINK)
    bfs_button.set_border_color(button_colors["border"])
    dfs_button.set_border_color(button_colors["border"])
    bfs = Astar(maze)
    maze.set_path_finder(bfs)


def draw_text():
    mst = public_pixel.render("MST", True, (255, 255, 255))
    window.blit(mst, (MST_ALGS_POSX, 550))

    maze = public_pixel.render("MAZE", True, (255, 255, 255))
    window.blit(maze, (MAZE_ALGS_POSX, 550))

    pathfinders = public_pixel.render("Pathfinders", True, (255, 255, 255))
    window.blit(pathfinders, (PATHFINDER_POSX, 550))

    settings = public_pixel.render("Settings", True, (255, 255, 255))
    window.blit(settings, (SETTINGS_POSX, 550))

    change_size = public_pixel.render("cell size", True, (255, 255, 255))
    window.blit(change_size, (SETTINGS_POSX + 175, 570))

    delay = public_pixel.render("delay (s)", True, (255, 255, 255))
    window.blit(delay, (SETTINGS_POSX + 175, 625))


# To simulate pointers the maze is passed in a list
def change_cell_size(scale: Scale):
    global maze
    maze = Maze(maze.rect, int(scale.value), maze.max_cost, maze.color)
    maze.draw_grid_points(window)


def change_delay(scale: Scale):
    global delay
    delay = scale.value


if __name__ == "__main__":
    running = True

    # MST-Maze algorithms
    kruskal_button = Button(
        pygame.Rect(MST_ALGS_POSX, 600, 150, 25),
        public_pixel,
        button_colors,
        label="Kruskal",
        onClick=change_generation_alg,
    )

    prim_button = Button(
        pygame.Rect(MST_ALGS_POSX, 650, 150, 25),
        public_pixel,
        button_colors,
        label="Prim",
        onClick=change_generation_alg,
    )

    boruvka_button = Button(
        pygame.Rect(MST_ALGS_POSX, 700, 150, 25),
        public_pixel,
        button_colors,
        label="Boruvka",
        onClick=change_generation_alg,
    )

    prim_maze_button = Button(
        pygame.Rect(MAZE_ALGS_POSX, 600, 150, 25),
        public_pixel,
        button_colors,
        label="Prim Maze",
        onClick=change_generation_alg,
    )

    # Pathfinding algorithms
    bfs_button = Button(
        pygame.Rect(PATHFINDER_POSX, 600, 150, 25),
        public_pixel,
        button_colors,
        label="BFS",
        onClick=solve_bfs,
    )

    dfs_button = Button(
        pygame.Rect(PATHFINDER_POSX, 650, 150, 25),
        public_pixel,
        button_colors,
        label="DFS",
        onClick=solve_dfs,
    )

    astar_button = Button(
        pygame.Rect(PATHFINDER_POSX, 700, 150, 25),
        public_pixel,
        button_colors,
        label="A*",
        onClick=solve_astar,
    )

    # Control buttons
    pause_button = Button(
        pygame.Rect(SETTINGS_POSX, 600, 150, 25),
        public_pixel,
        button_colors,
        label="Pause",
        onClick=pause_continue,
    )

    restart_button = Button(
        pygame.Rect(SETTINGS_POSX, 650, 150, 25),
        public_pixel,
        button_colors,
        label="Restart",
        onClick=restart_maze,
    )
    restart_button.set_hover_color(RED)
    restart_button.set_border_color(RED)

    cell_size = 20

    size_scale = Scale(
        20,
        50,
        100,
        (SETTINGS_POSX + 175, 600),
        7,
        public_pixel,
        onClick=change_cell_size,
    )

    delay_scale = Scale(
        0,
        0.1,
        100,
        (SETTINGS_POSX + 175, 650),
        7,
        public_pixel,
        onClick=change_delay,
        padding=23,
    )

    delay_scale.set_value(0.02)

    maze = Maze(
        pygame.Rect(10, 10, WIDTH - 20, 500), int(size_scale.value), max_cost=1000
    )

    delay = delay_scale.value

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not maze.is_fully_created() and not pause:
            bfs_button.set_active(False)
            dfs_button.set_active(False)
            astar_button.set_active(False)
            maze.new_wall()
            sleep(delay)
        else:
            if maze.generation_mode == Algorithms.PRIM_MAZE and maze.is_fully_created():
                bfs_button.set_active(True)
                dfs_button.set_active(True)
                astar_button.set_active(True)
                if state == State.SOLVING and not pause:
                    maze.solve_step()
                maze.draw_solution(window)
                sleep(delay)

        match maze.generation_mode:
            case Algorithms.KRUSKAL:
                kruskal_button.set_border_color(GREEN)
                prim_button.set_border_color(button_colors["border"])
                boruvka_button.set_border_color(button_colors["border"])
                prim_maze_button.set_border_color(button_colors["border"])

            case Algorithms.PRIM:
                prim_button.set_border_color(GREEN)
                kruskal_button.set_border_color(button_colors["border"])
                boruvka_button.set_border_color(button_colors["border"])
                prim_maze_button.set_border_color(button_colors["border"])

            case Algorithms.BORUVKA:
                boruvka_button.set_border_color(GREEN)
                kruskal_button.set_border_color(button_colors["border"])
                prim_button.set_border_color(button_colors["border"])
                prim_maze_button.set_border_color(button_colors["border"])

            case Algorithms.PRIM_MAZE:
                prim_maze_button.set_border_color(GREEN)
                kruskal_button.set_border_color(button_colors["border"])
                prim_button.set_border_color(button_colors["border"])
                boruvka_button.set_border_color(button_colors["border"])

        if pause:
            pause_button.set_border_color(RED)
        else:
            pause_button.set_border_color(button_colors["border"])

        pause_button.process()
        restart_button.process(maze)
        kruskal_button.process(maze, Algorithms.KRUSKAL)
        prim_button.process(maze, Algorithms.PRIM)
        boruvka_button.process(maze, Algorithms.BORUVKA)
        prim_maze_button.process(maze, Algorithms.PRIM_MAZE)
        bfs_button.process(maze)
        dfs_button.process(maze)
        astar_button.process(maze)

        size_scale.process()
        delay_scale.process()

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

        size_scale.draw(window)
        delay_scale.draw(window)
        draw_text()

        pygame.display.update()
        window.fill((0, 0, 0))

    pygame.quit()
