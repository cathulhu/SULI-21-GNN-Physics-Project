import math
from pprint import pprint
from operator import length_hint


class Root:

    octant_ranges=[]
    octants=[]
    particles=[]
    
    particle_count=0
    length=0
    width=0
    height=0
    

    def __init__(self,l,w,h):

        #-1 to adjust for zero indexing
        self.length=l
        self.width=w
        self.height=h

        print(f"Created root with dimensions: {l}, {w}, {h}")
        #length
        self.octant_ranges.append([0,math.floor(self.length/2)])
        self.octant_ranges.append([math.ceil(self.length/2),self.length-1])
        #width
        self.octant_ranges.append([0,math.floor(self.width/2)])
        self.octant_ranges.append([math.ceil(self.width/2),self.width-1])
        #height
        self.octant_ranges.append([0,math.floor(self.height/2)])
        self.octant_ranges.append([math.ceil(self.height/2),self.height-1])
        
        #check for odd sizing and adjust to avoid overlap        
        for x in range(0, len(self.octant_ranges)-1):
            if self.octant_ranges[x][1] == self.octant_ranges[x+1][0]:
                self.octant_ranges[x][1]-=1
        
        print("octant ranges:")

        for x in self.octant_ranges:
            print(x)





    def add_particle(self, passed_particle):
        print(f"adding particle at: {passed_particle.location_vect}")

        #first check if particle is in bound
        for x in range(0,6):
            if passed_particle.location_vect[0]<=self.length and passed_particle.location_vect[0] <= self.width and passed_particle.location_vect[0] <= self.height:
                
                if self.particle_count==0:
                    self.particles.append(passed_particle)
            else:
                print("Failed to add particle, outside of bounds")

        #next we'll check to see if the location of the particle warrants warrants the

        print("octant has the following particles:")
        for x in self.particles:
            print(x.location_vect)





    def remove_particle(self,coordinates):
        print(f"Trying to remove particle at {coordinates}")
        for x in self.particles:
            if (x.location_vect==coordinates):
                print("Particle found, removing.")
                self.particles.remove(x)

        print("After remove, octant has the following particles:")
        for x in self.particles:
            print(x.location_vect)





class Particle:
    location_vect=[0,0,0]
    momentum_vect=[0,0,0]

    def __init__(self, loc, mom):
        self.location_vect=loc
        self.momentum_vect=mom

a = Root(10,13,17)

testPart = Particle([1,3,11], [0,0,0])

a.add_particle(testPart)
# a.remove_particle([1,3,11])