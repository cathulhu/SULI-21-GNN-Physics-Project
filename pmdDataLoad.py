from numpy.lib.function_base import append
import openpmd_api as io
import math
import signal
import sys
import pprint

# def signal_handler(sig, frame):
#     sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)



def data_info():
    series = io.Series("openpmd_%T.bp", io.Access.read_only)
    i = series.iterations[1000]
    electrons = i.particles["electrons"]

    print("{0} meshes contained:".format(len(i.meshes)))

    #the different meshes, e-field, b-field, j, rho
    for m in i.meshes:
        print("\t {0}".format(m))

    print("")

    print("Contains {0} particle species:".format(len(i.particles)))
    









    
    for ps in i.particles:
        print("\t {0}".format(ps))
        print("")
        print("With records:")
        for r in i.particles[ps]:
            print("\t {0}".format(r))






def get_particles():
    series = io.Series("openpmd_%T.bp", io.Access.read_only)
    i = series.iterations[1000]
    electrons = i.particles["electrons"]

    position = electrons["position"]
    position_x= position["x"]
    position_y= position["y"]
    position_z= position["z"]

    momentum = electrons["momentum"]
    momentum_x = momentum["x"]
    momentum_y = momentum["y"]
    momentum_z = momentum["z"]

    #mass and charge should always be the same for electrons, they're fungible
    charges = electrons["charge"][io.Mesh_Record_Component.SCALAR]
    mass = electrons["mass"][io.Mesh_Record_Component.SCALAR]
    ids = electrons["id"][io.Mesh_Record_Component.SCALAR]

    particle_locations=[]
    particle_locations_normalized=[]
    particle_momentums=[]

    count=0
    for x in position_x:
        count+=1

    print(f"Loading {count} Particles...")

    for x in range(0,count):
        particle_locations.append((position_x[x],position_y[x],position_z[x]))
        particle_locations_normalized.append((position_x[x],position_y[x],position_z[x]))
        particle_momentums.append((momentum_x[x],momentum_y[x],momentum_z[x]))
        

    series.flush()

    for x in range(0, len(particle_locations_normalized)):
        particle_locations_normalized[x]=(round(particle_locations[x][0]*math.pow(10,6),4), round(particle_locations[x][1]*math.pow(10,6),4), round(particle_locations[x][2]*math.pow(10,6),4))

    return particle_locations_normalized


# get_particles()

# def get_size(input):
#     # print(f"max values: X={max(x_loc)}, Y={max(y_loc)}, Z={max(z_loc)}")
#     # print(f"min values: X={min(x_loc)}, Y={min(y_loc)}, Z={min(z_loc)}")










    # E_x = i.meshes["E"]["x"]
    # E_y = i.meshes["E"]["y"]
    # E_z = i.meshes["E"]["z"]
    # series.flush()

    # print(E_x.shape)

    # import code; code.interact(local=dict(globals(), **locals()))






# series = io.Series("openpmd_%T.bp", io.Access.read_only)
# # print("Read a Series with openPMD standard version %s" %
# #           series.openPMD)

# iteration_count = len(series.iterations)

# print(f"The Series contains {iteration_count} iterations:")

# for i in series.iterations:
#     print("\t {0}".format(i))
# print("")

# i = series.iterations[1000]

# print("{0} meshes contained:".format(len(i.meshes)))

# #the different meshes, e-field, b-field, j, rho
# for m in i.meshes:
#     print("\t {0}".format(m))

# print("")

# print("Contains {0} particle species:".format(
#     len(i.particles)))


    
# for ps in i.particles:
#     print("\t {0}".format(ps))
#     print("")
#     print("With records:")
#     for r in i.particles[ps]:
#         print("\t {0}".format(r))














# E_x = i.meshes["E"]["x"]
# E_shape = E_x.shape
# print("\nField E.x has shape {0} and datatype {1}".format(E_shape, E_x.dtype))

# all_data = E_x.load_chunk()
# series.flush()
# print("\nFull E/x is of shape {0} and starts with:".format(all_data.shape))
# print("")
# print(all_data[0, 0, :64])








# electrons = i.particles["electrons"]

# # import code; code.interact(local=dict(globals(), **locals()))

# position = electrons["position"]

# position_x= position["x"]
# position_y= position["y"]
# position_z= position["z"]


# # record
# E = i.meshes["E"]

# # record components
# E_x = E["x"]

# E_unitDim = E.unit_dimension

# # conversion to SI
# x_unit = E_x.unit_SI




# count=0
# particle_locations=[]
# x_loc=[]
# y_loc=[]
# z_loc=[]

# for x in position_x:
#     count+=1

# print(f"\nfound {count} particles")

# for x in range(0,count):
#     particle_locations.append((position_x[x],position_y[x],position_z[x]))

# series.flush()

# for x in particle_locations:

#     x=( x[0]*math.pow(10,6),x[1]*math.pow(10,6),x[2]*math.pow(10,6) )

#     print(x[0],x[1], x[2])

# for x in particle_locations:
#     x_loc.append(x[0])
#     y_loc.append(x[1])
#     z_loc.append(x[2])

# print("\n")
# print(f"max values: X={max(x_loc)}, Y={max(y_loc)}, Z={max(z_loc)}")
# print(f"min values: X={min(x_loc)}, Y={min(y_loc)}, Z={min(z_loc)}")



