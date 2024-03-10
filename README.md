# Description

A simple application to visualize [MST](https://en.wikipedia.org/wiki/Minimum_spanning_tree) algorithms and maze generation algorithms, when a maze is created you can see the solution using some pathfinding algorithms.

## Currently implemented algorithms

For MST:
- [Boruvka's algorithm](https://en.wikipedia.org/wiki/Boruvka%27s_algorithm)
- [Kruskal's algorithm](https://en.wikipedia.org/wiki/Kruskal_algorithm)
- [Prim's algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm)

For Maze generation:
- [Prim's modified algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Iterative_randomized_Prim's_algorithm_(without_stack,_without_sets))

For solving mazes:
- [A*](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [BFS](https://en.wikipedia.org/wiki/Breadth-first_search)
- [DFS](https://en.wikipedia.org/wiki/Depth-first_search)

# Screenshots

![preview1](/assets/preview1.png "Peview1")
![preview2](/assets/preview2.png "Peview2")

# Dependencies

- [python](https://www.python.org/) 3.10 or newer
- [pygame](https://www.pygame.org/docs/)

To install pygame in windows:

```
pip install pygame
```

in linux:

```
pip3 install pygame
```

# Download

```
git clone https://github.com/adriangm10/maze-mst-viewer.git
cd maze-mst-viewer
```

# Usage

To run the project in windows:

```
python visualizer.py
```
To run the project in linux:

```
python3 visualizer.py
```

or just `./visualizer.py`
