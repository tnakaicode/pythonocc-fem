from poly import create_triangulation

# https://github.com/tpaviot/pythonocc-core/issues/1000
import numpy as np
from OCC.Core.Poly import Poly_Triangle

vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=float)
elements = np.array([[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]], dtype=int)

occ_tris = create_triangulation(vertices, elements)
print(occ_tris)
