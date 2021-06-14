import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from linecache import getline, clearcache
from optparse import OptionParser

basename = os.path.dirname(__file__)

sys.path.append(os.path.join("../"))
from base_occ import dispocc
from base_bempp import plotBEM

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

import bempp.api
from bempp.api.operators.boundary import maxwell, sparse

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound
from OCC.Core.TopLoc import TopLoc_Location
from OCCUtils.Topology import Topo
from OCCUtils.Construct import make_box, make_line, make_wire, make_edge
from OCCUtils.Construct import make_plane, make_polygon
from OCCUtils.Construct import point_to_vector, vector_to_point
from OCCUtils.Construct import dir_to_vec, vec_to_dir


@bempp.api.real_callable
def tangential_trace(x, n, domain_index, result):
    result[:] = np.cross(np.array([1, 0, 0]), n)


if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    obj = plotBEM()
    # https://arxiv.org/abs/1703.10900

    k = 2
    #grid = bempp.api.shapes.cube(h=0.1)
    #bempp.api.export(obj.tempname + ".msh", grid, write_binary=False)
    grid = bempp.api.import_grid(obj.tempname + ".msh")
    space_segment = maxwell.multitrace_operator(grid, k)
    obj.grid = grid
    multitrace = maxwell.multitrace_operator(grid, k)
    identity = sparse.multitrace_identity(space_segment)
    calderon = 0.5 * identity - multitrace
    electric_trace = bempp.api.GridFunction(
        space=calderon.domain_spaces[0],
        fun=tangential_trace,
        dual_space=calderon.dual_to_range_spaces[0]
    )
    magnetic_trace = bempp.api.GridFunction(
        space=calderon.domain_spaces[1],
        fun=tangential_trace,
        dual_space=calderon.dual_to_range_spaces[1]
    )

    #trace_1 = calderon * [electric_trace, magnetic_trace]
    #trace_2 = calderon * trace_1
    #
    #electric_error = (trace_2[0]-trace_1[0]).l2_norm()/(trace_1[0].l2_norm())
    #magnetic_error = (trace_2[1]-trace_1[1]).l2_norm()/(trace_1[1].l2_norm())
    obj.convex_3d()
