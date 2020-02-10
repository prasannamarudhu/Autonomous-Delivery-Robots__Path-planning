import pygame
#from PIL import Image, ImageDraw
import time
import numpy as np
import math
from scipy.stats import linregress
from scipy.spatial.distance import euclidean


class bfs:
    def __init__(self, area, poly, rect, cir,rect2, rect3, rect4,rect5, rect6,circ2,circ3, rect7):
        self.extreme_point = area
        self.poly = poly
        self.rect5 = rect5
        self.rect6 = rect6
        self.rect = rect
        self.rect2 = rect2
        self.rect3 = rect3
        self.rect4 = rect4
        self.rect7 = rect7

        self.cir = cir
        self.circ2 = circ2
        self.circ3 = circ3
        self.obs_array = []
        self.disp = pygame.display.set_mode(self.extreme_point)
        self.build_world()

    def getChild(self, c_point):
        returnList = []
        #print c_point
        if (c_point[1] - 1 >= 0):
            returnList.append((c_point[0], c_point[1] - 1))
        if (c_point[1] + 1 < 250):
            returnList.append((c_point[0], c_point[1] + 1))
        if (c_point[0] - 1 >= 0):
            returnList.append((c_point[0] - 1, c_point[1]))
        if (c_point[0] + 1) < 250:
            returnList.append((c_point[0]  + 1, c_point[1]))
        if (c_point[0] + 1 < 250) and (c_point[1] - 1 >= 0):
            returnList.append((c_point[0] + 1, c_point[1] - 1))
        if (c_point[0] + 1 < 250) and (c_point[1] + 1 < 250):
            returnList.append((c_point[0] + 1, c_point[1] + 1))
        if (c_point[0] - 1 >= 0) and (c_point[1] - 1 >= 0):
            returnList.append((c_point[0] - 1, c_point[1] - 1))
        if (c_point[0] - 1 >= 0) and (c_point[1] + 1 < 250):
            returnList.append((c_point[0] - 1, c_point[1] + 1))

        return returnList

    def ccw(self,A,B,C):
        #Checking the range
        return ((C[1]-A[1]) * (B[0]-A[0])) > ((B[1] - A[1]) * (C[0] - A[0]))

    def intersect(self, pos, line_segment):
        #This function checks if the Ray of the point is interecting the line segments of the polygons.
        #for estimating the optimal polygon points, need to check with more than one array which I haven't done.
        a = self.ccw(pos, self.extreme_point, line_segment[0]) != self.ccw(pos, self.extreme_point, line_segment[1]) and self.ccw(pos, line_segment[0], line_segment[1]) != self.ccw(self.extreme_point, line_segment[0], line_segment[1])
        if a == True:
            return 1
        if a == False:
            return 0


    def check_cir(self, pos):
        if math.sqrt((pos[0] - ((self.cir[0] + self.cir[2])/2))**2 + (pos[1] - ((self.cir[1] + self.cir[3])/2))**2) <= 32 :
            return True
        else:
            return False

    def check_circ2(self, pos):
        if math.sqrt((pos[0] - ((self.circ2[0] + self.circ2[2])/2))**2 + (pos[1] - ((self.circ2[1] + self.circ2[3])/2))**2) <= (28.5) :
            return True
        else:
            return False

    def check_circ3(self, pos):
        if math.sqrt((pos[0] - ((self.circ3[0] + self.circ3[2])/2))**2 + (pos[1] - ((self.circ3[1] + self.circ3[3])/2))**2) <= 20 :
            return True
        else:
            return False

    def check_rect7(self, pos):
        if (pos[0] >= self.rect7[0][0]) & (pos[0] <= self.rect7[1][0]) & (pos[1] >= self.rect7[0][1]) & (pos[1] <= self.rect7[1][1]) :
            return True
        else:
            return False


    def check_rect(self, pos):
        if (pos[0] >= self.rect[0][0]) & (pos[0] <= self.rect[1][0]) & (pos[1] >= self.rect[0][1]) & (pos[1] <= self.rect[1][1]) :
            return True
        else:
            return False

    def check_rect2(self, pos):
        if (pos[0] >= self.rect2[0][0]) & (pos[0] <= self.rect2[1][0]) & (pos[1] >= self.rect2[0][1]) & (pos[1] <= self.rect2[1][1]) :
            return True
        else:
            return False

    def check_rect3(self, pos):
        if (pos[0] >= self.rect3[0][0]) & (pos[0] <= self.rect3[1][0]) & (pos[1] >= self.rect3[0][1]) & (pos[1] <= self.rect3[1][1]) :
            return True
        else:
            return False

    def check_rect4(self, pos):
        if (pos[0] >= self.rect4[0][0]) & (pos[0] <= self.rect4[1][0]) & (pos[1] >= self.rect4[0][1]) & (pos[1] <= self.rect4[1][1]) :
            return True
        else:
            return False


    def check_poly(self, pos):
        #Plan is to check the intersection
        container_var = 0
        for x in range(len(poly)):
            container_var = container_var + self.intersect(pos, [poly[x-1], poly[x]])
            #print container_var
        if (container_var % 2) == 0:
            return False
        else:
            return True

    def check_rect5(self, pos):
        #Plan is to check the intersection
        container_var = 0
        for x in range(len(rect5)):
            container_var = container_var + self.intersect(pos, [rect5[x-1], rect5[x]])
            #print container_var
        if (container_var % 2) == 0:
            return False
        else:
            return True

    def check_rect6(self, pos):
        # Plan is to check the intersection
        container_var = 0
        for x in range(len(rect6)):
            container_var = container_var + self.intersect(pos, [rect6[x - 1], rect6[x]])
            # print container_var
        if (container_var % 2) == 0:
            return False
        else:
            return True

    def make_obs_hp(self, pos):
        #checking the point if it's in the obstacle
        if self.check_rect(pos) or self.check_cir(pos) or self.check_circ2(pos) or self.check_circ3(pos) or self.check_rect2(pos) or self.check_rect3(pos) or self.check_rect4(pos) or self.check_rect5(pos) or self.check_rect6(pos)  or self.check_rect7(pos):
            return True
        else:
            return False

    def build_world(self):
        #This is for the gui
        blank_world = np.zeros(self.extreme_point, dtype='int')
        for x in range(self.extreme_point[0]):
            for y in range(self.extreme_point[1]):
                if self.make_obs_hp((x,y)):
                    blank_world[x][y] = 1
                    pygame.draw.line(self.disp, (0, 0, 255), (x,y), (x,y))

        pygame.display.update()


    def start_bfs(self, pos, epos):
        start_time = time.time()
        self.sp = pos
        closed_point = []
        queue = []
        self.node_info = {}
        current_point = pos
        while(current_point != epos):
            childs = self.getChild(current_point)
            valid_child = [c for c in childs if hash(c) not in closed_point]
            valid_child = [c for c in valid_child if c not in queue]
            #print valid_child
            permited_child = []

            for obj in valid_child:
                temp = self.make_obs_hp(obj)
                #print temp
                if temp == False:
                    permited_child.append(obj)
            #print permited_child
            for obj in permited_child:
                pygame.draw.line(self.disp, (255, 255, 0), obj, obj)
                pygame.display.update()
                self.node_info[obj] = current_point

            #print permited_child

            queue.extend(permited_child)
            closed_point.append(hash(current_point))
            #print queue
            #print closed_point
            #print(closed_point)
            try:
                current_point = queue.pop(0)

                #print current_point
                #print len(closed_point)
                #aa = raw_input()
            except:
                break
        total_time = time.time() - start_time
        print ('This BFS took ' + str(total_time) + ' seconds')

        self.find_path(epos)

    x=0
    y=0

    def find_path(self, goal):
        gp = goal

        List_X = [goal[0]]
        List_Y = [goal[1]]
        while (gp != self.sp):

            List_X.append(gp[0])
            List_Y.append(gp[1])

            pygame.draw.line(self.disp, (255, 0, 0), gp, gp,2 )

            pygame.display.update()
            gp = self.node_info[gp]

        #print("gp_listx", List_X, "gp_listy", List_Y)
        Total_dist = path_length(List_X, List_Y)
        print('This BFS path length is ' + str(Total_dist) + ' meters')
        print (" ")
        Scaled = pygame.transform.scale(self.disp, (640,480))
        pygame.image.save(Scaled, "bfs.jpeg")

        aa = input('Path Found')
        exit()


def path_length(List_X, List_Y):
    length = 0
    for i in range(len(List_X) - 1):
        v = [List_X[i], List_Y[i]]
        w = [List_X[i + 1], List_Y[i + 1]]
        length += euclidean(v, w)
    return length


if __name__ == '__main__':
    #print ("Arena starts is of size (0-249)(0-149), so define the points accordingly.")
    print(" ")
    #start_point = tuple(map(int,input("Enter Starting point in the format: example - 'x,y' : ").split(',')))
    #goal_point = tuple(map(int,input("Enter goal point in the format: example - 'x,y' : ").split(',')))
    start_point =180,245-100  #-100+24
    goal_point = 130,-100+45  #250-100

    #goal_point = (250,149-149)
    start_point = (start_point[0], 149 - start_point[1])
    goal_point = (goal_point[0], 149 - goal_point[1])
    poly = [(120, 249 - 55), (158, 249 - 51), (165, 249 - 89), (188, 249 - 51), (168, 249 - 14), (145, 249 - 14)]
    circ = (10, 250 - 210 - 32, 10 + 64, 250 - 210 + 32)
    circ2 = (135, (250 - 40 - 28.5), 135 + 57, (250 - 40 + 28.5))
    circ3 = (10, (250 - 120 - 20), 10 + 40, (250 - 120 + 20))
    square = [( 10 , 250-12-53), (10 + 42 , 250-10)]
    rect2 = [( 69 ,250-12-50), (69+50 , 250-12)]
    rect3 = [( 69 ,250-80-80), (69+125 , 250-80)]
    rect4 = [( 120 ,250-210-30), (120+55 , 250-210)]
    rect5 = [(200, 250-210), (200, 250 - 240), (245, 250-240), (245, 250-120), (245-25, 250-120), (245-25, 250-210),(200, 250-210)]
    rect6 = [(245-40, 250-55), (245-(20), 250 - 95), (245, 250-55), (245-(20), 250 - 15)]
    rect7 = [( 25 , 250-100-40), (25 + 30 , 250-100)]


    area = (250,250)
    a = bfs(area, poly, square, circ, rect2,rect3, rect4, rect5, rect6,circ2,circ3,rect7)
    #Checking if the goal point is in the obstacle
    if a.make_obs_hp(start_point):
        print ("Start point is in the obtacle")
        exit()
    if a.make_obs_hp(goal_point):
        print ("Goal point is in the obtacle")
        exit()
    a.start_bfs(start_point, goal_point)
    print (goal_point)
    a.find_path(goal_point)
