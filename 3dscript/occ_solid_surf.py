import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from linecache import getline, clearcache
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from base_occ import dispocc, set_loc, spl_face, set_trf
from src.geometry import curvature

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

from OCC.Core.gp import gp_Circ, gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.TopoDS import topods, TopoDS_Shape, TopoDS_Compound
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.Geom import Geom_Surface
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeShell, BRepBuilderAPI_MakeSolid
from OCC.Core.GeomAPI import GeomAPI_PointsToBSplineSurface
from OCC.Core.GeomAbs import GeomAbs_G2
from OCC.Core.TColgp import TColgp_Array2OfPnt
from OCCUtils.Topology import Topo
from OCCUtils.Construct import make_box, make_line, make_shell, make_wire, make_edge
from OCCUtils.Construct import make_plane, make_polygon
from OCCUtils.Construct import point_to_vector, vector_to_point
from OCCUtils.Construct import dir_to_vec, vec_to_dir


    

def spl_shell(px, py, pz, axs=gp_Ax3()):
    nx, ny = px.shape
    pnt_2d = TColgp_Array2OfPnt(1, nx, 1, ny)
    for row in range(pnt_2d.LowerRow(), pnt_2d.UpperRow() + 1):
        for col in range(pnt_2d.LowerCol(), pnt_2d.UpperCol() + 1):
            i, j = row - 1, col - 1
            pnt = gp_Pnt(px[i, j], py[i, j], pz[i, j])
            pnt_2d.SetValue(row, col, pnt)
            #print (i, j, px[i, j], py[i, j], pz[i, j])

    api = GeomAPI_PointsToBSplineSurface(pnt_2d, 3, 8, GeomAbs_G2, 0.001)
    api.Interpolate(pnt_2d)
    surf = api.Surface()
    shell = BRepBuilderAPI_MakeShell(surf, True).Shell()
    shell.Location(set_loc(gp_Ax3(), axs))
    return shell


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
    ax1 = obj.prop_axs(axs, scale=10)
    ax2 = obj.prop_axs(axs, scale=-10)
    pln1 = obj.make_plane_axs(ax1, [-100, 100], [-100, 100])
    pln2 = obj.make_plane_axs(ax2, [-100, 100], [-100, 100])
    #pln_shell = BRepBuilderAPI_MakeShell(pln, True).Shell()

    px = np.linspace(-1, 1, 500) * 100
    py = np.linspace(-1, 1, 500) * 100
    mesh = np.meshgrid(px, py)
    data1 = mesh[0]**2 / 1000
    data2 = mesh[1]**2 / 2000

    surf1 = spl_shell(*mesh, data1, ax1)
    circ1 = make_wire(make_edge(gp_Circ(ax1.Ax2(), 50)))
    circ1_proj = obj.proj_rim_pln(circ1, surf1, ax1)

    surf2 = spl_shell(*mesh, data2, ax2)
    circ2 = make_wire(make_edge(gp_Circ(ax2.Ax2(), 50)))
    circ2_proj = obj.proj_rim_pln(circ2, surf2, ax2)
    
    thu = BRepOffsetAPI_ThruSections()
    thu.AddWire(circ1_proj)
    thu.AddWire(circ2_proj)
    surf = thu.Shape()
    
    api = BRepBuilderAPI_MakeSolid(surf, surf1, surf2)
    #api.Add(surf)
    api.Build()
    print(api.Shape())
    print(api.Solid())

    #obj.display.DisplayShape(surf1, transparency=0.9)
    #obj.display.DisplayShape(surf2, transparency=0.9)
    #obj.display.DisplayShape(api.Solid())

    #api = BRepBuilderAPI_MakeSolid(topods.Shell(pln1),
    #                               topods.Shell(pln2))
    #api.Build()
    print(api.Shape())
    print(api.Solid())

    obj.display.DisplayShape(pln1, transparency=0.9)
    obj.display.DisplayShape(pln2, transparency=0.9)
    obj.display.DisplayShape(api.Solid())
    
    obj.export_stp(api.Solid())

    obj.show()
