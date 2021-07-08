import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from linecache import getline, clearcache
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from base_occ import dispocc, spl_curv, spl_face

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.BRep import BRep_CurveRepresentation, BRep_Tool
from OCC.Core.BRepFill import BRepFill_Filling
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
from OCC.Core.GeomAbs import GeomAbs_C0, GeomAbs_G2
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCCUtils.Topology import Topo
from OCCUtils.Construct import make_box, make_line, make_wire, make_edge
from OCCUtils.Construct import make_plane, make_polygon
from OCCUtils.Construct import point_to_vector, vector_to_point
from OCCUtils.Construct import dir_to_vec, vec_to_dir

if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    obj = dispocc(touch=True)

    num = 100
    pt = np.linspace(np.pi / 6, 2 * np.pi, num)
    pts = []
    for i, t in enumerate(pt):
        x = np.sin(t)
        y = np.cos(t)
        z = np.sin(t / 2)
        pts.append(gp_Pnt(x, y, z))

    p_array = TColgp_Array1OfPnt(1, num)
    #p_array = TColgp_Array1OfPnt(1, num + 1)
    for idx, t in enumerate(pts):
        p_array.SetValue(idx + 1, pts[idx])
    #p_array.SetValue(num + 1, pts[0])
    api = GeomAPI_PointsToBSpline(p_array)
    crv = api.Curve()
    obj.display.DisplayShape(crv)

    px = np.linspace(-1, 1, 100) * 1.5
    py = np.linspace(-1, 1, 200) * 1.5
    mesh = np.meshgrid(px, py)
    face = spl_face(*mesh, mesh[0]**2 / 1000)
    rim = make_polygon(pts, closed=True)

    n_sided = BRepFill_Filling()
    for e in Topo(rim).edges():
        n_sided.Add(e, GeomAbs_C0)
    n_sided.Add(face, GeomAbs_G2)
    n_sided.Build()
    fce = n_sided.Face()
    obj.display.DisplayShape(fce)
    obj.display.DisplayShape(face)

    obj.show_axs_pln(scale=1)
    obj.show()
