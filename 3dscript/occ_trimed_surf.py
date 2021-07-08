import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from linecache import getline, clearcache
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from base_occ import dispocc, spl_face

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TColgp import TColgp_Array1OfPnt, TColgp_Array2OfPnt
from OCC.Core.TColgp import TColgp_HArray1OfPnt, TColgp_HArray2OfPnt
from OCC.Core.Geom import Geom_BoundedSurface
from OCC.Core.GeomAPI import GeomAPI_IntCS, GeomAPI_IntSS
from OCC.Core.GeomAPI import GeomAPI_PointsToBSplineSurface
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
from OCC.Core.GeomAPI import GeomAPI_Interpolate
from OCC.Core.GeomAbs import GeomAbs_C0, GeomAbs_C1, GeomAbs_C2
from OCC.Core.GeomAbs import GeomAbs_G1, GeomAbs_G2
from OCC.Core.GeomAbs import GeomAbs_Intersection, GeomAbs_Arc
from OCCUtils.Topology import Topo
from OCCUtils.Construct import make_box, make_line, make_wire, make_edge
from OCCUtils.Construct import make_plane, make_polygon
from OCCUtils.Construct import point_to_vector, vector_to_point
from OCCUtils.Construct import dir_to_vec, vec_to_dir


def spl_surf(px, py, pz, axs=gp_Ax3()):
    nx, ny = px.shape
    pnt_2d = TColgp_Array2OfPnt(1, nx, 1, ny)
    for row in range(pnt_2d.LowerRow(), pnt_2d.UpperRow() + 1):
        for col in range(pnt_2d.LowerCol(), pnt_2d.UpperCol() + 1):
            i, j = row - 1, col - 1
            pnt = gp_Pnt(px[i, j], py[i, j], pz[i, j])
            pnt_2d.SetValue(row, col, pnt)
            #print (i, j, px[i, j], py[i, j], pz[i, j])

    api = GeomAPI_PointsToBSplineSurface(pnt_2d, 3, 8, GeomAbs_G2, 0.001)
    api.Interpolate(pnt_2d)
    return api.Surface()


if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    obj = dispocc(touch=True)

    axs = gp_Ax3(
        gp_Pnt(1, 1, 1),
        gp_Dir(0, 0.1, 1.0),
        gp_Dir(0.1, 0.1, 0.0)
    )

    px = np.linspace(-1, 1, 500) * 75
    py = np.linspace(-1, 1, 750) * 75
    mesh = np.meshgrid(px, py)
    data = mesh[0]**2 / 1000 + mesh[1]**2 / 2000
    surf = spl_face(*mesh, data - 2, axs)

    pnt_2d = [
        gp_Pnt(-30, -30, 0),
        gp_Pnt(+40, -20, 1),
        gp_Pnt(+45, +30, -1),
        gp_Pnt(0, +45, 0),
        gp_Pnt(-35, +40, 0)
    ]
    rim_2d = make_polygon(pnt_2d, closed=True)
    rim = obj.proj_rim_pln(rim_2d, surf)

    obj.show_axs_pln(gp_Ax3(), scale=25)
    obj.display.DisplayShape(surf)
    obj.display.DisplayShape(rim_2d)
    obj.display.DisplayShape(rim, color="YELLOW")
    obj.show()
