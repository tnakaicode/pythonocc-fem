import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from base_occ import dispocc, rotate_xyz

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

from OCC.Core.gp import gp_Ax3, gp_Circ, gp_Dir, gp_Pnt
from OCC.Core.BRepFill import BRepFill_Filling
from OCC.Core.GeomAbs import GeomAbs_Arc, GeomAbs_C0, GeomAbs_C1, GeomAbs_C2
from OCC.Core.GeomAbs import GeomAbs_G1, GeomAbs_G2
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepOffset import BRepOffset_MakeOffset, BRepOffset_Skin
from OCC.Core.V3d import V3d_XnegYpos, V3d_XposYnegZpos, V3d_XposYposZpos
from OCCUtils.Topology import Topo
from OCCUtils.Construct import make_face, make_plane, make_polygon, make_edge, make_wire, rotate
from OCCUtils.Construct import point_to_vector, vector_to_point
from OCCUtils.Construct import dir_to_vec, vec_to_dir


class Circle3D(dispocc):

    def __init__(self, disp=True, touch=True):
        dispocc.__init__(self, disp=disp, touch=touch)
        self.add_function("View", self.display.View_Iso)

        axs = gp_Ax3(gp_Pnt(),
                     gp_Dir(0, 0, -1),
                     gp_Dir(0, 1, 0))

        radii = 10.0
        shift = 0.0
        dat = [35, 20, 10, 5, 1, 0.5]
        dat.append(100 - np.sum(dat))
        col = ["BLUE", "RED", "GREEN", "YELLOW"]
        print(dat)
        val = 0
        cir = gp_Circ(axs.Ax2(), radii)
        shp = []
        for idx, rate in enumerate(dat):
            r0 = 2 * np.pi * dat[idx] / 100
            print(idx, rate, val, r0)
            edg = make_edge(cir, val, val + r0)
            crv, u0, u1 = BRep_Tool.Curve(edg)
            p0, p1 = gp_Pnt(), gp_Pnt()
            crv.D0(u0, p0)
            crv.D0(u1, p1)
            e0 = make_edge(axs.Location(), p0)
            e1 = make_edge(axs.Location(), p1)

            poly = make_wire([e0, edg, e1])
            face = make_face(poly)
            sold = BRepOffset_MakeOffset(
                face, 1.0, 1.0E-5,
                BRepOffset_Skin, False, True,
                GeomAbs_Arc, True, True).Shape()
            shp.append(sold)
            # self.display.DisplayShape(sold, transparency=0.9,
            #                          color=self.colors[idx % 5])
            val += r0
        self.display_shapes(shp)

    def display_shapes(self, shps, trs=0.9, col=True):
        for i, shp in enumerate(shps):
            if col == True:
                colr = self.colors[i % len(self.colors)]
            else:
                colr = None
            self.display.DisplayShape(shp, transparency=trs, color=colr)


if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    obj = Circle3D()
    obj.show()
