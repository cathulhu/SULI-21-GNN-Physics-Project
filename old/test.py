import openpmd_api as io
import numpy as np

series = io.Series("openpmd_%T.bp", io.Access.read_only)

iterationGroup = series.iterations[1000]

print("openPMD version: ",
      series.openPMD)
      
if series.contains_attribute("author"):
    print("Author: ",
          series.author)
          
          
# record
E = iterationGroup.meshes["E"]

# record components
E_x = E["x"]


# unit system agnostic dimension
E_unitDim = E.unit_dimension

# ...
# io.Unit_Dimension.M

# conversion to SI
x_unit = E_x.unit_SI

x_data = E_x.load_chunk()
series.flush()

extent = E_x.shape

print("Iteration 100 contains {0} particle species:".format(len(iterationGroup.particles)))

print(
    "First values in E_x "
    "of shape: ",
    extent)


print(x_data[0, 0, :5])
