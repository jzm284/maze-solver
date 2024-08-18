import random
import pygame

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

