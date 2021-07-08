import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from linecache import getline, clearcache
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from base import set_trf, set_loc, spl_face
from base_occ import dispocc

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepProj import BRepProj_Projection
from OCC.Core.GeomProjLib import geomprojlib_Project
from OCCUtils.Topology import Topo
from OCCUtils.Construct import vec_to_dir, dir_to_vec
from OCCUtils.Construct import make_polygon

if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    axs = gp_Ax3(gp_Pnt(100, 0, 10), gp_Dir(0, 0.5, 1))

    px = np.linspace(-1, 1, 100) * 600
    py = np.linspace(-1, 1, 100) * 600
    mesh = np.meshgrid(px, py)
    surf = mesh[0]**2 / 1000 + mesh[1]**2 / 2000
    face = spl_face(*mesh, surf, axs)
    brep_surf = BRep_Tool.Surface(face)

    pts = []
    pts.append(gp_Pnt(-100, -200, 0))
    pts.append(gp_Pnt(+200, -300, 0))
    pts.append(gp_Pnt(+300, +400, 0))
    pts.append(gp_Pnt(+100, +200, 0))
    pts.append(gp_Pnt(-400, +500, 0))
    poly = make_polygon(pts, closed=True)
    #poly.Location(set_loc(gp_Ax3(), axs))

    proj = BRepProj_Projection(poly, face, axs.Direction())
    proj_poly = proj.Current()

    obj = dispocc(touch=True)
    obj.display.DisplayShape(face, color="BLUE", transparency=0.9)
    obj.display.DisplayShape(poly)
    obj.display.DisplayShape(proj_poly, color="BLUE")

    for i, e in enumerate(Topo(proj_poly).edges()):
        e_curve, u0, u1 = BRep_Tool.Curve(e)
        u = (u0 + u1) / 2
        u01, u11 = (u + u0) / 2, (u + u1) / 2
        print(e, u0, u1)
        p0 = e_curve.Value(u0)
        p1 = e_curve.Value(u1)
        p2 = gp_Pnt()
        v0, v1 = gp_Vec(), gp_Vec()
        e_curve.D2(u, p2, v0, v1)
        ax = gp_Ax3(p2, vec_to_dir(v0), vec_to_dir(v1))
        p3 = e_curve.Value(u01)
        p4 = e_curve.Value(u11)
        v0.Normalize()
        v1.Normalize()
        v0.Scale(50)
        v1.Scale(50)
        obj.show_axs_pln(ax, scale=100, name="edge p{:d}".format(i))
        obj.display.DisplayVector(v0, p2)
        obj.display.DisplayMessage(p3, "u0")
        obj.display.DisplayMessage(p4, "u1")

    obj.show_axs_pln(gp_Ax3(), scale=25, name="axs")
    obj.show_axs_pln(axs, scale=25, name="axs-surf")
    obj.show()
