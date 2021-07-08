#!/usr/bin/env python

# Copyright 2017 Thomas Paviot (tpaviot@gmail.com)
##
# This file is part of pythonOCC.
##
# pythonOCC is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# pythonOCC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with pythonOCC.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from base_occ import dispocc, spl_face

from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.Graphic3d import Graphic3d_NameOfMaterial, Graphic3d_NOM_ALUMINIUM, Graphic3d_NOM_COPPER, Graphic3d_NOM_BRASS
from OCC.Extend.ShapeFactory import get_aligned_boundingbox, get_oriented_boundingbox


def get_boundingbox(shape, tol=1e-6, use_mesh=True):
    """ return the bounding box of the TopoDS_Shape `shape`
    Parameters
    ----------
    shape : TopoDS_Shape or a subclass such as TopoDS_Face
        the shape to compute the bounding box from
    tol: float
        tolerance of the computed boundingbox
    use_mesh : bool
        a flag that tells whether or not the shape has first to be meshed before the bbox
        computation. This produces more accurate results
    """
    bbox = Bnd_Box()
    bbox.SetGap(tol)
    if use_mesh:
        mesh = BRepMesh_IncrementalMesh()
        mesh.SetParallelDefault(True)
        mesh.SetShape(shape)
        mesh.Perform()
        if not mesh.IsDone():
            raise AssertionError("Mesh not done.")
    brepbndlib_Add(shape, bbox, use_mesh)

    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    return xmin, ymin, zmin, xmax, ymax, zmax, xmax - xmin, ymax - ymin, zmax - zmin


if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    obj = dispocc(touch=True)

    print("Box bounding box computation")
    box_shape = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()
    bb1 = get_boundingbox(box_shape)
    print(bb1)
    obj.display.DisplayShape(box_shape, transparency=0.9,
                             material=Graphic3d_NOM_BRASS)

    print("Cylinder bounding box computation")
    cyl_shape = BRepPrimAPI_MakeCylinder(10., 20.).Shape()
    bb2 = get_boundingbox(cyl_shape)
    print(bb2)
    obj.display.DisplayShape(cyl_shape, transparency=0.9)

    print("Torus bounding box computation")
    torus_shape = BRepPrimAPI_MakeCylinder(15., 5.).Shape()
    bb3 = get_boundingbox(torus_shape)
    print(bb3)
    obj.display.DisplayShape(torus_shape, transparency=0.9)
    obj.show()
