import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from linecache import getline, clearcache
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from base_occ import dispocc

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.Geom import Geom_SphericalSurface
from OCC.Extend.ShapeFactory import scale_shape
from OCCUtils.Topology import Topo
from OCCUtils.Construct import make_box, make_face, make_line, make_wire, make_edge
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
    obj.SelectMesh()
    axs = gp_Ax3()
    ax1 = gp_Ax3(gp_Pnt(-100, 0, 0), gp_Dir(0, 0, 1))
    ax2 = gp_Ax3(gp_Pnt(+200, 0, 0), gp_Dir(0, 1, 1))
    sphere1 = Geom_SphericalSurface(ax1, 50)
    sphere2 = Geom_SphericalSurface(ax2, 75)
    sphere3 = scale_shape(
        make_face(sphere2.Sphere()),
        2.0, 1.5, 0.9)

    obj.display.DisplayShape(sphere1)
    obj.display.DisplayShape(sphere2)
    obj.display.DisplayShape(sphere3, color="RED")

    obj.show()

    obj = dispocc(disp=False)
    obj.selected_shape = [
        make_face(sphere1.Sphere())
    ]
    obj.export_stp_selected()
    c, d, box = obj.gen_aligned_bounded_box()
    obj.selected_shape.append(box)
    obj.export_stp_selected()
