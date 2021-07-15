import openpmd_api as io
import numpy as np

series = io.Series("openpmd_%T.bp", io.Access.read_only)
seriesOutput = io.Series(
    "data_%05T.h5",
    io.Access.create)