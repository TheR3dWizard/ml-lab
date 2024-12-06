import math
import numpy as np
from collections import deque 
from typing import List,Set
import copy

class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def distance(self,position):
        return math.sqrt((position.x-self.x)**2 + (position.y-self.y)**2)

    def __add__(self,position):
        return Position(self.x+position.x,self.y+position.y)
    
    def __eq__(self,position):
        return self.x == position.x and self.y == position.y
    
    def __hash__(self) -> int:
        return hash((self.x,self.y))
    
    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"
    


class Maze:
    def __init__(self,array):
        self.maze = array
        self.start = Position(0,0)
        self.end = Position(len(array)-1,len(array[0])-1)

    def inBounds(self,position:Position):
        if position.x < 0 or position.y < 0:
            return False
        if position.x > self.end.x or position.y > self.end.y:
            return False
        return True  

    def getVal(self,position:Position):
        return maze[position.x][position.y]

    def isFree(self,position:Position):
        if self.inBounds(position):
            if self.getVal(position) == 0:
                return True 
        return False
    
    def distance(self,position:Position):
        return math.sqrt((position.x-self.end.x)**2 + (position.y-self.end.y)**2)
    
class Path:
    def __init__(self,nodes:List[Position]=[],length=0):
        self.path = nodes
        self.length = length

    def add(self,position:Position):
        self.length += position.distance(self.path[-1])
        self.path.append(position)

    def getEnd(self):
        return self.path[-1]

    def __repr__(self):
        return f"Nodes: {self.path} Distance: {self.length}"
    
    def copy(self):
        return Path(copy.deepcopy(self.path),self.length)

class Solution:
    def __init__(self):
       self.directions = {
        Position(0,-1), #l
        Position(0,1), #r
        Position(-1,0), #u
        Position(1,0),  #d
        }
       self.visited = set()
       self.visited.add(Position(0,0))
       
    def dfs(self,maze:Maze,path:Path,pos:Position=Position(0,0)):
        # print("Current Position",pos)
        if pos == maze.end:
            return path
        for direction in self.directions:
            nextpos = pos + direction
            # print("Next position: ",nextpos)
            if nextpos in self.visited:
                continue 
            if maze.isFree(nextpos):
                self.visited.add(nextpos)
                path.add(nextpos)
                result =  self.dfs(maze,path,nextpos)
                if result:
                    return result
                

    def bfs(self,maze:Maze):
        queue = deque()
        start = Position(0,0)
        queue.append(Path([start]))
        visited = set()
        visited.add(start)

        while queue != []:
            curpath = queue.popleft()
            if curpath.getEnd() == maze.end:
                return curpath
            for direction in self.directions:
                nextpos = curpath.getEnd()+direction
                if maze.isFree(nextpos):
                    newpath = curpath.copy()
                    newpath.add(nextpos)
                    queue.append(newpath)

    def astar(self,maze:Maze):
        queue:List[Path] = []
        start = Position(0,0)
        queue.append(Path([start]))
        visited = set()
        visited.add(start)

        while queue != []:
            minpath:Path = None
            mindist = float('inf')
            for path in queue:
                hn = maze.distance(path.getEnd())                
                dist = hn + path.length
                if dist < mindist:
                    mindist = dist
                    minpath = path
            if minpath.getEnd() == maze.end:
                return minpath
            queue.remove(minpath)
            for direction in self.directions:
                nextpos = minpath.getEnd()+direction
                if maze.isFree(nextpos) and nextpos not in visited:
                    newpath = minpath.copy()
                    newpath.add(nextpos)
                    visited.add(nextpos)    
                    queue.append(newpath)


                
        


sol = Solution()

maze = np.array([
    [0,0,0,1,0],
    [0,1,0,1,0],
    [0,1,0,0,0],
    [0,1,0,0,0],
    [0,0,0,1,0],
    ]
)

pathDFS = sol.dfs(Maze(maze),Path([Position(0,0)]))
pathBFS = sol.bfs(Maze(maze))
pathAstar = sol.astar(Maze(maze))

print("DFS path: ",pathDFS)
print("bFS path: ",pathBFS)
print("Astar path: ",pathAstar)

# print(Maze(maze).distance(Position(0,0)))

# print(Maze(maze).distance(Position(4,0)))

            

    