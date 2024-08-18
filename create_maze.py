import random
import pygame

# right, down, left, up
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

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

def draw_maze(width, height, edges):
    """
    Creates the maze of width x height dimensions using Kruskal's algorithm.
    Visually displays process in Pygame window.

    Args:
        width (int): width (highest x value + 1) of the maze
        height (int): height (highest y value + 1) of the maze
        edges (int): list of edges between nodes in the maze

    Returns:
        : 1 on successful completion, else 0
    """
    pygame.init()
    screen = pygame.display.set_mode((width * 40, height * 40))
    clock = pygame.time.Clock()
    screen.fill((153, 204, 255))

    for i in range(width):
        for j in range(height):
            x = i * 40
            y = j * 40

            pygame.draw.line(screen, (255, 255, 255), (x, y), (x + 40, y), 1)  # Top wall
            pygame.draw.line(screen, (255, 255, 255), (x, y), (x, y + 40), 1)  # Left wall
            pygame.draw.line(screen, (255, 255, 255), (x + 40, y), (x + 40, y + 40), 1)  # Right wall
            pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x + 40, y + 40), 1)  # Bottom wall
    
    pygame.display.flip()
    n = width * height
    minSpanningTree = []

    while len(minSpanningTree) < n - 1:
        edge = edges.pop(0)
        if edge.node1.group != edge.node2.group:
            minSpanningTree.append(edge)
            edge.node1.union(edge.node2)
            node1 = edge.node1
            node2 = edge.node2

            x1, y1 = node1.x, node1.y
            x2, y2 = node2.x, node2.y


            if x1 == x2 and y1 == y2 - 1:  # node2 is below node1
                pygame.draw.line(screen, (153, 204, 255), (node1.x * 40, node1.y * 40 + 40), (node1.x * 40 + 40, node1.y * 40 + 40), 1)
                print("removed bottom wall")
            elif x1 == x2 and y1 == y2 + 1:  # node2 is above node1
                pygame.draw.line(screen, (153, 204, 255), (node2.x * 40, node2.y * 40 + 40), (node2.x * 40 + 40, node2.y * 40 + 40), 1)
                print("removed top wall")
            elif x1 == x2 - 1 and y1 == y2:  # node2 is to the right of node1
                pygame.draw.line(screen, (153, 204, 255), (node1.x * 40 + 40, node1.y * 40), (node1.x * 40 + 40, node1.y * 40 + 40), 1)
                print("removed right wall")
            elif x1 == x2 + 1 and y1 == y2:  # node2 is to the left of node1
                pygame.draw.line(screen, (153, 204, 255), (node2.x * 40 + 40, node2.y * 40), (node2.x * 40 + 40, node2.y * 40 + 40), 1)
                print("removed left wall")


            pygame.display.update()
            clock.tick(100)
        else:
            continue
        print(str(edge))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)

    pygame.quit()
    return 1

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.group = set()
        self.group.add(self)
    
    def union(self, other):
        self.group.update(other.group)
        for node in other.group:
            node.group = self.group
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return f"({self.x}, {self.y})"

class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
    
    def __str__(self):
        return f"{self.node1} -> {self.node2}"

if __name__ == "__main__":
    width = 20
    height = 20
    edges = get_grid(width, height)
    draw_maze(width, height, edges)