from OCC.Core.BRepProj import BRepProj_Projection
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
from OCC.Extend.DataExchange import write_step_file, read_step_file
from OCC.Extend.DataExchange import write_stl_file, read_stl_file
from OCCUtils.Construct import make_face, make_polygon, point_to_vector, vector_to_point
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
    surf = obj.make_cylinder_surf(
        axs, radii=1, hight=1.75, rng=[0, 2 * np.pi], xyz="z")
    sprl = make_spiral()
    proj = BRepProj_Projection(sprl, surf, axs.Location())
    sprl_proj = proj.Current()
    trim = make_face(surf, sprl_proj)

    #proj = BRepProj_Projection(sprl, surf, axs.Location())
    #i = 0
    # while proj.More():
    #    shpe = proj.Current()
    #    obj.display.DisplayShape(shpe, color=obj.colors[i % 5])
    #    proj.Next()
    #    i += 1
    #    print(i)

    # obj.display.DisplayShape(surf)
    obj.display.DisplayShape(sprl)
    obj.display.DisplayShape(sprl_proj, color="BLUE")
    obj.display.DisplayShape(trim, color="RED")

    obj.show()
