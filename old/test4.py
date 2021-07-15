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




print("\n")

# E_x = i.meshes["E"]["x"]
# # E_shape = E_x.shape
# # print("\nField E.x has shape {0} and datatype {1}".format(E_shape, E_x.dtype))

# all_data = E_x.load_chunk()
# series.flush()
# print("\nFull E/x is of shape {0} and starts with:".format(all_data.shape))
# print("")
# print(all_data[1, 63, :64])

# print("\n\n")




E_y_modes = i.meshes["E"]["y"]
shape = E_y_modes.shape  # (modal components, r, y)

# read E_z in all modes

#E_x_raw = E_x_modes[:, :, :]
# read E_z in mode_0 (one scalar field)

E_y_m0 = E_y_modes[0:1, 0:shape[1], 0:shape[2]]
# read E_z in mode_1 (two fields; skip mode_0 with one scalar field)

E_y_m1 = E_y_modes[1:3, 0:shape[1], 0:shape[2]]

series.flush()

print(E_y_m0)  # still mode-decomposed data, not too useful for users
