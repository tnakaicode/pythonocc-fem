#!/usr/bin/env python

# Copyright 2016 Thomas Paviot (tpaviot@gmail.com)
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

import os
import sys
#from __future__ import print_function

from OCC.Display.WebGl import threejs_renderer
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeTorus
from OCC.Core.gp import gp_Vec
from OCC.Extend.ShapeFactory import translate_shp

sys.path.append(os.path.join("../"))
from base import plotocc

obj = plotocc()

idx = 0
torus_shp1 = BRepPrimAPI_MakeTorus(20, 5).Shape()

torus_shp2b = BRepPrimAPI_MakeTorus(20, 5).Shape()
torus_shp2 = translate_shp(torus_shp2b, gp_Vec(60, 0, 0))

torus_shp3b = BRepPrimAPI_MakeTorus(20, 5).Shape()
torus_shp3 = translate_shp(torus_shp3b, gp_Vec(-60, 0, 0))

# default quality
print("Computing RED torus: default quality")
obj.display.DisplayShape(torus_shp1, color="RED")  # red

# better mesh quality, i.e. more triangles
print("Computing GREEN torus: better quality, more time to compute")
obj.display.DisplayShape(torus_shp2, color="GREEN")  # green

# worse quality, i.e. less triangles
print("Computing BLUE torus: worse quality, faster to compute")
obj.display.DisplayShape(torus_shp3, color="BLUE")  # blue

obj.show()
