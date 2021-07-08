import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from base_occ import dispocc, set_loc

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax3
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_ThruSections, BRepOffsetAPI_MakeOffset, BRepOffsetAPI_MakeEvolved, BRepOffsetAPI_MakePipe, BRepOffsetAPI_MakePipeShell
from OCC.Core.BRepOffset import BRepOffset_MakeOffset, BRepOffset_Skin, BRepOffset_Interval
from OCC.Core.GeomAbs import GeomAbs_C0
from OCC.Core.GeomAbs import GeomAbs_Intersection, GeomAbs_Arc
from OCCUtils.Construct import make_polygon
from OCCUtils.Construct import vec_to_dir, dir_to_vec


def poly_rotate_shape(poly, axis=gp_Ax3(), num=50):
    api = BRepOffsetAPI_ThruSections()
    print(poly.Location().Transformation())
    print(dir_to_vec(axis.Direction()))
    for idx, phi in enumerate(np.linspace(0, 2 * np.pi, num)):
        ax = axis.Rotated(axis.Axis(), phi)
        poly_i = poly.Located(set_loc(axis, ax))
        api.AddWire(poly_i)
    api.Build()
    return api.Shape()


if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    px = np.linspace(-1, 1, 100) * 100 + 50
    py = np.linspace(-1, 1, 200) * 100 - 50
    mesh = np.meshgrid(px, py)

    p0 = gp_Pnt(0, 50.0, 0)
    p1 = gp_Pnt(0, 60.0, 100.0)
    p2 = gp_Pnt(0, 50.0, 200.0)
    axis = gp_Ax3(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
    poly = make_polygon([p0, p1, p2])
    face = poly_rotate_shape(poly, axis)
    sold = BRepOffset_MakeOffset(
        face, 1.0, 1.0E-5, BRepOffset_Skin,
        False, True, GeomAbs_Arc, True, True
    ).Shape()

    obj = dispocc(touch=True)
    obj.display.DisplayShape(poly)
    obj.display.DisplayShape(face)
    obj.display.DisplayShape(sold, transparency=0.9, color="BLUE")
    obj.show_axs_pln(scale=50)
    obj.show()
