import random
import pygame

# right, down, left, up
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def get_grid(width: int, height: int):
    """
    Generates a grid of width x height nodes with edges between adjacent nodes
    (up, down, left, right). Edges are shuffled randomly and returned for use in 
    Kruskal's algorithm (finding a random minimum spanning tree aka a perfect maze).
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