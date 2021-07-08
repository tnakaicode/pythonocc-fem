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
from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM, Graphic3d_NOM_COPPER, Graphic3d_NOM_BRASS
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

    px = np.linspace(-1, 1, 100) * 100 + 50
    py = np.linspace(-1, 1, 200) * 100 - 50
    mesh = np.meshgrid(px, py)

    obj = dispocc(touch=True)
    pln1 = obj.make_plane_axs(rx=[-100, 100], ry=[-100, 100])
    pln2 = obj.make_plane_axs(gp_Ax3(gp_Pnt(), gp_Dir(1, 0, 0)),
                              rx=[-100, 100], ry=[-100, 100])
    box1 = make_box(gp_Pnt(50, -50, 0), 20, 30, 40)
    obj.display.DisplayShape(pln1, material=Graphic3d_NOM_ALUMINIUM)
    obj.display.DisplayShape(pln2, material=Graphic3d_NOM_COPPER)
    obj.display.DisplayShape(box1, material=Graphic3d_NOM_BRASS)
    obj.show_axs_pln()
    obj.show()
