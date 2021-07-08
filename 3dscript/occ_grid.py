import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import os

sys.path.append(os.path.join('../'))
from base_occ import dispocc

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.gp import gp_Pln
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.TColgp import TColgp_Array1OfPnt, TColgp_Array2OfPnt
from OCC.Core.TColgp import TColgp_HArray1OfPnt, TColgp_HArray2OfPnt
from OCC.Core.GeomAPI import GeomAPI_PointsToBSplineSurface
from OCC.Core.GeomAbs import GeomAbs_C0, GeomAbs_C1, GeomAbs_C2
from OCC.Core.GeomAbs import GeomAbs_G1, GeomAbs_G2
from OCC.Core.GeomAbs import GeomAbs_Intersection, GeomAbs_Arc

if __name__ == '__main__':
    obj = dispocc(touch=True)

    px = np.linspace(-1, 1, 100) * 200
    py = np.linspace(-1, 1, 300) * 200 + 150
    mesh = np.meshgrid(px, py)
    surf = mesh[0]**2 / 1000
    nx, ny = surf.shape

    pnt_2d = TColgp_Array2OfPnt(1, nx, 1, ny)
    for row in range(pnt_2d.LowerRow(), pnt_2d.UpperRow() + 1):
        for col in range(pnt_2d.LowerCol(), pnt_2d.UpperCol() + 1):
            i, j = row - 1, col - 1
            x, y, z = mesh[0][i, j], mesh[1][i, j], surf[i, j]
            pnt = gp_Pnt(x, y, z)
            pnt_2d.SetValue(row, col, pnt)
            #print (i, j, px[i, j], py[i, j], pz[i, j])

    #
    # Approximates a BSpline Surface passing through an array of Points.
    # The resulting BSpline will have the following properties:
    # 1- his degree will be in the range [Degmin,Degmax]
    # 2- his continuity will be at least <Continuity>
    # 3- the distance from the point <Points> to the BSpline will be lower to Tol3D.
    #
    api = GeomAPI_PointsToBSplineSurface(pnt_2d, 2, 2, GeomAbs_G2, 0.001)
    api.Interpolate(pnt_2d)
    #surface = BRepBuilderAPI_MakeFace(curve, 1e-6)
    # return surface.Face()
    face = BRepBuilderAPI_MakeFace(api.Surface(), 1e-6).Face()
    obj.display.DisplayShape(face)

    obj.show_axs_pln(scale=10)
    obj.show()
