import pyvisgraph as vg
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
import time
import pickle


def path_length(path):
    length = 0
    for i in range(len(path) - 1):
        v = [path[i].x, path[i].y]
        w = [path[i + 1].x, path[i + 1].y]
        length += euclidean(v, w)
    return length


def plot_polygon(vertices):
    last_i = len(vertices) - 1
    for i in range(len(vertices)):
        v = vertices[i]
        if i == last_i:
            w = vertices[0]
        else:
            w = vertices[i + 1]
        plt.plot([v.x, w.x], [v.y, w.y], 'r-')


def plot_edge(edge):
    v = edge.p1
    w = edge.p2
    plt.plot([v.x, w.x], [v.y, w.y], 'b--')

def plot_path(path):
    for i in range(len(path) - 1):
        v = path[i]
        w = path[i + 1]
        plt.plot([v.x, w.x], [v.y, w.y], 'g-', linewidth=4.0)


polys = [[vg.Point(69.0,88.0), vg.Point(69.0,165.0),vg.Point(182.0,165.0), vg.Point(182.0,88.0)],
         [vg.Point(185.0, 217.0), vg.Point(185.0, 254.0), vg.Point(244.0, 254.0), vg.Point(244.0, 140.0),vg.Point(213, 140), vg.Point(213, 217)],
         [vg.Point(7.0,13.0), vg.Point(7.0,70.0),vg.Point(44.0,70.0), vg.Point(44.0,13.0)],
         [vg.Point(69.0,13.0), vg.Point(69.0,70.0),vg.Point(113.0,70.0), vg.Point(113.0,13.0)],
         [vg.Point(101.0,217.0), vg.Point(101.0,254.0),vg.Point(160.0,254.0), vg.Point(160.0,217.0)],
         [vg.Point(26.0,100.0),vg.Point(20.0,100.0),vg.Point(17.0,102.0),vg.Point(15.0,103.0),
          vg.Point(7.0,111.0),vg.Point(6.0,113.0),vg.Point(5.0,116.0),vg.Point(4.0,122.0)
          ,vg.Point(5.0,128.0),vg.Point(6.0,131.0),vg.Point(7.0,133.0),vg.Point(10.0,137.0)
          ,vg.Point(11.0,138.0),vg.Point(15.0,141.0),vg.Point(17.0,142.0)
          , vg.Point(26.0,144.0),vg.Point(56.0,144.0), vg.Point(56.0,100.0)],
         [vg.Point(230.0, 88.0), vg.Point(242.0, 56.0), vg.Point(230.0, 24.0), vg.Point(218.0, 56.0)],
         [vg.Point(27, 185),vg.Point(23, 186),vg.Point(21, 187),vg.Point(19, 188),vg.Point(17, 189),vg.Point(13, 192),vg.Point(10, 195),vg.Point(7, 199),vg.Point(6, 201),vg.Point(5, 203)
          ,vg.Point(4, 205),vg.Point(3, 209),vg.Point(2, 216),vg.Point(3, 223),vg.Point(4, 227),vg.Point(5, 229)
          ,vg.Point(6, 231),vg.Point(7, 233),vg.Point(10, 237),vg.Point(11, 238),vg.Point(12, 239)
          ,vg.Point(13, 240),vg.Point(17, 243),vg.Point(19, 244),vg.Point(21, 245),vg.Point(23, 246)
          ,vg.Point(27, 247),vg.Point(34, 248),vg.Point(41, 247),vg.Point(45, 246),vg.Point(47, 245)
          ,vg.Point(49, 244),vg.Point(51, 243),vg.Point(56, 239),vg.Point(57, 238),vg.Point(58, 237)
          ,vg.Point(61, 233),vg.Point(62, 231),vg.Point(63, 229),vg.Point(64, 227),vg.Point(65, 223)
          ,vg.Point(66, 216),vg.Point(65, 209),vg.Point(64, 205),vg.Point(63, 203),vg.Point(62, 201)
          ,vg.Point(61, 199),vg.Point(58, 195),vg.Point(57, 194),vg.Point(56, 193),vg.Point(55, 192)
          ,vg.Point(51, 189),vg.Point(49,188),vg.Point(47,187),vg.Point(45,186),vg.Point(41, 185)
          ,vg.Point(34, 184)],
         [vg.Point(146, 17),vg.Point(144, 18),vg.Point(143, 19),vg.Point(137, 25),vg.Point(135, 28),
          vg.Point(134, 30),vg.Point(133, 33),vg.Point(132, 37),vg.Point(132, 38),vg.Point(132, 45),
          vg.Point(132, 46),vg.Point(133, 50),vg.Point(134, 53),vg.Point(135, 55),vg.Point(143, 64),
          vg.Point(144, 65),vg.Point(146, 66),vg.Point(150,68),vg.Point(153,69),vg.Point(160, 70),
          vg.Point(167, 69),vg.Point(170, 68),vg.Point(174, 66),vg.Point(176, 65),vg.Point(177, 64),vg.Point(183, 58),
          vg.Point(185, 55),vg.Point(186, 53),vg.Point(187, 50),vg.Point(188, 46),vg.Point(188, 45),
          vg.Point(188, 38),vg.Point(188, 37),vg.Point(187, 33),vg.Point(186, 30),vg.Point(185, 28),
          vg.Point(183, 25),vg.Point(177, 19),vg.Point(176, 18),vg.Point(174, 17),vg.Point(170, 15),
          vg.Point(167, 14),vg.Point(160, 13),vg.Point(153 ,14)]
         ]

#polys = vg.Point(float(x[0,0]),float(y[0,0]))
g = vg.VisGraph()
g.build(polys)
start_time = time.time()
shortest = g.shortest_path(vg.Point(180,245), vg.Point(130,45))
plot_path(shortest)

for p in polys:
    plot_polygon(p)

for e in g.visgraph.get_edges():
   plot_edge(e)


print('The time taken --->',time.time() - start_time)


length = "{}".format(path_length(shortest))
print ("The length of the shortest path is", length)


plt.show()