import random
import pygame

# right, down, left, up
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
LIGHT_BLUE = (153, 204, 255)
LIGHT_GRAY = (83, 83, 83)
WHITE = (255, 255, 255)

WIDTH = 20
HEIGHT = 20
SQUARE_SIZE = 40
HEADER_SIZE = 0
SIDE_PANEL_SIZE = 150


def get_grid(width: int, height: int):
    """
    Generates a grid of width x height nodes with edges between adjacent nodes
    (up, down, left, right). Edges are shuffled randomly and returned for use in
    Kruskal's algorithm (finding a random minimum spanning tree aka a perfect maze).

    Args:
        width (int): The width of the grid.
        height (int): The height of the grid.

    Returns:
        globalEdges: A list of shuffled edges between adjacent nodes in the grid.
    """
    grid = [[Node(x, y) for y in range(height)] for x in range(width)]
    globalEdges = []

    for i in range(width):
        for j in range(height):
            node = grid[i][j]
            for direction in directions:
                nextX = i + direction[0]
                nextY = j + direction[1]
                if 0 <= nextX < width and 0 <= nextY < height:
                    edge = Edge(node, grid[nextX][nextY])
                    globalEdges.append(edge)

    # the algorithm calls for assigning random weights to edges and then sorting
    # but shuffling the list produces a similar result
    random.shuffle(globalEdges)

    return globalEdges


def draw_grid(width, height, screen):
    """Draws the grid of the maze in the Pygame window.

    Args:
        width (_int_): The width of the grid.
        height (_int_): The height of the grid.
        screen (_pygame.display_): The Pygame window to draw the maze in.
    """
    for i in range(width):
        for j in range(height):
            x = i * SQUARE_SIZE
            y = j * SQUARE_SIZE

            pygame.draw.line(
                screen,
                WHITE,
                (x, y + HEADER_SIZE),
                (x + SQUARE_SIZE, y + HEADER_SIZE),
                1,
            )  # Top wall
            pygame.draw.line(
                screen,
                WHITE,
                (x, y + HEADER_SIZE),
                (x, y + SQUARE_SIZE + HEADER_SIZE),
                1,
            )  # Left wall
            pygame.draw.line(
                screen,
                WHITE,
                (x + SQUARE_SIZE, y + HEADER_SIZE),
                (x + SQUARE_SIZE, y + SQUARE_SIZE + HEADER_SIZE),
                1,
            )  # Right wall
            pygame.draw.line(
                screen,
                WHITE,
                (x, y + SQUARE_SIZE + HEADER_SIZE),
                (x + SQUARE_SIZE, y + SQUARE_SIZE + HEADER_SIZE),
                1,
            )  # Bottom wall
    pygame.display.flip()


def draw_maze(width, height, screen, clock, edges):
    """
    Draws the maze using Kruskal's algorithm.
    The algorithm finds the minimum spanning tree from a randomly sorted set
    of edges and we draw the maze in a Pygame window in real-time.
    Args:
        width (_int_): _description_
        height (_int_): _description_
        screen (_pygame.display_): The Pygame window to draw the maze in.
        clock (_pygame.Clock_): The Pygame clock to control the frame rate.
        edges (_list(Edge)_): The randomly sorted list of edges.

    Returns:
        minSpanningTree (_list(Edge)_): The random minimum spanning tree of the maze.
        In other words, the minimum (weighted) set of edges required to connect all nodes
        in the maze.
    """
    n = width * height
    minSpanningTree = []

    while len(minSpanningTree) < n - 1:
        edge = edges.pop(0)
        # Kruskal's algorithm: if the nodes are in different sets,
        # put them in the same set and add the edge to the minimum spanning tree
        if edge.node1.group != edge.node2.group:
            minSpanningTree.append(edge)
            edge.node1.union(edge.node2)
            node1 = edge.node1
            node2 = edge.node2

            x1, y1 = node1.x, node1.y
            x2, y2 = node2.x, node2.y

            if x1 == x2 and y1 == y2 - 1:  # node2 is below node1
                pygame.draw.line(
                    screen,
                    LIGHT_BLUE,
                    (x1 * SQUARE_SIZE, y1 * SQUARE_SIZE + SQUARE_SIZE + HEADER_SIZE),
                    (
                        x1 * SQUARE_SIZE + SQUARE_SIZE,
                        y1 * SQUARE_SIZE + SQUARE_SIZE + HEADER_SIZE,
                    ),
                    1,
                )
            elif x1 == x2 and y1 == y2 + 1:  # node2 is above node1
                pygame.draw.line(
                    screen,
                    LIGHT_BLUE,
                    (x2 * SQUARE_SIZE, y2 * SQUARE_SIZE + SQUARE_SIZE + HEADER_SIZE),
                    (
                        x2 * SQUARE_SIZE + SQUARE_SIZE,
                        y2 * SQUARE_SIZE + SQUARE_SIZE + HEADER_SIZE,
                    ),
                    1,
                )
            elif x1 == x2 - 1 and y1 == y2:  # node2 is to the right of node1
                pygame.draw.line(
                    screen,
                    LIGHT_BLUE,
                    (x1 * SQUARE_SIZE + SQUARE_SIZE, y1 * SQUARE_SIZE + HEADER_SIZE),
                    (
                        x1 * SQUARE_SIZE + SQUARE_SIZE,
                        y1 * SQUARE_SIZE + SQUARE_SIZE + HEADER_SIZE,
                    ),
                    1,
                )
            elif x1 == x2 + 1 and y1 == y2:  # node2 is to the left of node1
                pygame.draw.line(
                    screen,
                    LIGHT_BLUE,
                    (x2 * SQUARE_SIZE + SQUARE_SIZE, y2 * SQUARE_SIZE + HEADER_SIZE),
                    (
                        x2 * SQUARE_SIZE + SQUARE_SIZE,
                        y2 * SQUARE_SIZE + SQUARE_SIZE + HEADER_SIZE,
                    ),
                    1,
                )

            pygame.display.update()
            clock.tick(60)
        else:
            continue
    return minSpanningTree


def create_maze(width, height):
    """
    Creates the maze of width x height dimensions using Kruskal's algorithm.
    Visually displays process in Pygame window.

    Args:
        width (_int_): width (highest x value + 1) of the maze
        height (_int_): height (highest y value + 1) of the maze
        edges (_int_): list of edges between nodes in the maze

    Returns:
        : the minimum spanning tree on successful completion, else None
    """
    pygame.init()
    screen = pygame.display.set_mode(
        (width * SQUARE_SIZE + SIDE_PANEL_SIZE, height * SQUARE_SIZE + HEADER_SIZE)
    )
    clock = pygame.time.Clock()
    screen.fill(LIGHT_BLUE)
    pygame.draw.rect(screen, (LIGHT_GRAY), (0, 0, width * SQUARE_SIZE, HEADER_SIZE))
    pygame.draw.rect(screen, (LIGHT_GRAY), (width * SQUARE_SIZE, 0, SIDE_PANEL_SIZE, height * SQUARE_SIZE))

    # Flag to avoid recreating the maze on every iteration
    firstRun = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if firstRun:
            firstRun = False
            edges = get_grid(width, height)
            draw_grid(width, height, screen)
            maze = draw_maze(width, height, screen, clock, edges)
        # setting frame rate to 60fps max
        clock.tick(60)
    pygame.quit()

    return maze


# Node class to represent an (x, y) coordinate in the grid
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.group = set()
        self.group.add(self)

    # Merge two groups of nodes, used in Kruskal's algorithm
    def union(self, other):
        self.group.update(other.group)
        for node in other.group:
            node.group = self.group

    # Hash needed for set operations
    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"


# Edge class to represent an edge between two nodes
class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def __str__(self):
        return f"{self.node1} -> {self.node2}"


if __name__ == "__main__":
    create_maze(WIDTH, HEIGHT)
