import pygame

def a_star(screen, clock, maze, start, end):
    reached_end = False
    while not reached_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
    
    
    
    
    """
    try left, right up down, mark each as visited. If we reach the end, we are done. Else if we reach a dead end, we backtrack to the last visited node and try a different path.
    """