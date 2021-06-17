import numpy as np
cimport numpy as np
DTYPEF = np.float
DTYPEI = np.int

ctypedef np.float_t DTYPE_F_t
ctypedef np.int_t DTYPE_I_t

from cython.operator cimport dereference as deref

from OCC.Core._gp import new_gp_Pnt
from OCC.Core._TColgp import new_TColgp_Array1OfPnt, TColgp_Array1OfPnt_SetValue
from OCC.Core._Poly import \
     new_Poly_Array1OfTriangle, \
     Poly_Array1OfTriangle_SetValue, \
     new_Poly_Triangle, \
     new_Poly_Triangulation

from OCC.Core.Poly import Poly_Triangulation


def create_triangulation(np.ndarray[DTYPE_F_t, ndim=2] vertices, np.ndarray[DTYPE_I_t, ndim=2] faces):
    cdef int n_pts = vertices.shape[0]
    p_array = new_TColgp_Array1OfPnt(1, n_pts)

    for i in range(n_pts):
        TColgp_Array1OfPnt_SetValue(p_array, i+1, new_gp_Pnt(vertices[i,0],vertices[i,1],vertices[i,2]))

    cdef int n_faces = faces.shape[0]
    f_array = new_Poly_Array1OfTriangle(1, n_faces)

    for i in range(n_faces):
        Poly_Array1OfTriangle_SetValue(f_array, i+1, new_Poly_Triangle(int(faces[i,0])+1, int(faces[i,1])+1, int(faces[i,2])+1))


    return Poly_Triangulation(p_array, f_array)