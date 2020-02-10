from scipy.spatial.distance import euclidean
import math, sys, pygame, random
from math import *
from pygame import *
import time

class Node(object):
    def __init__(self, point, parent):
        super(Node, self).__init__()
        self.point = point
        self.parent = parent

XDIM = 250
YDIM = 250
windowSize = [XDIM, YDIM]
delta = 10.0
GAME_LEVEL = 1
GOAL_RADIUS = 2
MIN_DISTANCE_TO_ADD = 1
NUMNODES = 10000
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(windowSize)
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
blue = 0, 255, 0
green = 0, 0, 255
cyan = 0,180,105
#cyan =0, 0, 255

count = 0
rectObs = []
circObs =[]
rhombObs=[]

def dist(p1,p2):    #distance between two points
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def point_circle_collision(p1, p2, radius):
    distance = dist(p1,p2)
    if (distance <= radius):
        return True
    return False

def step_from_to(p1,p2):
    if dist(p1,p2) < delta:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + delta*cos(theta), p1[1] + delta*sin(theta)

def collides(p):    #check if point collides with the obstacle
    for rect in rectObs:
        if rect.collidepoint(p) == True:
            return True

    for rect in circObs:
        if rect.collidepoint(p)==True:
            return True

    for rect in rhombObs:
        if rect.collidepoint(p) == True:
            return True

    return False

def get_random_clear():
    while True:
        p = random.random()*XDIM, random.random()*YDIM
        noCollision = collides(p)
        if noCollision == False:
            return p


def init_obstacles(configNum):  #initialized the obstacle
    global rectObs
    rectObs = []
    #print("config "+ str(configNum))
    if (configNum == 0):
        rectObs.append(pygame.Rect((XDIM / 2.0 - 50, YDIM / 2.0 - 100),(100,200)))
    if (configNum == 1):
        rectObs.append(pygame.Rect((10,190),(48,50)))
        rectObs.append(pygame.Rect((80, 188), (50, 53)))
        rectObs.append(pygame.Rect((80,250-160),(105,70)))
        rectObs.append(pygame.Rect((110,10),(60,30)))
        rectObs.append(pygame.Rect((200, 10), (45, 30)))
        rectObs.append(pygame.Rect((225, 10), (20, 115)))
        rectObs.append(pygame.Rect((25, 250-145), (30, 40)))

        #circle obstacles
        circObs_c = pygame.draw.circle(screen, green, (165, 215), 25)
        circObs.append(circObs_c)
        circObs_c2 = pygame.draw.circle(screen, green, (40, 40), 32)
        circObs.append(circObs_c2)
        circObs_c3 = pygame.draw.circle(screen, green, (25, 125), 20)
        circObs.append(circObs_c3)

        #rhombus obstacle
        rhomb = pygame.draw.polygon(screen, green, [(215,200),(230, 170),(245,200),(230, 230)])
        rhombObs.append(rhomb)

    if (configNum == 2):
        rectObs.append(pygame.Rect((100,50),(200,150)))
    if (configNum == 3):
        rectObs.append(pygame.Rect((100,50),(200,150)))

    for rect in rectObs:
        pygame.draw.rect(screen, green, rect)


def path_length(List_X, List_Y):
    length = 0
    for i in range(len(List_X) - 1):
        v = [List_X[i], List_Y[i]]
        w = [List_X[i + 1], List_Y[i + 1]]
        length += euclidean(v, w)
    return length


def reset():
    global count
    screen.fill(white)
    init_obstacles(GAME_LEVEL)
    count = 0

def main():
    global count
    start = time.time()
    initPoseSet = False
    initialPoint = Node(None, None)
    goalPoseSet = False
    goalPoint = Node(None, None)
    currentState = 'init'

    nodes = []
    reset()

    while True:
        if currentState == 'init':
            #print('goal point not yet set')
            pygame.display.set_caption('Select Starting Point and then Goal Point')
            fpsClock.tick(10)
        elif currentState == 'goalFound':
            currNode = goalNode.parent
            pygame.display.set_caption('Goal Reached')

            List_X = [currNode.parent.point[0]]
            List_Y = [currNode.parent.point[1]]

            EndTime = time.time()
            print (" ")
            print ('This RRT_Algorithm took ' + str(EndTime-start) + ' seconds')


            while currNode.parent != None:
                #print ("currNode.parent.x",currNode.parent.x)
                #print("currNode.0x", currNode[0])
                #print("currpoint",currNode.point[0])
                List_X.append([currNode.parent.point[0]])
                List_Y.append([currNode.parent.point[1]])


                pygame.draw.line(screen,red,currNode.point,currNode.parent.point)
                currNode = currNode.parent
            optimizePhase = True

            Total_dist = path_length(List_X, List_Y)
            print('This RRT path length is ' + str(Total_dist) + ' meters')
            #Scaled = pygame.transform.scale(screen, (640, 480))
            #pygame.image.save(screen, "bfs.jpeg")



        elif currentState == 'optimize':
            fpsClock.tick(0.5)
            pass
        elif currentState == 'buildTree':
            count = count+1
            pygame.display.set_caption('Performing RRT')
            if count < NUMNODES:
                foundNext = False
                while foundNext == False:
                    rand = get_random_clear()
                    parentNode = nodes[0]
                    for p in nodes:
                        if dist(p.point,rand) <= dist(parentNode.point,rand):
                            newPoint = step_from_to(p.point,rand)
                            if collides(newPoint) == False:
                                parentNode = p
                                foundNext = True

                newnode = step_from_to(parentNode.point,rand)
                nodes.append(Node(newnode, parentNode))
                pygame.draw.line(screen,cyan,parentNode.point,newnode)

                if point_circle_collision(newnode, goalPoint.point, GOAL_RADIUS):
                    currentState = 'goalFound'

                    goalNode = nodes[len(nodes)-1]


            else:
                print("Ran out of nodes... :(")
                return;

        #handle events



        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Exiting")
            if e.type == MOUSEBUTTONDOWN:
                #print('mouse down')
                if currentState == 'init':
                    if initPoseSet == False:
                        nodes = []
                        if collides(e.pos) == False:
                            #print('initiale point set: '+str(e.pos))

                            initialPoint = Node((180,250-245), None)
                            nodes.append(initialPoint) # Start in the center
                            initPoseSet = True
                            pygame.draw.circle(screen, red, initialPoint.point, GOAL_RADIUS)
                    elif goalPoseSet == False:
                        #print('goal point set: '+str(e.pos))
                        if collides(e.pos) == False:
                            goalPoint = Node((130,250-45),None)
                            goalPoseSet = True
                            pygame.draw.circle(screen, green, goalPoint.point, GOAL_RADIUS)
                            currentState = 'buildTree'
                else:
                    currentState = 'init'
                    initPoseSet = False
                    goalPoseSet = False
                    reset()

        pygame.display.update()
        fpsClock.tick(10000)



if __name__ == '__main__':
    main()
    







