import random
import pygame
import time
from maze_solver import a_star

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
FONT_SIZE = 22

# Colors
button_color = (0, 128, 255)
text_color = (255, 255, 255)

# Button properties
btn_reset_maze = pygame.Rect(825, 100, 100, 75)
btn_maze_start = pygame.Rect(825, 200, 100, 75)


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


def draw_maze(width, height, screen, clock, edges, fast=False):
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
        edge = edges.pop(0)
        # Kruskal's algorithm: if the nodes are in different sets,
        # put them in the same set and add the edge to the minimum spanning tree
        if edge.node1.group != edge.node2.group:
            minSpanningTree.append(edge)
            edge.node1.union(edge.node2)
            node1 = edge.node1
            node2 = edge.node2
            node1.neighbors.append(node2)
            node2.neighbors.append(node1)
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
            if not fast:
                clock.tick(60)
            else:
                # draw the maze all at once
                clock.tick(1000)
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

    Returns:
        : the minimum spanning tree on successful completion, else None
    """
    pygame.init()
    screen = pygame.display.set_mode(
        (width * SQUARE_SIZE + SIDE_PANEL_SIZE, height * SQUARE_SIZE + HEADER_SIZE)
    )
    clock = pygame.time.Clock()
    screen.fill(LIGHT_BLUE)
    # Draw header (none right now)
    pygame.draw.rect(screen, (LIGHT_GRAY), (0, 0, width * SQUARE_SIZE, HEADER_SIZE))
    # Draw side panel with buttons
    pygame.draw.rect(screen, (LIGHT_GRAY), (width * SQUARE_SIZE, 0, SIDE_PANEL_SIZE, height * SQUARE_SIZE))

    # Flag to avoid recreating the maze on every iteration
    firstRun = True
    running = True
    choosing_start = False
    lock_points = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_maze_start.collidepoint(event.pos):
                    choosing_start = True
                elif btn_reset_maze.collidepoint(event.pos):
                    edges = get_grid(width, height)
                    draw_grid(width, height, screen)
                    maze = draw_maze(width, height, screen, clock, edges)
                    if maze == None:
                        running = False
        
        if firstRun:
            start_text = ["Set", "Maze Start"]
            draw_button(screen, start_text, btn_maze_start, button_color, text_color, "Calibri.ttf", FONT_SIZE)
            reset_text = ["Reset", "Maze"]
            draw_button(screen, reset_text, btn_reset_maze, button_color, text_color, "Calibri.ttf", FONT_SIZE)
            firstRun = False
            edges = get_grid(width, height)
            draw_grid(width, height, screen)
            maze = draw_maze(width, height, screen, clock, edges)
            if maze == None:
                running = False
        
        if choosing_start and not lock_points:
            done_choosing, start_end = choose_start(screen, clock)
            if done_choosing:
                choosing_start = False
                lock_points = start_end is not None
            else:
                running = False
                
        if lock_points:
            a_star(screen, clock, maze, start_end[0], start_end[1])
            time.sleep(3)
            running = False
        
        
        # setting frame rate to 60fps max
        clock.tick(60)
    pygame.quit()

    return maze

def choose_start(screen, clock):
    done_choosing = False
    while not done_choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None  # Indicate that we should quit the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Get the position of the mouse
                    x, y = event.pos
                    # Find which grid cell the mouse is in
                    start_x = x // SQUARE_SIZE
                    start_y = y // SQUARE_SIZE
                    if start_x < WIDTH and start_y < HEIGHT: # User chose a valid start position                        
                        # now user has to choose an end location
                        rval, (end_x, end_y) = choose_end(screen, clock, (start_x, start_y))
                        if not rval:
                            return False, None # first False indicates that we should quit the game
                        return True, ((start_x, start_y), (end_x, end_y))
                    elif btn_maze_start.collidepoint(event.pos): # User clicked start to cancel choosing
                        done_choosing = True
                        return True, None

        pygame.display.flip()
        clock.tick(60)  # Maintain 60 FPS
        
    return True  # Indicate no need to quit the game

def choose_end(screen, clock, start_btn):
    done_choosing = False
    start_x = start_btn[0]
    start_y = start_btn[1]
    grid_x = -1
    grid_y = -1
    color = (0, 255, 0)
    while not done_choosing:
        if color == (0, 255, 0):
            color = LIGHT_BLUE
        else:
            color = (0, 255, 0)
        flash_square(screen, start_x, start_y, color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Get the position of the mouse
                    x, y = event.pos
                    # Find which grid cell the mouse is in
                    grid_x = x // SQUARE_SIZE
                    grid_y = y // SQUARE_SIZE
                    if grid_x < WIDTH and grid_y < HEIGHT: # User chose a valid end position
                        flash_square(screen, start_x, start_y, (0, 255, 0))
                        flash_square(screen, grid_x, grid_y, (255, 0, 0))
                        done_choosing = True

        pygame.display.flip()
        clock.tick(60)  # Maintain 60 FPS
        
    return True, (grid_x, grid_y)

def flash_square(screen, x, y, color):
    pygame.draw.rect(screen, color, (x * SQUARE_SIZE + 1, y * SQUARE_SIZE + HEADER_SIZE + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1))
    pygame.display.flip()
    time.sleep(0.5)
    

def draw_button(surface, text_lines, rect, button_color, text_color, font=None, font_size=36):
    # Draw the button rectangle
    pygame.draw.rect(surface, button_color, rect)
    
    if font:
        font = pygame.font.Font(font, font_size)
    else:
        font = pygame.font.Font(None, font_size)
    
    # Calculate total height of text block
    total_height = sum(font.size(line)[1] for line in text_lines)
    
    # Calculate the starting position to center text block vertically
    y_offset = rect.centery - total_height // 2
    
    # Render and blit each line of text
    for line in text_lines:
        text_surf = font.render(line, True, text_color)
        text_rect = text_surf.get_rect(center=(rect.centerx, y_offset + text_surf.get_height() // 2))
        surface.blit(text_surf, text_rect)
        y_offset += text_surf.get_height()  # Move y_offset down for next line of text


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.neighbors = []
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

    # Equality check needed for dictionary keys and sets
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Comparison for sorting and priority queue operations
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

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
