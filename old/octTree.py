from re import L
from numpy.core.numeric import outer


class Octant:
    particle_list = []
    leafs = []
    length=0
    width=0
    height=0

    def __init__(self,l,w,h):
        self.length=l
        self.width=w
        self.height=h
        print(f"Created ocatant with dimensions of {l}, {w}, {h}")

    def add_particle(self, location, momentum):
        spawnedParticle = Particle()
        spawnedParticle.location_vector=location
        spawnedParticle.momentum_vector=momentum

        self.particle_list.append(spawnedParticle)

class Particle:
    location_vector = []
    momentum_vector = []

    def __init__(self):
        print("test")


class Cube:
    outer_octants=[]
    octant_range=[]
    x_coord_range:[0,0]
    y_coord_range:[0,0]
    z_coord_range:[0,0]

    for x in range(0,8):
        octant_range.append([])

    def __init__(self,length,width,height):
        for x in range(0,8):
            self.outer_octants.append(Octant(length/2,width/2,height/2))


a = Cube(11,5,20)