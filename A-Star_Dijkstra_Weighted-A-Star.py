import numpy as np
import matplotlib.pyplot as plt
import math
import time
import pickle
from scipy.spatial.distance import euclidean

class Planning:

    def __init__(self, x, y, cost, ID, Parent, Hdist):
        self.x = x
        self.y = y
        self.cost = cost
        self.ID = ID
        self.Parent = Parent
        self.Hdist = Hdist

def draw(O_Points):

    Workspace = plt.Rectangle((0,0), 250,250, color='w')
    plt.gca().add_patch(Workspace)

    x, y = zip(*O_Points)
    plt.plot(x, y, 'b.')
    # for i in O_Points:
    #   plt.plot(i[0],i[1],'b.')


    return O_Points


def unique_index(x, y):
    Index = x + y * 250  # Provides a unique identity to the point set , which saves the time and computation during verification.

    return Index


def Calculate_Path(explored_set, Final_Points):
    List_X = [Final_Points.x]
    List_Y = [Final_Points.y]
    ParentID = Final_Points.Parent

    while ParentID != -1:
        Node = explored_set[ParentID]
        List_X.append(Node.x)
        List_Y.append(Node.y)
        ParentID = Node.Parent

    return List_X, List_Y


def Generate_neighbors(Current_N, O_Points, ):
    X = Current_N.x
    Y = Current_N.y
    cost = Current_N.cost
    Moving_Action = [(1, 0, 1), (0, 1, 1), (-1, 0, 1), (0, -1, 1), (-1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)),
                     (1, -1, math.sqrt(2)), (1, 1, math.sqrt(2))]

    Neighbor_Values = []

    for i in range(0, 8):

        Move_X = X + Moving_Action[i][0]
        Move_Y = Y + Moving_Action[i][1]
        Move_Cost = cost + Moving_Action[i][2]
        Coordinates = (Move_X, Move_Y)

        if Move_X in range(0, round(251)) and Move_Y in range(0, round(251)):

            if Coordinates not in O_Points:
                UID = unique_index(Move_X, Move_Y)
                Neighbor_Node = Planning(Move_X, Move_Y, Move_Cost, UID, Current_N.ID, 0)
                Neighbor_Values.append(Neighbor_Node)

    return Neighbor_Values


def dijksta_algo(StartPoints, GoalPoints,O_Points):

    start_time = time.time()

    plt.plot(StartPoints[0], StartPoints[1], 'rx')
    plt.plot(GoalPoints[0], GoalPoints[1], 'rx')
    O_Points = draw(O_Points)

    if StartPoints in O_Points or StartPoints[0] > 250  or StartPoints[1] > 250  or GoalPoints in O_Points or GoalPoints[0] > 250  or GoalPoints[1] > 250 :
        print('The Points are either in the Obstacle Space or out of the Workspace.Exiting.')
        exit(0)

    explored_set = dict()
    future_set = dict()
    show_animation = list()

    Source_Points = Planning(StartPoints[0], StartPoints[1], 0, 0, -1, 0)
    Final_Points = Planning(GoalPoints[0], GoalPoints[1], 0, 0, 0, 0)

    Source_Points.ID = unique_index(Source_Points.x, Source_Points.y)
    future_set[Source_Points.ID] = Source_Points

    while len(future_set) != 0:

        ID_Current = min(future_set, key=lambda i: future_set[i].cost)
        Current_N = future_set[ID_Current]

        show_animation.append((Current_N.x, Current_N.y))
        x, y = zip(*show_animation)

        del future_set[ID_Current]
        explored_set[ID_Current] = Current_N

        if Current_N.x == Final_Points.x and Current_N.y == Final_Points.y:
            Final_Points.Parent = Current_N.Parent
            Final_Points.cost = Current_N.cost
            plt.plot(x, y, 'y.')
            break

        if len(show_animation) % (1000) == 0:
            plt.plot(x, y, 'y.')
            plt.pause(0.0001)
            show_animation.clear()

        Neighbors = Generate_neighbors(Current_N, O_Points, )

        for Neighbor in Neighbors:
            if Neighbor.ID in explored_set:
                continue

            if Neighbor.ID in future_set:
                if future_set[Neighbor.ID].cost > Neighbor.cost:
                    future_set[Neighbor.ID].cost = Neighbor.cost
                    future_set[Neighbor.ID].Parent = ID_Current


            else:
                future_set[Neighbor.ID] = Neighbor

    List_X, List_Y = Calculate_Path(explored_set, Final_Points)
    for i in range(len(List_X)):
        plt.plot(List_X[i], List_Y[i], 'r.')
    print('time ------>', time.time() - start_time)
    print('Path Length ------>', path_length(List_X, List_Y))
    #plt.show()


def distance_heuristic(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


def Generate_neighbors_A(Current_N, Goal_N, O_Points,w ):
    X = Current_N.x
    Y = Current_N.y
    Goal_X = Goal_N.x
    Goal_Y = Goal_N.y
    cost = Current_N.cost
    Moving_Action = [(1, 0, 1), (0, 1, 1), (-1, 0, 1), (0, -1, 1), (-1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)),
                     (1, -1, math.sqrt(2)), (1, 1, math.sqrt(2))]

    Neighbor_Values = []

    for i in range(0, 8):

        Move_X = X + Moving_Action[i][0]
        Move_Y = Y + Moving_Action[i][1]
        Move_Cost = cost + Moving_Action[i][2]
        Hdist = Move_Cost + w*distance_heuristic(Move_X, Move_Y, Goal_X, Goal_Y)
        Coordinates = (Move_X, Move_Y)
        if Move_X in range(0, round(251)) and Move_Y in range(0, round(251)):

            if Coordinates not in O_Points:
                UID = unique_index(Move_X, Move_Y)
                Neighbor_Node = Planning(Move_X, Move_Y, Move_Cost, UID, Current_N.ID, Hdist)
                Neighbor_Values.append(Neighbor_Node)

    return Neighbor_Values


def Astar_algo(StartPoints, GoalPoints,O_Points,w):

    plt.plot(StartPoints[0],StartPoints[1],'rx')
    plt.plot(GoalPoints[0],GoalPoints[1],'rx')
    O_Points = draw(O_Points)
    start_time = time.time()
    if StartPoints in O_Points or StartPoints[0] > 250  or StartPoints[1] > 250  or GoalPoints in O_Points or            GoalPoints[0] > 250  or GoalPoints[1] > 250 :
        print('The Points are either in the Obstacle Space or out of the Workspace.Exiting.')
        exit(0)

    explored_set = dict()
    future_set = dict()
    show_animation = list()

    Hdist_source = distance_heuristic(StartPoints[0], StartPoints[1], GoalPoints[0], GoalPoints[1])
    Source_Points = Planning(StartPoints[0], StartPoints[1], 0, 0, -1, Hdist_source)
    Final_Points = Planning(GoalPoints[0], GoalPoints[1], 0, 0, 0, 0)

    Source_Points.ID = unique_index(Source_Points.x, Source_Points.y)
    future_set[Source_Points.ID] = Source_Points

    while len(future_set) != 0:

        ID_Current = min(future_set, key=lambda i: future_set[i].Hdist)
        Current_N = future_set[ID_Current]

        show_animation.append((Current_N.x, Current_N.y))
        x, y = zip(*show_animation)

        if Current_N.x == Final_Points.x and Current_N.y == Final_Points.y:
            Final_Points.Parent = Current_N.Parent
            Final_Points.cost = Current_N.cost
            plt.plot(x, y, 'y.')
            break

        if len(show_animation) % (1000) == 0:
            plt.plot(x, y, 'y.')
            plt.pause(0.0001)
            show_animation.clear()

        del future_set[ID_Current]
        explored_set[ID_Current] = Current_N

        Neighbors = Generate_neighbors_A(Current_N, Final_Points, O_Points,w)

        for Neighbor in Neighbors:

            if Neighbor.ID in explored_set:
                continue

            if Neighbor.ID in future_set:
                if future_set[Neighbor.ID].cost > Neighbor.cost:
                    future_set[Neighbor.ID].cost = Neighbor.cost
                    future_set[Neighbor.ID].Hdist = Neighbor.Hdist
                    future_set[Neighbor.ID].Parent = ID_Current

            else:
                future_set[Neighbor.ID] = Neighbor

    List_X, List_Y = Calculate_Path(explored_set, Final_Points)

    for i in range(len(List_X)):
        plt.plot(List_X[i], List_Y[i], 'r.')


    print('time ------>', time.time() - start_time)
    print('Path Length ------>' , path_length(List_X,List_Y))
    #plt.show()

def path_length(ListX,ListY):
    length = 0
    for i in range(len(ListX) - 1):
        v = [ListX[i], ListY[i]]
        w = [ListX[i+1], ListY[i+1]]
        length += euclidean(v, w)
    return length


def main():
    with open('Obstacle_Points.txt', 'rb') as fp:
        O_Points = pickle.load(fp)

    print("Enter the start point x-coordinate")
    X_start = int(input())
    print("Enter the start point y-coordinate")
    Y_start = int(input())
    print("Enter the goal point x-coordinate")
    X_goal = int(input())
    print("Enter the goal point y-coordinate")
    Y_goal = int(input())

    print("Select your choice of Path Planning Algorithm.")
    print("Press 1 for Dijkstra Algorithm")
    print("Press 2 for A-Star Algorithm")
    print("Press 3 for Weighted A-Star Algorithm")
    S = int(input("Make you selection:"))



    if S == 1:

        Validity = dijksta_algo((X_start, Y_start), (X_goal, Y_goal),O_Points)
        if Validity == "The Points are either in the Obstacle Space or out of the Workspace.Exiting.":
            print(Validity)
            exit(0)

    elif S == 2:

        Validity = Astar_algo((X_start, Y_start), (X_goal, Y_goal),O_Points,w=1)
        if Validity == "The Points are either in the Obstacle Space or out of the Workspace.Exiting.":
            print(Validity)
            exit(0)

    elif S == 3:

        Validity = Astar_algo((X_start, Y_start), (X_goal, Y_goal),O_Points,w=4)
        if Validity == "The Points are either in the Obstacle Space or out of the Workspace.Exiting.":
            print(Validity)
            exit(0)

    else:
        print("Option Not Valid. Exiting Code.")
        exit(0)

if __name__ == '__main__':

    main()
