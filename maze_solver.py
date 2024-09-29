import pygame
from queue import PriorityQueue


def a_star(screen, clock, maze, start: int, end: int) -> None:
    reached_end = False
    start_node = get_start_node(maze, start)
    curr_node = start_node
    curr_cost = 0
    open_set = PriorityQueue()
    open_set.put(0 + manhattan_distance(curr_node, end), curr_node)
    path = {}
    while not reached_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        if curr_node.x == end[0] and curr_node.y == end[1]:
            reached_end = True
            draw_path(screen, curr_node, start_node, path)
            break
        elif open_set.empty():
            print("No path found")
            return
        
        pygame.draw.rect(screen, (0, 0, 0), (curr_node.x * 20, curr_node.y * 20, 20, 20))
        neighbors = curr_node.neighbors
        for neighbor in neighbors:
            cost = curr_cost + 1 + manhattan_distance(neighbor, end)
            open_set.put((cost, neighbor))
        curr_cost += 1
        next_node = open_set.get()[1]
        path[next_node] = curr_node
        curr_node = next_node
        pygame.display.flip()
        clock.tick(60)

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
  
# heuristic function for A*      
def manhattan_distance(node1, node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)