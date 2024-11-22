import pygame
import sys
from queue import PriorityQueue

SQUARE_SIZE = 40
HEADER_SIZE = 0

def a_star(screen, clock, maze, start: int, end: int) -> None:
    reached_end = False
    start_node = get_start_node(maze, start)
    end_node = get_end_node(maze, end)
    curr_node = start_node
    curr_cost = 0
    open_set = PriorityQueue()
    open_set.put((manhattan_distance(start_node, end_node), start_node))
    path = {}
    while not reached_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        curr_node.visited = True
        pygame.draw.rect(screen, (0, 0, 0), (curr_node.x * SQUARE_SIZE, curr_node.y * SQUARE_SIZE + HEADER_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        neighbors = curr_node.neighbors
        for neighbor in neighbors:
            if neighbor.visited:
                continue
            path[neighbor] = curr_node
            open_set.put((manhattan_distance(neighbor, end_node), neighbor))
        curr_cost += 1
        next_node = open_set.get()[1]
        curr_node = next_node
        pygame.display.flip()
        clock.tick(20)
        if curr_node.x == end[0] and curr_node.y == end[1]:
            draw_path(screen, clock, curr_node, start_node, path)
            reached_end = True

def draw_path(screen, clock, end_node, start_node, path):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return
    curr_node = end_node
    pygame.draw.rect(screen, (0, 255, 0), (curr_node.x * SQUARE_SIZE, curr_node.y * SQUARE_SIZE + HEADER_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    pygame.display.flip()
    # draw path from the end to the start
    while curr_node != start_node:
        # each node in path maps to its parent node on the path, all the way back to the start
        curr_node = path[curr_node]
        pygame.draw.rect(screen, (0, 255, 0), (curr_node.x * SQUARE_SIZE, curr_node.y * SQUARE_SIZE + HEADER_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pygame.display.flip()
        clock.tick(20)

def get_end_node(edges, end):
    for edge in edges:
        if (edge.node1.x == end[0] and edge.node1.y == end[1]):
            return edge.node1
        elif (edge.node2.x == end[0] and edge.node2.y == end[1]):
            return edge.node2
    return None

def get_start_node(edges, start):
    for edge in edges:
        if (edge.node1.x == start[0] and edge.node1.y == start[1]):
            return edge.node1
        elif (edge.node2.x == start[0] and edge.node2.y == start[1]):
            return edge.node2
    return None
  
# heuristic functions for A*      
def manhattan_distance(node1, node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)

def euclidean_distance(node1, node2):
    return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5