from OCC.Core.BRepBndLib import brepbndlib, brepbndlib_Add, brepbndlib_AddOBB, brepbndlib_AddOptimal
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.Bnd import Bnd_Box, Bnd_OBB
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

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Dir, gp_XYZ
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Extend.ShapeFactory import get_aligned_boundingbox, get_oriented_boundingbox
from OCCUtils.Topology import Topo
from OCCUtils.Construct import make_box, make_line, make_wire, make_edge
from OCCUtils.Construct import make_plane, make_polygon
from OCCUtils.Construct import point_to_vector, vector_to_point
from OCCUtils.Construct import dir_to_vec, vec_to_dir


def midpoint(pntA, pntB):
    """ computes the point that lies in the middle between pntA and pntB

    Parameters
    ----------

    pntA, pntB : gp_Pnt

    Returns
    -------

    gp_Pnt

    """
    vec1 = gp_Vec(pntA.XYZ())
    vec2 = gp_Vec(pntB.XYZ())
    veccie = (vec1 + vec2) * 0.5
    return gp_Pnt(veccie.XYZ())


def get_aligned_boundingbox_ratio(shape, tol=1e-6, optimal_BB=True, ratio=1):
    """ return the bounding box of the TopoDS_Shape `shape`

    Parameters
    ----------

    shape : TopoDS_Shape or a subclass such as TopoDS_Face
        the shape to compute the bounding box from

    tol: float
        tolerance of the computed boundingbox

    use_triangulation : bool, True by default
        This makes the computation more accurate

    Returns
    -------
        if `as_pnt` is True, return a tuple of gp_Pnt instances
         for the lower and another for the upper X,Y,Z values representing the bounding box

        if `as_pnt` is False, return a tuple of lower and then upper X,Y,Z values
         representing the bounding box
    """
    bbox = Bnd_Box()
    bbox.SetGap(tol)

    # note: useTriangulation is True by default, we set it explicitely, but t's not necessary
    if optimal_BB:
        use_triangulation = True
        use_shapetolerance = True
        brepbndlib_AddOptimal(
            shape, bbox, use_triangulation, use_shapetolerance)
    else:
        brepbndlib_Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    dx, mx = (xmax - xmin) * ratio, (xmax + xmin) / 2
    dy, my = (ymax - ymin) * ratio, (ymax + ymin) / 2
    dz, mz = (zmax - zmin) * ratio, (zmax + zmin) / 2
    x0, x1 = mx - dx / 2, mx + dx / 2
    y0, y1 = my - dy / 2, my + dy / 2
    z0, z1 = mz - dz / 2, mz + dz / 2
    corner1 = gp_Pnt(x0, y0, z0)
    corner2 = gp_Pnt(x1, y1, z1)
    center = midpoint(corner1, corner2)
    box_shp = BRepPrimAPI_MakeBox(corner1, corner2).Shape()
    return center, [dx, dy, dz], box_shp


def get_oriented_boundingbox_ratio(shape, optimal_OBB=True, ratio=1.0):
    """ return the oriented bounding box of the TopoDS_Shape `shape`

    Parameters
    ----------

    shape : TopoDS_Shape or a subclass such as TopoDS_Face
        the shape to compute the bounding box from
    optimal_OBB : bool, True by default. If set to True, compute the
        optimal (i.e. the smallest oriented bounding box). Optimal OBB is
        a bit longer.
    Returns
    -------
        a list with center, x, y and z sizes

        a shape
    """
    obb = Bnd_OBB()
    if optimal_OBB:
        is_triangulationUsed = True
        is_optimal = True
        is_shapeToleranceUsed = False
        brepbndlib_AddOBB(shape, obb, is_triangulationUsed,
                          is_optimal, is_shapeToleranceUsed)
    else:
        brepbndlib_AddOBB(shape, obb)

    # converts the bounding box to a shape
    aBaryCenter = obb.Center()
    aXDir = obb.XDirection()
    aYDir = obb.YDirection()
    aZDir = obb.ZDirection()
    aHalfX = obb.XHSize()
    aHalfY = obb.YHSize()
    aHalfZ = obb.ZHSize()
    dx = aHalfX * ratio
    dy = aHalfY * ratio
    dz = aHalfZ * ratio

    ax = gp_XYZ(aXDir.X(), aXDir.Y(), aXDir.Z())
    ay = gp_XYZ(aYDir.X(), aYDir.Y(), aYDir.Z())
    az = gp_XYZ(aZDir.X(), aZDir.Y(), aZDir.Z())
    p = gp_Pnt(aBaryCenter.X(), aBaryCenter.Y(), aBaryCenter.Z())
    anAxes = gp_Ax2(p, gp_Dir(aZDir), gp_Dir(aXDir))
    anAxes.SetLocation(gp_Pnt(p.XYZ() - ax * dx - ay * dy - az * dz))
    aBox = BRepPrimAPI_MakeBox(anAxes, 2.0 * dx, 2.0 * dy, 2.0 * dz).Shape()
    return aBaryCenter, [dx, dy, dz], aBox


if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    obj = dispocc(touch=True)

    shp = obj.read_cadfile("./as1_pe_203.stp", disp=False)
    trf = gp_Trsf()
    trf.SetRotation(gp_Ax1(gp_Pnt(), obj.base_axs.XDirection()), np.pi / 6)
    shp.Move(TopLoc_Location(trf))

    c1, d1xyz, box1 = get_aligned_boundingbox(shp)
    c2, d2xyz, box2 = get_oriented_boundingbox(shp)
    c3, d3xyz, box3 = get_aligned_boundingbox_ratio(shp, ratio=1.25)
    c4, d4xyz, box4 = get_oriented_boundingbox_ratio(shp, ratio=1.25)

    obj.display.DisplayShape(shp)
    obj.display.DisplayShape(box1, transparency=0.9, color="BLUE")
    obj.display.DisplayShape(box2, transparency=0.9, color="RED")
    obj.display.DisplayShape(box3, transparency=0.9, color="GREEN")
    obj.display.DisplayShape(box4, transparency=0.9, color="YELLOW")

    obj.selected_shape = [shp, box3]
    obj.export_stp_selected()

    obj.show_axs_pln()
    obj.show()
