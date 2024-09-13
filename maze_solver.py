import pygame

def a_star(screen, clock, maze, start, end):
    reached_end = False
    while not reached_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        curr_node = None
        for edge in maze:
            if (edge.node1.x == start[0] and edge.node1.y == start[1]):
                curr_node = edge.node1
                break
            elif (edge.node2.x == start[0] and edge.node2.y == start[1]):
                curr_node = edge.node2
                break
        
        if curr_node == None:
            print("Error: Start node not found in maze")
            return
        
        
    
    
    
    """
    try left, right up down, mark each as visited. If we reach the end, we are done. Else if we reach a dead end, we backtrack to the last visited node and try a different path.
    """