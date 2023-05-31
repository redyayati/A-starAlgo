# Changing visualization so that path looks better
import pygame as pg 
import pygame.gfxdraw
import random

pg.init()
width = 800
height = 800
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock() 
running  = True

base_font = pg.font.SysFont('consolas', 20)
textColor = (0,0,0)

size = 10
cols = int(width/size)
rows = int(height/size)
w = size
h = size
grid = [[0 for _ in range(cols)] for _ in range(rows)] #initializing a 2D Array matrix
openSet = []  # Containes all the nodes and neighbors that need to be traversed and assigned f,g and h values
closedSet = [] # Contains all the elements that are best option from openSet
path = []

class Spot : 
    def __init__(self,i,j) : 
        self.i = i 
        self.j = j 
        self.f = 0 
        self.h = 0 
        self.g = 0 
        self.neighbors = []
        self.previous= None 
        self.wall = False
        if random.random() < .3 : self.wall = True

    def show(self) : 
        x = self.i * w
        y = self.j * h 
        gray = 150,150,150
        black = 0,0,0
        if self.wall :
            pg.draw.circle(screen,black, (int(x+(size/2)),int(y+(size/2))), int(size/2.5))
        pg.draw.rect(screen, gray, (x,y,w,h), 1)
        
    def addNeighbors(self, grid) : 
        i = self.i
        j = self.j 
        if i < cols-1 : 
            self.neighbors.append(grid[j][i+1])
        if i > 0 : 
            self.neighbors.append(grid[j][i-1])
        if j < rows-1 : 
            self.neighbors.append(grid[j+1][i])
        if j > 0 :
            self.neighbors.append(grid[j-1][i])
        # Diagonals : 
        if i > 0 and j > 0 : 
            self.neighbors.append(grid[j-1][i-1])
        if i < cols-1 and j > 0 : 
            self.neighbors.append(grid[j-1][i+1])
        if i > 0 and j < rows-1 : 
            self.neighbors.append(grid[j+1][i-1])
        if j < rows-1 and i < cols-1 : 
            self.neighbors.append(grid[j+1][i+1])
def drawPath(path) : 
    start = int(path[0].i * w + (size/2)) , int(path[0].j * h + (size/2))
    for point in path : 
        end = int(point.i * w +(size/2)), int(point.j * h+(size/2))
        red = (255,0,0)
        pg.draw.line(screen,red,start, end, 3 )
        start = end
def heuristic(a,b) : 
    x1 , y1 = a.i , a.j
    x2 , y2 = b.i , b.j
    d = (x2 - x1)**2 + (y2-y1)**2
    return d**(1/2) 
def manhattenHeuristic(a,b): 
    d = abs(a.i - b.i) + abs(a.j-b.j)
    return d

def resetGrid(grid) : 
    n = 0 
    for row in range(rows) : 
        for col in range(cols) : 
            grid[row][col].f = 0
            grid[row][col].g = 0
            grid[row][col].h = 0
            grid[row][col].previous = None 
    openSet = []
    closedSet = []
    path = []
    return grid , openSet, closedSet, path , n 



for row in range(rows) : 
    for col in range(cols) : 
        grid[row][col] = Spot(col,row)
        
for row in range(rows) : 
    for col in range(cols) : 
        grid[row][col].addNeighbors(grid)  


start = grid[0][0]
end = grid[rows-1][cols-1]
start.wall = False
end.wall = False
openSet.append(start) #openSet has starting point to start with. 

n = 0
solution = True

while running : 
    screen.fill((255,255,255))
    if n == 0 : # This is to stop the loop when its done 
        if len(openSet) > 0 :  # As long as there are nodes to evaluate in openSet, keep going 
            lowestFindex = 0 #searching for next best option in the following loop
            for element in openSet : 
                if element.f < openSet[lowestFindex].f : 
                    lowestFindex = openSet.index(element)
            current = openSet[lowestFindex]
            
            if current == end : # check If we reach the end 
                # Path Evaluation 
                path = []
                temp = current
                path.append(temp)
                while temp.previous != None : 
                    path.append(temp.previous) # adding previous parent to the path array to generate path 
                    temp = temp.previous
                print(len(path))
                print("DONE !!")
                n +=1 # we quit the loop by adding 1 to variable "n" since the loop runs at n==0

            #Best option moves from openSet to closedSet
            closedSet.append(current) 
            openSet.remove(current) 
            #check all the neighbors
            neighbors = current.neighbors
            # Looping thru every neighbor to assign them f value
            for neighbor in neighbors : 
                    if neighbor not in closedSet and not neighbor.wall: # examin only when it is not in closedSet
                        tempG = current.g + 1 
                        betterNode = False
                        if neighbor in openSet :  # check if it has a better previous g
                            if tempG < neighbor.g : 
                                neighbor.g = tempG
                                betterNode = True # since this is a better node, we should update its f value and porevious as current 
                        else : 
                            neighbor.g = tempG
                            openSet.append(neighbor)
                            betterNode = True # this is obvioulsy a better node since this was not existing in openSet before , we should update its f value and porevious as current 
                        if betterNode :   # we want to calculate f value and set current as previous only if its a better path
                            # neighbor.h = heuristic(neighbor,end)
                            neighbor.h = manhattenHeuristic(neighbor,end)
                            neighbor.f = neighbor.g + neighbor.h 
                            neighbor.previous = current # assiging previous to track path later 
            
        else : # No Solution  
            solution = False
    # Display Part 
    for i in range(rows) :
        for j in range(cols) :  
            grid[i][j].show() # All squares in grid are shown in this color
    path = []
    temp = current
    path.append(temp)
    while temp.previous != None : 
        path.append(temp.previous) # adding previous parent to the path array to generate path 
        temp = temp.previous
    # for closed in closedSet : closed.show() # All squares in closedSet are in this color
    # for opened in openSet : opened.show((80,255,80)) # All in OpenSet are in this color

    drawPath(path)

    if solution == False : # Prompt for NO solution
        pg.draw.rect(screen,(255,255,255), (80,190,250,45) )
        text = base_font.render("No Solution, hit 'R' " ,True,textColor)  #For a square size of 83
        screen.blit(text,(100, 200))
    for event in pg.event.get() : 
        if event.type == pg.QUIT : 
            running = False 
        elif event.type == pg.KEYDOWN : 
            if event.key == pg.K_q : 
                running = False 
            if event.key == pg.K_r : 
                n = 0
                for row in range(rows) : 
                    for col in range(cols) : 
                        grid[row][col].f = 0
                        grid[row][col].g = 0
                        grid[row][col].h = 0
                        grid[row][col].previous = None
                        grid[row][col].wall = False
                        if random.random() < .3 : grid[row][col].wall = True
                start.wall = False
                end.wall = False
                openSet = [start]
                closedSet = [] 
                solution = True
    pg.display.flip()
    clock.tick(50)
pg.quit()
