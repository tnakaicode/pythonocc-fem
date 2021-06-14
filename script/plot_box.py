import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from linecache import getline, clearcache
from optparse import OptionParser

basename = os.path.dirname(__file__)

sys.path.append(os.path.join("../"))
from src.base_bempp import plotBEM, bempp_triangle_grid

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)
logging.getLogger('numba').setLevel(logging.ERROR)
logging.getLogger('bempp').setLevel(logging.ERROR)

import bempp

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3, gp_Sphere
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound
from OCC.Core.TopLoc import TopLoc_Location
from OCCUtils.Topology import Topo
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox
from OCCUtils.Construct import make_box, make_line, make_wire, make_edge, make_face
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

    obj = plotBEM()
    axs = gp_Ax3()
    box = make_box(100, 100, 100)
    pln = make_plane(vec_normal=gp_Vec(0, 0.5, 1))
    obj.selected_shape = [obj.make_cylinder_surf()]
    #obj.grid = bempp_triangle_grid(obj.make_comp_selcted(), isR=2.5, thA=2.5)
    # obj.export_stl_selected()
    obj.grid = bempp.api.import_grid(obj.tempname + "_001.stl")
    obj.convex_3d()
