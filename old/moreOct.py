import math
import matplotlib.pyplot as plt
import numpy as np




#helpful attribute classes

class Dimensions:
    x = 0
    y = 0
    z = 0

    def __init__(self, length, width, height):
        self.x = length
        self.y = width
        self.z = height


class Coordinate_Range:
    x_range = []
    y_range = []
    z_range = []

    # format ([x_min,x_max]),[y_min,y_max],[z_min,z_max])
    def __init__(self, x_arr, y_arr, z_arr):
        self.x_range = x_arr
        self.y_range = y_arr
        self.z_range = z_arr


class Child_Octant_Range:

    def set_octant_measurements(self):
        self.x1_length=self.x_first[1]-self.x_first[0]+1
        self.x2_length=self.x_second[1]-self.x_second[0]+1
        self.y1_length=self.y_first[1]-self.y_first[0]+1
        self.y1_length=self.y_second[1]-self.y_second[0]+1
        self.z1_length=self.z_first[1]-self.z_first[0]+1
        self.z2_length=self.z_second[1]-self.z_second[0]+1


    def __init__(self, passedNode):
        #length
        # print(f"** length            {passedNode.node_dimensions.x}")
        self.x_first=[0,math.floor(passedNode.node_dimensions.x/2)]
        # print(f"    x_first :   {self.x_first}")
        self.x_second=[math.ceil(passedNode.node_dimensions.x/2),passedNode.node_dimensions.x-1]
        #width
        self.y_first=[0,math.floor(passedNode.node_dimensions.y/2)]
        self.y_second=[math.ceil(passedNode.node_dimensions.y/2),passedNode.node_dimensions.y-1]
        #height
        self.z_first=[0,math.floor(passedNode.node_dimensions.z/2)]
        self.z_second=[math.ceil(passedNode.node_dimensions.z/2),passedNode.node_dimensions.z-1]

        #check for odd sizing and adjust to avoid overlap
        if self.x_first[1] == self.x_second[0]:
            # print("correcting overlap")
            self.x_first[1] -=1
        
        if self.y_first[1] == self.y_second[0]:
            # print("correcting overlap")
            self.y_first[1] -=1

        if self.z_first[1] == self.z_second[0]:
            # print("correcting overlap")
            self.z_first[1] -=1

        self.set_octant_measurements

        print(f"\t   Node partition segements: X:{self.x_first, self.x_second}\n\t\t\t\t     Y:{self.y_first, self.y_second}\n\t\t\t\t     Z:{self.z_first, self.z_second}\n")


class Position:
    x=0
    y=0
    z=0

    def __init__(self,x_coord,y_coord,z_coord):
        self.x=x_coord
        self.y=y_coord
        self.z=z_coord


class Momentum:
    i=0
    j=0
    k=0

    def __init__(self,i_vector,j_vector,k_vector):
        self.x=i_vector
        self.y=j_vector
        self.z=k_vector


def check_if_in_range(passed_particle, passed_range):
    if passed_particle.coordinates.x >= passed_range.x_range[0] and passed_particle.coordinates.x <= passed_range.x_range[1]:
        # print("x ok")
        if passed_particle.coordinates.y >= passed_range.y_range[0] and passed_particle.coordinates.y <= passed_range.y_range[1]:
            # print("y ok")
            if passed_particle.coordinates.z >= passed_range.z_range[0] and passed_particle.coordinates.z <= passed_range.z_range[1]:
                # print("z ok")
                return True

    return False







#component classes

class Particle:
    coordinates = None        # 3 axis coordinate that determines which ooctant it will reside in
    momentum_vector = None    # 3D vector representing direction particle will move in

    def __init__(self,x_coord,y_coord,z_coord):
        self.coordinates=Position(x_coord,y_coord,z_coord)

    def set_momentum (self,i,j,k):
        self.momentum_vector=Momentum(i,j,k)

    def set_position(self,x_coord,y_coord,z_coord):
        self.coordinates=Position(x_coord,y_coord,z_coord)






class Tree:
    root = None                 # pointer to root node
    octant_count = 0
    next_id=0
    total_particle_count = 0
    totalDimensions = None      # array list of dimension range, for top level first digits should be 0, ex: [0,5],[0,9],[0,12]
    split_threshold=1           #if more than X number of particles in a cell, split into octants
    abort_search_flag=False
    reorder_flag=False

    def __init__(self, length, width, height):      #supply the total dimensions of the oct-tree upon instantiation
        if length > 1 and width >1 and height >1:
            self.totalDimensions = Dimensions(length, width, height)

            print(f"\n  creating new tree with dimensions: {self.totalDimensions.x} {self.totalDimensions.y} {self.totalDimensions.z}\n")
            print("\n")
            #spawning first node into tree and passing it the coordinate range that will be its domain (the whole thing) until it inevitably gets split up
            self.root = Node([0,self.totalDimensions.x], [0,self.totalDimensions.y], [0,self.totalDimensions.z], self)
            self.octant_count+=1
        else:
            print("Failed to create Oct-tree! Tree must have minimum of 2 units of dimension in each axis.")
            
    def add_particle(self, passed_particle):
        print(f"\nTrying to add particle at: ({passed_particle.coordinates.x},{passed_particle.coordinates.y},{passed_particle.coordinates.z})...")
        if passed_particle.coordinates.x < self.totalDimensions.x and passed_particle.coordinates.y < self.totalDimensions.y and passed_particle.coordinates.z < self.totalDimensions.z:
            # print(f"Node {self.root.id} Check if particle in bounds?: True")
            #x=[0,{self.totalDimensions.x}], y=[0,{self.totalDimensions.y}], z=[0,{self.totalDimensions.z}]

            #pass to node now, go down the tree starting from self.root
            self.root.place_particle(passed_particle)
        else:
            print(f"Failed to add particle, location outside bounds of shape.")



class Node:
    owner_tree=None    # each node will have the same link to the parent tree for incrementing particle count

    def __init__(self, passed_length_range, passed_width_range, passed_height_range,passed_tree):
        # print(f" Creating new node over coord range: {passed_length_range, passed_width_range, passed_height_range}")

        self.node_dimensions = None         # description of size of volume within larger shape this section encompasses
        self.node_coordinate_ranges = None  # tells us where in the overall shape is this volume located
        self.octant_range_divisions=None    # what divisions will this octant be split up along if it gets partitioned?
        self.isBottomLayer=True             # flag that says if the node is part of the bottom most leafs, set to false after spawning child octants
        self.parent_node=None               # link to the node above this one
        self.particle_count=0               # when this goes over ... 1? ... we split the node into 8 more parts
        self.neighbors=[]                   # list of pointers to the other nodes in its level, will be empty for the top one, of course
        self.children=[]                    # pointer to leaf octants
        self.particles=[]
        self.owner_tree=passed_tree
        self.id=self.owner_tree.next_id
        self.owner_tree.next_id+=1
        self.owner_tree.octant_count+=1

        self.node_coordinate_ranges=Coordinate_Range(passed_length_range, passed_width_range, passed_height_range)
        # print(f"passed: {passed_length_range, passed_width_range, passed_height_range}")
        self.node_dimensions=Dimensions(passed_length_range[1]-passed_length_range[0],passed_width_range[1]-passed_width_range[0],passed_height_range[1]-passed_height_range[0])

        print(f"\t      Node {self.id} has dimensions: {self.node_dimensions.x} {self.node_dimensions.y} {self.node_dimensions.z}")
        # print(f"\t    Node {self.id} coordinate range: ", end ='')
        # print(f"X:{self.node_coordinate_ranges.x_range}, Y:{self.node_coordinate_ranges.y_range}, Z:{self.node_coordinate_ranges.z_range}")

        self.octant_range_divisions = Child_Octant_Range(self)




    def place_particle(self, passed_particle):
        # print("searching through tree for bottom layer...")
        
        if self.isBottomLayer:
            print(f"checking if particle in range for dimensions of Node {self.id}: ", end="")
            print(check_if_in_range(passed_particle, self.node_coordinate_ranges))
            
            if check_if_in_range(passed_particle, self.node_coordinate_ranges):
                if self.particle_count ==0:
                    self.particle_count+=1


                    self.particles.append(passed_particle)
                    print(f"\n\tParticle added at: {passed_particle.coordinates.x},{passed_particle.coordinates.y},{passed_particle.coordinates.z} in Node {self.id}\n")

                else:
                    print(f"\nThreshold of {self.owner_tree.split_threshold} particle reached! Partitition node into 8 octants...\n")
                    self.partition()
                    #now try to place that particle in one of the children
                    self.owner_tree.abort_search_flag=False
                    self.place_particle(passed_particle)
            else:
                for item in self.neighbors:
                    item.place_particle(passed_particle)
                    if self.owner_tree.abort_search_flag:
                        break
        else:
            for item in self.children:
                item.place_particle(passed_particle)
                if self.owner_tree.abort_search_flag:
                    break


    def partition(self):
        # spawned_node = Node(self.node_dimensions.x/8, self.node_dimensions.y/8, self.node_dimensions.z/8, self.owner_tree)
        # print(f"spawning with: {[self.octant_range_divisions.x_first[0],self.octant_range_divisions.x_first[1]+1], self.octant_range_divisions.y_first, self.octant_range_divisions.z_first, self.owner_tree}\n")
        
        spawned_node0 = Node(self.octant_range_divisions.x_first, self.octant_range_divisions.y_first, [self.octant_range_divisions.z_first[0],self.octant_range_divisions.z_first[1]+1], self.owner_tree)
        spawned_node1 = Node(self.octant_range_divisions.x_first, self.octant_range_divisions.y_first, self.octant_range_divisions.z_second, self.owner_tree)

        spawned_node2 = Node(self.octant_range_divisions.x_first, self.octant_range_divisions.y_second, self.octant_range_divisions.z_first, self.owner_tree)
        spawned_node3 = Node(self.octant_range_divisions.x_first, self.octant_range_divisions.y_second, self.octant_range_divisions.z_second, self.owner_tree)
        
        spawned_node4 = Node(self.octant_range_divisions.x_second, self.octant_range_divisions.y_first, self.octant_range_divisions.z_first, self.owner_tree)
        spawned_node5 = Node(self.octant_range_divisions.x_second, self.octant_range_divisions.y_first, self.octant_range_divisions.z_second, self.owner_tree)

        spawned_node6 = Node(self.octant_range_divisions.x_second, self.octant_range_divisions.y_second, self.octant_range_divisions.z_first, self.owner_tree)
        spawned_node7 = Node(self.octant_range_divisions.x_second, self.octant_range_divisions.y_second, self.octant_range_divisions.z_second, self.owner_tree)


        self.children.append(spawned_node0)
        self.children.append(spawned_node1)
        self.children.append(spawned_node2)
        self.children.append(spawned_node3)
        self.children.append(spawned_node4)
        self.children.append(spawned_node5)
        self.children.append(spawned_node6)
        self.children.append(spawned_node7)

        #give each node a link to its parent
        for x in self.children:
            x.parent_node=self

        #since we've now done the partition the parent node is no longer the bottom layer
        self.isBottomLayer=False

        #set the flag that says we need to go through and reorganize all the points in this node into the newly divided octants
        self.owner_tree.reorder_flag=True




# test = Tree(16, 16, 16)
test = Tree(6, 6, 6)

spawned_particle = Particle(0,0,0)
test.add_particle(spawned_particle)
test.add_particle(spawned_particle)
# test.add_particle(spawned_particle)


# spawned_particle2 = Particle(9,4,11)
# test.add_particle(spawned_particle2)

# test.add_particle(Particle(12,4,2))
# test.add_particle(Particle(12,4,14))

# test.add_particle(Particle(9,4,11))




























# # prepare some coordinates
# x, y, z = np.indices((16, 16, 16))

# # draw cuboids in the top left and bottom right corners, and a link between them

# cubes = []

# #for index in test.root.children:
#     #cubes.append(x < index.node_coordinate_ranges.x_range[1] & y < index.node_coordinate_ranges.y_range[1], z < index.node_coordinate_ranges.z_range[1])
#     # print(index.node_coordinate_ranges.x_range[1])
#     # print(index.node_coordinate_ranges.y_range[1])
#     # print(index.node_coordinate_ranges.z_range[1])
# cube1 = (x < test.root.node_dimensions.x) & (y < test.root.node_dimensions.y) & (z < test.root.node_dimensions.z)
# #cube1 = (x > 0) & (y > 0) & (z > 0)
# cube2 = (x > test.root.children[0].node_dimensions.x) & (y >= 5) & (z >= 5)


# # combine the objects into a single boolean array
# voxels = cube1 | cube2

# # set the colors of each object
# colors = np.empty(voxels.shape, dtype=object)
# colors[cube1] = '#20f2ffcc'
# colors[cube2] = 'green'

# # and plot everything
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# ax.voxels(voxels, facecolors=colors, edgecolor='k')

# plt.show()






# test.root.partition()






        # #TODO go through existing particles and reassign them to appropriate octants
        # for x in self.particles:
        #     print(x.coordinates.x, x.coordinates.y, x.coordinates.z)
        #     # self.owner_tree.add_particle(x)
        #     #TODO write remove function for particle to remove self from outdated list
        #     #x.remove_self