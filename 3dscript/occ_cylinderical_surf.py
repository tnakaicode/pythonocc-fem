import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from linecache import getline, clearcache
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from base_occ import dispocc

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.gp import gp_Elips, gp_Circ
from OCC.Core.AIS import AIS_Shape, AIS_RadiusDimension, AIS_AngleDimension, AIS_Animation
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_BLACK
from OCC.Core.Prs3d import Prs3d_DimensionAspect
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.BRepProj import BRepProj_Projection
from OCC.Extend.DataExchange import write_step_file, read_step_file
from OCC.Extend.DataExchange import write_stl_file, read_stl_file
from OCCUtils.Construct import make_edge, make_face, make_polygon, make_wire, point_to_vector, vector_to_point
from OCCUtils.Construct import dir_to_vec, vec_to_dir

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)


def make_spiral(r=1, z=1.0):
    pn = int(100 * r)
    pt = np.linspace(0, 2 * np.pi, pn)
    pz = np.linspace(0, z, pn)
    pts = []
    for i, t in enumerate(pt):
        x = np.cos(r * t)
        y = np.sin(r * t)
        z = pz[i]
        pts.append(gp_Pnt(x, y, z))
    return make_polygon(pts, closed=True)


if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    obj = dispocc(touch=True)
    axs = gp_Ax3()
    
    circ_ax2 = axs.Ax2()
    circ = gp_Circ(circ_ax2, 75)
    circ_edg = make_edge(circ)

    elip_ax2 = axs.Ax2()
    elip = make_wire(make_edge(gp_Elips (elip_ax2, 100, 50)))
    
    rd = AIS_RadiusDimension(circ_edg)
    the_aspect = Prs3d_DimensionAspect()
    the_aspect.SetCommonColor(Quantity_Color(Quantity_NOC_BLACK))
    rd.SetDimensionAspect(the_aspect)
    
    obj.display.Context.Display(rd, True)
    obj.display.DisplayShape(elip)
    obj.display.DisplayShape(circ_edg)

    obj.show()
