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
    torus = obj.make_torus(gp_Ax3(), r0=3000, r1=2000)
    beam0 = gp_Ax3(
        gp_Pnt(7500, 1100, 0),
        gp_Dir(-1, 0, 0.1),
        gp_Dir(0, 0.1, 1)
    )
    beam1 = obj.run_beam_face(beam0, torus, tr=1)
    pts = [
        beam0.Location(), beam1.Location()
    ]
    for i in range(100):
        beam1 = obj.run_beam_face(beam1, torus, tr=0)
        pts.append(beam1.Location())
    ray = make_polygon(pts)
    
    obj.show_axs_pln(beam0, scale=100)
    obj.show_axs_pln(beam1, scale=100)
    obj.display.DisplayShape(torus, color="BLUE", transparency=0.9)
    obj.display.DisplayShape(ray)
    obj.show_axs_pln()
    obj.show()
