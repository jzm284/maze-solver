import pygame
from queue import PriorityQueue
from create_maze import 


def a_star(screen, clock, maze, start: int, end: int) -> None:
    reached_end = False
    curr_node = get_start_node(maze, start)
    curr_cost = 0
    open_set = PriorityQueue()
    open_set.put((0 + manhattan_distance(curr_node, end), curr_node))
    while not reached_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        if curr_node.x == end[0] and curr_node.y == end[1]:
            reached_end = True
            break
        
        neighbors = curr_node.neighbors
        for neighbor in neighbors:
            cost = curr_cost + 1 + manhattan_distance(neighbor, end)
            open_set.put((cost, neighbor))
        curr_cost += 1
        curr_node = open_set.get()[1]
        
    
def get_start_node(edges, start):
    curr_node = None
    for edge in edges:
        if (edge.node1.x == start[0] and edge.node1.y == start[1]):
            curr_node = edge.node1
            break
        elif (edge.node2.x == start[0] and edge.node2.y == start[1]):
            curr_node = edge.node2
            break
    
    if curr_node == None:
        print("Error: Start node not found in maze")
        return
        
def manhattan_distance(node1, node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)