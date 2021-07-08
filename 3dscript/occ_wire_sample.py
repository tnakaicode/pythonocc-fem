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

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.BRepAdaptor import BRepAdaptor_CompCurve, BRepAdaptor_HCompCurve
from OCC.Core.Approx import Approx_Curve2d, Approx_Curve3d
from OCC.Core.GeomAbs import GeomAbs_Shape
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve
from OCC.Core.GCPnts import GCPnts_AbscissaPoint_Length
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
    axs = gp_Ax3()

    pts = []
    for t in np.linspace(0, np.pi, 5):
        x = np.sin(t)
        y = np.cos(t)
        z = np.sin(t) * np.cos(t)
        pts.append(gp_Pnt(x, y, z))
    wire = make_polygon(pts, closed=False)

    sample_resolution = 10
    c = BRepAdaptor_CompCurve()
    c.Initialize(wire, True)
    curve = BRepAdaptor_HCompCurve(c)
    # compute length of curve for sampling
    approx = Approx_Curve3d(curve, 0.001, GeomAbs_Shape.GeomAbs_C2, 1000, 25)
    geom_curve = approx.Curve()
    adaptor_curve = GeomAdaptor_Curve(geom_curve)
    l = GCPnts_AbscissaPoint_Length(adaptor_curve)
    # sample from curve using
    nr_sample_points = int(sample_resolution * l)
    sampled_curve = []
    point_samples_local = []
    for j in np.linspace(curve.FirstParameter(), curve.LastParameter(), nr_sample_points):
        p = curve.Value(j)
        point_samples_local.append(p)
        sampled_curve.append([p.X(), p.Y(), p.Z()])
        obj.display.DisplayShape(p)
    # sampled_curves.append(np.array(sampled_curve))
    # point_samples.append(point_samples_local)

    obj.display.DisplayShape(geom_curve)
    obj.show()
