import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from linecache import getline, clearcache
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from src.base_occ import dispocc

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound
from OCC.Core.TopLoc import TopLoc_Location
from OCCUtils.Topology import Topo
from OCCUtils.Construct import gp_vec_print, make_box, make_line, make_wire, make_edge
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

    obj = dispocc()

    # Base axs
    axs = gp_Ax3()
    pln = obj.make_plane_axs(axs, rx=[0, 2], ry=[0, 2])

    # Beam axs
    ax1 = gp_Ax3(
        gp_Pnt(1, 1, 1),
        gp_Dir(0.1, -0.2, 0.3),
        gp_Dir(0.9, 0.1, 0.1)
    )
    ax1_prj = obj.proj_pnt_pln(ax1.Location(), pln, axs)
    ax1_dst = obj.prop_axs(ax1, scale=0.25).Location()

    # Ref Coord
    # Z Direction: beam-pnt -> axs-ZDir
    # Y Direction: axs-ZDir
    ax1_loc = gp_Ax3(ax1.Ax2())
    ax1_loc.SetDirection(vec_to_dir(gp_Vec(ax1_prj, axs.Location())))
    ax1_loc.SetYDirection(axs.Direction())
    v_z = dir_to_vec(ax1_loc.Direction())
    v_x = dir_to_vec(ax1_loc.XDirection())
    v_y = dir_to_vec(ax1_loc.YDirection())

    # Ref Coord XY-Plane
    ax1_pxy = obj.make_plane_axs(ax1_loc, rx=[-0.25, 0.25], ry=[-0.25, 0.25])
    pnt_pxy = obj.proj_pnt_pln(ax1_dst, ax1_pxy, ax1_loc)
    lin_pxy = make_edge(ax1_loc.Location(), pnt_pxy)
    vec_pxy = gp_Vec(ax1_loc.Location(), pnt_pxy)
    deg_pxy = v_x.AngleWithRef(vec_pxy, v_z)
    txt_pxy = "pnt_pxy: {:.1f}".format(np.rad2deg(deg_pxy))
    obj.display.DisplayShape(make_edge(pnt_pxy, ax1_dst))
    obj.display.DisplayMessage(pnt_pxy, txt_pxy)
    print(np.rad2deg(deg_pxy))

    # Ref Coord YZ-Plane
    ax1_ayz = gp_Ax3(ax1_loc.Ax2())
    ax1_ayz.SetXDirection(ax1_loc.YDirection())
    ax1_ayz.SetDirection(ax1_loc.XDirection())
    ax1_pyz = obj.make_plane_axs(ax1_ayz, rx=[-0.25, 0.25], ry=[-0.25, 0.25])
    pnt_pyz = obj.proj_pnt_pln(ax1_dst, ax1_pyz, ax1_ayz)
    lin_pyz = make_edge(ax1_loc.Location(), pnt_pyz)
    vec_pyz = gp_Vec(ax1_loc.Location(), pnt_pyz)
    deg_pyz = v_z.AngleWithRef(vec_pyz, v_x.Reversed())
    txt_pyz = "pnt_pyz: {:.1f}".format(np.rad2deg(deg_pyz))
    obj.display.DisplayShape(make_edge(pnt_pyz, ax1_dst))
    obj.display.DisplayMessage(pnt_pyz, txt_pyz)
    print(np.rad2deg(deg_pyz))

    obj.show_axs_pln(axs, scale=1)
    obj.show_axs_pln(ax1, scale=0.75)
    obj.show_axs_pln(ax1_loc, scale=0.25)
    obj.display.DisplayShape(pln, transparency=0.9)
    obj.display.DisplayShape(ax1_pxy, color="RED", transparency=0.9)
    obj.display.DisplayShape(lin_pxy, color="BLUE")
    obj.display.DisplayShape(ax1_pyz, color="GREEN", transparency=0.9)
    obj.display.DisplayShape(lin_pyz, color="BLUE")
    obj.display.DisplayShape(ax1_prj)
    obj.show()
