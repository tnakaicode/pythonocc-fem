import numpy as np
import sys
import os
import time
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from src_cython.poly import create_triangulation

# https://github.com/tpaviot/pythonocc-core/issues/1000
from OCC.Core.Poly import Poly_Triangle

vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=float)
elements = np.array([[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]], dtype=int)

occ_tris = create_triangulation(vertices, elements)
print(occ_tris)
