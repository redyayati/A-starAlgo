# A* algorithm 
import pygame as pg 
import pygame.gfxdraw
pg.init()
width = 500
height = 500
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock() 
running  = True

base_font = pg.font.SysFont('consolas', 10)
textColor = (150,150,150)


size = 20
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
    def show(self, color) : 
        x = self.i * w
        y = self.j * h 
        pg.draw.rect(screen, color, (x,y,w-1,h-1))
        pg.draw.rect(screen, ("gray"), (x,y,w-1,h-1), 1)
        # text = base_font.render(str(self.i) +","+ str(self.j),True,textColor)  #For a square size of 83
        # screen.blit(text,(x ,y ))
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

def heuristic(a,b) :  # this heuristic uses euclidian diatance from the spot to the end point
    x1 , y1 = a.i , a.j
    x2 , y2 = b.i , b.j
    d = (x2 - x1)**2 + (y2-y1)**2
    return d**(1/2) 
def manhattenHeuristic(a,b): # this heuristic uses summation of delta X and delta Y between sopt and end Point 
    d = abs(a.i - b.i) + abs(a.j-b.j)
    return d
  
for row in range(rows) : 
    for col in range(cols) : 
        grid[row][col] = Spot(col,row)
        
for row in range(rows) : 
    for col in range(cols) : 
        grid[row][col].addNeighbors(grid)  


start = grid[0][0]
end = grid[rows-1][cols-1]
openSet.append(start) #openSet has starting point to start with. 

n = 0
loop1 = 1
loop2 = 1
looping = False
while running : 
    screen.fill((255,255,255))
    if n == 0 : # This is to stop the loop when its done 
        if openSet != None :  # As long as there are nodes to evaluate in openSet, keep going 
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
                print("DONE !!")
                n +=1 # we quit the loop by adding 1 to variable "n" since the loop runs at n==0

            #Best option moves from openSet to closedSet
            closedSet.append(current) 
            openSet.remove(current) 
            #check all the neighbors
            neighbors = current.neighbors
            # Looping thru every neighbor to assign them f value
            for neighbor in neighbors : 
                    if neighbor not in closedSet : # examin only when it is not in closedSet
                        tempG = current.g + 1 
                        if neighbor in openSet :  # check if it has a better previous g
                            if tempG < neighbor.g : neighbor.g = tempG
                        else : 
                            neighbor.g = tempG
                            openSet.append(neighbor)
            
                        neighbor.h = heuristic(neighbor,end)
                        # neighbor.h = manhattenHeuristic(neighbor,end)
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.previous = current # assiging previous to track path later 
            
        else :   
            pass # No solution
    # Display Part 
    for i in range(rows) :
        for j in range(cols) :  
            grid[i][j].show("light blue") # All squares in grid are shown in this color
    path = []
    temp = current
    path.append(temp)
    while temp.previous != None : 
        path.append(temp.previous) # adding previous parent to the path array to generate path 
        temp = temp.previous
    for closed in closedSet : closed.show("red") # All squares in closedSet are in this color
    for opened in openSet : opened.show("green") # All in OpenSet are in this color
    for ele in path : 
        ele.show("blue")
    for event in pg.event.get() : 
        if event.type == pg.QUIT : 
            running = False 
        elif event.type == pg.KEYDOWN : 
            if event.key == pg.K_q : 
                running = False 
    pg.display.flip()
    clock.tick(50)
pg.quit()
