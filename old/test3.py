import openpmd_api as io


if __name__ == "__main__":
    series = io.Series("openpmd_%T.bp", io.Access.read_only)
    print("Read a Series with openPMD standard version %s" %
          series.openPMD)

    print("The Series contains {0} iterations:".format(len(series.iterations)))
    for i in series.iterations:
        print("\t {0}".format(i))
    print("")

    i = series.iterations[1000]


    print("Iteration 100 contains {0} meshes:".format(len(i.meshes)))

    for m in i.meshes:
        print("\t {0}".format(m))

    print("")

    print("Iteration 100 contains {0} particle species:".format(
        len(i.particles)))
        
    for ps in i.particles:
        print("\t {0}".format(ps))
        print("With records:")
        for r in i.particles[ps]:
            print("\t {0}".format(r))





#mesh / field shapes

E_x = i.meshes["E"]["x"]
E_shape = E_x.shape
print("\nField E.x has shape {0} and datatype {1}".format(E_shape, E_x.dtype))

B_x = i.meshes["B"]["x"]
B_shape = B_x.shape
print("\nField B.x has shape {0} and datatype {1}".format(B_shape, B_x.dtype))

# B_y = i.meshes["B"]["y"]
# B_shape = B_x.shape
# print("\nField B.y has shape {0} and datatype {1}".format(B_shape, B_y.dtype))

# B_z = i.meshes["B"]["z"]
# B_shape = B_x.shape
# print("\nField B.z has shape {0} and datatype {1}".format(B_shape, B_z.dtype))

j_x = i.meshes["j"]["x"]
j_shape = j_x.shape
print("\nField j.x has shape {0} and datatype {1}".format(j_shape, j_x.dtype))




all_data = E_x.load_chunk()
series.flush()
print("\nFull E/x is of shape {0} and starts with:".format(all_data.shape))
print("")
print(all_data[0, 0, :64])







# printing a scalar value
electrons = i.particles["electrons"]
charge = electrons["charge"]

position = electrons["position"]

position_x= position["x"]
position_y= position["y"]
position_z= position["z"]

id = electrons["id"]

series.flush()

print(charge)

for x in electrons:
    print(x)

print(f"{position_x[44],position_y[11],position_z[11]}")



    # E_x = i.meshes["E"]["x"]
    # shape = E_x.shape

    # print("Field E.x has shape {0} and datatype {1}".format(
    #       shape, E_x.dtype))

    # chunk_data = E_x[1:3, 1:3, 1:2]
    # # print("Queued the loading of a single chunk from disk, "
    # #       "ready to execute")
    # series.flush()
    # print("Chunk has been read from disk\n"
    #       "Read chunk contains:")
    # print(chunk_data)
    # for row in range(2):
    #     for col in range(2):
    #         print("\t({0}|{1}|{2})\t{3}".format(
    #            row + 1, col + 1, 1, chunk_data[row*chunk_extent[1]+col])
    #         )
    #     print("")

    # all_data = E_x.load_chunk()
    # series.flush()
    # print("Full E/x is of shape {0} and starts with:".format(all_data.shape))
    # print(all_data[0, 0, :5])

    # The files in 'series' are still open until the object is destroyed, on
    # which it cleanly flushes and closes all open file handles.
    # One can delete the object explicitly (or let it run out of scope) to
    # trigger this.
    # del series