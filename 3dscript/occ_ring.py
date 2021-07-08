import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from linecache import getline, clearcache
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from base import plot2d
from base_occ import dispocc

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

from OCC.Core.gp import gp_Circ, gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCC.Core.Geom import Geom_Circle
from OCCUtils.Topology import Topo
from OCCUtils.Construct import make_box, make_line, make_wire, make_edge, make_circle
from OCCUtils.Construct import make_plane, make_polygon
from OCCUtils.Construct import point_to_vector, vector_to_point
from OCCUtils.Construct import dir_to_vec, vec_to_dir


def pon_de_ring(r=1, t=0.0):
    val = np.abs((2 * np.cos(t)**2 - 1)**2 - 1 / 2)
    z2 = np.abs((r - 6 + 2 * val) * (10 + 4 * val))
    return np.sqrt(z2)


if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    r0 = 1
    pt = np.linspace(0, 2 * np.pi, 100)
    pr = pon_de_ring(r0, pt)

    plt2d = plot2d(aspect="auto")
    plt2d.axs.plot(pt, pr)
    plt2d.SavePng(plt2d.tmpdir + "pon_de_ring.png")

    obj = dispocc(touch=True)
    axs = gp_Ax3()
    r0, r1, r2 = 20.0, 5.0, 1.5
    rt = 10
    nu = 200

    pu = np.linspace(0, 2 * np.pi, nu)
    crv = Geom_Circle(axs.Ax2(), r0)
    api = BRepOffsetAPI_ThruSections()
    # api.SetSmoothing(True)
    api.SetContinuity(True)
    for u in pu:
        p0, vz, vx = gp_Pnt(), gp_Vec(), gp_Vec()
        crv.D2(u, p0, vz, vx)
        vx = gp_Vec(axs.Location(), p0)
        ax1 = gp_Ax3(p0, vec_to_dir(vz), vec_to_dir(vx))
        #rad = pon_de_ring(radii, u)
        rad = r1 + r2 * np.sin(rt * u)
        cir = gp_Circ(ax1.Ax2(), rad)
        edg = make_edge(cir)
        rim = make_wire(edg)
        #obj.show_axs_pln(ax1, scale=0.1)
        # obj.display.DisplayShape(rim)
        print(u, p0)

        api.AddWire(rim)
    # api.Build()
    surf = api.Shape()

    beam0 = gp_Ax3(
        gp_Pnt(32.0, 0, 0),
        gp_Dir(-1, 0.5, 0.1),
        gp_Dir(0, 0.1, 1)
    )
    beam1 = obj.run_beam_face(beam0, surf, tr=1)
    pts = [
        beam0.Location(), beam1.Location()
    ]
    for i in range(100):
        beam1 = obj.run_beam_face(beam1, surf, tr=0)
        pts.append(beam1.Location())
    ray = make_polygon(pts)

    obj.display.DisplayShape(surf, color="BLUE", transparency=0.9)
    obj.display.DisplayShape(ray)
    obj.show_axs_pln(beam0, scale=0.5)
    obj.show_axs_pln(beam1, scale=0.5)

    # obj.show_axs_pln()
    obj.show()
