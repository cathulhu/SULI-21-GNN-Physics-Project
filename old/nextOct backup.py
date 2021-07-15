import math
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from random import seed
from random import randint





#helpful attribute classes

class Dimensions_Tree:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Dimensions_Node:

    def __init__(self, passed_coordinate_range):
        
        self.x = (passed_coordinate_range.x_range[1] - passed_coordinate_range.x_range[0])+1
        self.y = (passed_coordinate_range.y_range[1] - passed_coordinate_range.y_range[0])+1
        self.z = (passed_coordinate_range.z_range[1] - passed_coordinate_range.z_range[0])+1


class Coordinate_Range:

    # format ([x_min,x_max]),[y_min,y_max],[z_min,z_max])
    def __init__(self, x_arr, y_arr, z_arr):
        self.x_range = x_arr
        self.y_range = y_arr
        self.z_range = z_arr


class Position:

    def __init__(self,i_coord,j_coord,k_coord):
        self.i=i_coord
        self.j=j_coord
        self.k=k_coord





def subdivide_range(range):
    midpoint = math.floor((range[1] - range[0]) / 2) + range[0]

    return [
        [range[0], midpoint],
        [midpoint + 1, range[1]]
    ]


def check_for_undivisible_dimensions(passed_node):
    # if a dimension = 4 it can still be split up, 3 splits into 2/1, thus we lock at 1.
    if passed_node.node_dimensions.x==1 or passed_node.node_dimensions.y==1 or passed_node.node_dimensions.z==1:
        passed_node.dont_split=True
        # print(f"undivisible @{passed_node.id}")


class Child_Octant_Range:

    def __init__(self, passedNode):

        #length
        x_ranges = subdivide_range(passedNode.node_coordinate_ranges.x_range)
        self.x_first = x_ranges[0]
        self.x_second = x_ranges[1]
        #width
        y_ranges = subdivide_range(passedNode.node_coordinate_ranges.y_range)
        self.y_first = y_ranges[0]
        self.y_second = y_ranges[1]
        #height
        z_ranges = subdivide_range(passedNode.node_coordinate_ranges.z_range)
        self.z_first = z_ranges[0]
        self.z_second = z_ranges[1]

        if passedNode.dont_split:
            print("\t\t\t\t         No further segmentation possible!")
        else:
            print(f"\t    Node {passedNode.id} partition segements: X:{self.x_first, self.x_second}\n\t\t\t\t         Y:{self.y_first, self.y_second}\n\t\t\t\t         Z:{self.z_first, self.z_second}\n")



def check_if_in_range(passed_particle, passed_node):
    if passed_particle.coordinates.i >= passed_node.node_coordinate_ranges.x_range[0] and passed_particle.coordinates.i <= passed_node.node_coordinate_ranges.x_range[1]:
        # print("x ok")
        if passed_particle.coordinates.j >= passed_node.node_coordinate_ranges.y_range[0] and passed_particle.coordinates.j <= passed_node.node_coordinate_ranges.y_range[1]:
            # print("y ok")
            if passed_particle.coordinates.k >= passed_node.node_coordinate_ranges.z_range[0] and passed_particle.coordinates.k <= passed_node.node_coordinate_ranges.z_range[1]:
                # print("z ok")
                # print("Particle fits in range, recursing...")
                return True

    return False


#returns the node that the passed particle belongs in
def find_node(passed_tree, passed_particle):

    abort_flag = False

    if check_if_in_range(passed_particle, passed_tree.root):
        print(f"Particle belongs in Node {passed_tree.root.id}")
        return passed_tree.root
    else:
        for x in passed_tree.root.children:
            while not abort_flag:
                if check_if_in_range(passed_particle, x):
                    abort_flag= True
                    print(f"Particle belongs in Node {x.id}")
                    return x


def insert_particle(passed_node, passed_particle):

        if check_if_in_range( passed_particle ,passed_node ):
            if passed_node.children:
                for x in passed_node.children:
                    if check_if_in_range(passed_particle, x):
                        insert_particle(x, passed_particle)
            else:

                if passed_node.particle_count < passed_node.owner_tree.split_threshold:
                    #case where particle is in range and there are no children means ready to insert OR need to partition if node is already at limit, then insert
                    passed_particle.node_occupancy = passed_node.id
                    passed_node.particles.append(passed_particle)
                    passed_node.particle_count+=1
                    passed_node.owner_tree.total_particle_count+=1
                    print(f"Particle added to Node {passed_node.id}\n")
                else:
                    passed_node.partition()

                    # this part distributes existing particles from a higher level to lower ones
                    for y in passed_node.particles:
                        insert_particle(passed_node, y)
                        passed_node.particles.remove(y)

                    # finally insert the new particle we tried to add first off
                    insert_particle(passed_node, passed_particle)
        else:
            print("particle not in range")


    # TODO REALLLLYYY IMMPORTANT!!!! after partition the particles of that node need to be redistributed to its children



def get_all_particles_below(passed_node, passed_list):

    #get all the particles in this top level node
    for x in passed_node.particles:
        passed_list.append(x)
        #print(f"Particle @{x.coordinates.i,x.coordinates.j,x.coordinates.k}, Node {x.node_occupancy}")

    for x in passed_node.children:
        get_all_particles_below(x, passed_list)


def get_all_nodes_below(passed_node, passed_list):
    
    for x in passed_node.children:
        get_all_nodes_below(x, passed_list)

    passed_list.append(passed_node)






















#component classes

class Particle:

    def __init__(self,x_coord,y_coord,z_coord):
        self.coordinates=Position(x_coord,y_coord,z_coord)
        self.node_occupancy=None

    # def set_momentum (self,i,j,k):
    #     self.momentum_vector=Momentum(i,j,k)

    def set_position(self,x_coord,y_coord,z_coord):
        self.coordinates=Position(x_coord,y_coord,z_coord)




class Tree:

    root = None                 # pointer to root node
    octant_count = 0
    total_particle_count = 0
    tree_dimensions = None      # for top level first digits should be 0, ex: [0,5],[0,9],[0,12]
    split_threshold=100           # if more than X number of particles in a cell, split into octants
    layer_count=0


    def __init__(self, length, width, height):      #supply the total dimensions of the oct-tree upon instantiation
        if length > 1 and width >1 and height >1:
            if isinstance(length, int) and isinstance(width, int) and isinstance(height, int):
                self.totalDimensions = Dimensions_Tree(length, width, height)

                print(f"\nCreated tree with dimensions: {self.totalDimensions.x} {self.totalDimensions.y} {self.totalDimensions.z}")
                print("\n")
                #spawning first node into tree and passing it the coordinate range that will be its domain (the whole thing) until it inevitably gets split up
                self.root = Node([0,self.totalDimensions.x-1], [0,self.totalDimensions.y-1], [0,self.totalDimensions.z-1], self)
            else:
                print("Failed to create Oct-Tree! Dimensions must be integer!")
        else:
            print("Failed to create Oct-tree! Tree must have minimum of 2 units of dimension in each axis.")
            



    def add_particle(self, passed_particle):
        print(f"\nTrying to add Particle {self.total_particle_count} at: ({passed_particle.coordinates.i},{passed_particle.coordinates.j},{passed_particle.coordinates.k})")
        
        #check that the particle is within total bounds
        if passed_particle.coordinates.i < self.totalDimensions.x and passed_particle.coordinates.j < self.totalDimensions.y and passed_particle.coordinates.k < self.totalDimensions.z:
            #check that particle coordinates are integers
            if isinstance(passed_particle.coordinates.i, int) and isinstance(passed_particle.coordinates.j, int) and isinstance(passed_particle.coordinates.k, int):

                #if here then particle fits in the overall shape, now find which octant to put it in...
                insert_particle(self.root, passed_particle)

            else:
                print("failed to add particle, coordinates must be integer!")
        else:
            print(f"Failed to add particle, location outside bounds of shape.")
















class Node:
    owner_tree=None    # each node will have the same link to the parent tree for incrementing particle count

    def __init__(self, passed_length_range, passed_width_range, passed_height_range,passed_tree):
        # print(f" Creating new node over coord range: {passed_length_range, passed_width_range, passed_height_range}")

        self.node_dimensions = None         # description of size of volume within larger shape this section encompasses
        self.node_coordinate_ranges = None  # tells us where in the overall shape is this volume located
        self.octant_range_divisions=None    # what divisions will this octant be split up along if it gets partitioned?
        self.parent_node=None               # link to the node above this one
        self.particle_count=0               # when this goes over (tree.split_threshold) we split the node into 8 more parts
        self.neighbors=[]                   # list of pointers to the other nodes in its level, will be empty for the top one, of course
        self.children=[]                    # pointer to descendant octants
        self.particles=[]                   # list of particles in this node, upon partition these get redistributed
        self.owner_tree=passed_tree         # pointer to the tree this node belongs to, useful for recursion starting point
        self.id=self.owner_tree.octant_count    # each node has ID number, tree keeps track of them
        self.owner_tree.octant_count+=1
        self.allow_particle_overloading = True  # if true when node reaches split count and maximum depth extra particles will just keep getting added.

        self.dont_split=False               # No node can be smaller than 1 units in any dimension, so block subdivizion at a certain point

        self.node_coordinate_ranges=Coordinate_Range(passed_length_range, passed_width_range, passed_height_range)
        self.node_dimensions=Dimensions_Node(self.node_coordinate_ranges)

        print(f"\n\t    Node {self.id} has dimensions of:   {self.node_dimensions.x}, {self.node_dimensions.y}, {self.node_dimensions.z}")
        print(f"\t    Node {self.id} coordinate range:    ", end ='')
        print(f"X:{self.node_coordinate_ranges.x_range}, Y:{self.node_coordinate_ranges.y_range}, Z:{self.node_coordinate_ranges.z_range}")

        check_for_undivisible_dimensions(self)
        self.octant_range_divisions = Child_Octant_Range(self)
        self.layerID=self.owner_tree.layer_count





    def partition(self):
        # spawned_node = Node(self.node_dimensions.x/8, self.node_dimensions.y/8, self.node_dimensions.z/8, self.owner_tree)
        # print(f"spawning with: {[self.octant_range_divisions.x_first[0],self.octant_range_divisions.x_first[1]+1], self.octant_range_divisions.y_first, self.octant_range_divisions.z_first, self.owner_tree}\n")
        
        if self.dont_split:
            print(f"\nNode {self.id} full, can't divide because maximum depth reached.")
            if self.allow_particle_overloading:
                print("Octant overloading enabled\n")
        else:

            print(f"\n\t____________Node {self.id}_New Level______________")

            spawned_node0 = Node(self.octant_range_divisions.x_first, self.octant_range_divisions.y_first, self.octant_range_divisions.z_first, self.owner_tree)
            spawned_node1 = Node(self.octant_range_divisions.x_first, self.octant_range_divisions.y_first, self.octant_range_divisions.z_second, self.owner_tree)

            spawned_node2 = Node(self.octant_range_divisions.x_first, self.octant_range_divisions.y_second, self.octant_range_divisions.z_first, self.owner_tree)
            spawned_node3 = Node(self.octant_range_divisions.x_first, self.octant_range_divisions.y_second, self.octant_range_divisions.z_second, self.owner_tree)

            # print("fourth node spawned: x_first, y_first, z_second")
            # print(self.octant_range_divisions.x_first, self.octant_range_divisions.y_second, self.octant_range_divisions.z_first)
            
            spawned_node4 = Node(self.octant_range_divisions.x_second, self.octant_range_divisions.y_first, self.octant_range_divisions.z_first, self.owner_tree)
            spawned_node5 = Node(self.octant_range_divisions.x_second, self.octant_range_divisions.y_first, self.octant_range_divisions.z_second, self.owner_tree)

            spawned_node6 = Node(self.octant_range_divisions.x_second, self.octant_range_divisions.y_second, self.octant_range_divisions.z_first, self.owner_tree)
            spawned_node7 = Node(self.octant_range_divisions.x_second, self.octant_range_divisions.y_second, self.octant_range_divisions.z_second, self.owner_tree)

            #print(self.octant_range_divisions.x_second, self.octant_range_divisions.y_second, self.octant_range_divisions.z_second)
            


            self.children.append(spawned_node0)
            self.children.append(spawned_node1)
            self.children.append(spawned_node2)
            self.children.append(spawned_node3)
            self.children.append(spawned_node4)
            self.children.append(spawned_node5)
            self.children.append(spawned_node6)
            self.children.append(spawned_node7)

            self.owner_tree.layer_count+=1

            #give each node a link to its parent
            for x in self.children:
                x.parent_node=self
                x.layerID=self.owner_tree.layer_count

            print("\n")













# testTree = Tree(17,16,5)
testTree = Tree(4,4,4)
# smallTree = Tree(2,2,2)
# testTree = Tree(64,64,512)
testTree = Tree(300,300,300)

# testTree.root.partition()
# testTree.root.children[2].partition()
#testTree.root.children[0].children[0].partition()
# testTree.root.children[7].children[0].partition()


# seed(1)
for x in range(0,1000):
    testTree.add_particle(Particle(randint(0,300), randint(0,300), randint(0,300)))

# testparticle0=Particle(0,0,0)
# testparticle1=Particle(0,3,1)
# testparticle2=Particle(1,2,0)
# testparticle3=Particle(0,1,2)

# testTree.add_particle(testparticle0)
# testTree.add_particle(testparticle1)
# testTree.add_particle(testparticle2)
# testTree.add_particle(testparticle3)



























def plot_linear_cube(ax, X, Y, Z, color):
    [x_start, x_end] = X
    [y_start, y_end] = Y
    [z_start, z_end] = Z

    x_end+=1
    y_end+=1
    z_end+=1

    xx = [x_start, x_start, x_end, x_end, x_start]
    yy = [y_start, y_end, y_end, y_start, y_start]
    kwargs = {'alpha': 1, 'color': color}
    ax.plot3D(xx, yy, [z_start]*5, **kwargs)
    ax.plot3D(xx, yy, [z_end]*5, **kwargs)
    ax.plot3D([x_start, x_start], [y_start, y_start], [z_start, z_end], **kwargs)
    ax.plot3D([x_start, x_start], [y_end, y_end], [z_start, z_end], **kwargs)
    ax.plot3D([x_end, x_end], [y_end, y_end], [z_start, z_end], **kwargs)
    ax.plot3D([x_end, x_end], [y_start, y_start], [z_start, z_end], **kwargs)

def plot_scatter_points(ax, points, color='purple'):
    kwargs = {'alpha': 1, 'color': color}
    ax.scatter3D([x[0] for x in points], [y[1] for y in points], [z[2] for z in points], **kwargs)

    







def plot_tree():

    print("Rendering Tree...")

    list = []
    get_all_particles_below(testTree.root, list)

    nodelist = []
    get_all_nodes_below(testTree.root, nodelist)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #TODO instead of printing each node, count the nodes per cube and just increase the size of the node in the figure corresponding to the count

    for x in nodelist:
        #print(x.node_coordinate_ranges.x_range, x.node_coordinate_ranges.y_range, x.node_coordinate_ranges.z_range)
        color="C" + str(x.layerID)
        plot_linear_cube(ax, x.node_coordinate_ranges.x_range, x.node_coordinate_ranges.y_range, x.node_coordinate_ranges.z_range, color)

    coordinateList = []

    for x in list:
        coordinateList.append((x.coordinates.i+0.5,x.coordinates.j+0.5,x.coordinates.k+0.5))

    plot_scatter_points(ax, coordinateList)

    # plt.title('My Plot o\' Stuff')
    plt.show()



plot_tree()






















# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# plot_linear_cube(ax, [2, 4], [2, 4], [0, 1])
# plot_linear_cube(ax, [2, 3], [2, 3], [0, 0.5])
# plot_scatter_points(ax, [(2.5,2.5,.25), (3,3,.75), (2,2,1)])
# plot_linear_cube(ax, [2, 3], [3, 4], [0.5, 1])
# plot_linear_cube(ax, [3, 4], [2, 3], [0, 0.5])
# plt.title('My Plot o\' Stuff')
# plt.show()


# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# plot_linear_cube(ax, [0,3],[0,3],[0,3])
# plt.show()

