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

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound
from OCC.Core.TopLoc import TopLoc_Location
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
    # obj.create_tempdir(flag=-1)
    axs = gp_Ax3()

    px = np.linspace(-1, 1, 100) * 100 + 50
    py = np.linspace(-1, 1, 200) * 100 - 50
    mesh = np.meshgrid(px, py)
    data = mesh[0]**2 / 1000
    surf = spl_face(*mesh, data)

    obj.display.DisplayShape(surf)
    obj.display.FitAll()
    obj.export_cap()
    for i in range(10):
        trsf = gp_Trsf()
        trsf.SetRotation(obj.base_axs.Axis(), np.deg2rad(20))
        surf.Move(TopLoc_Location(trsf))
        # obj.display.View.Update()
        obj.display.Viewer.Redraw()
        #obj.display.DisplayShape(surf, update=True)
        obj.display.FitAll()
        obj.export_cap()

    obj.show()
