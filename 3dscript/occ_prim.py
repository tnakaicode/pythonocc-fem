import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import os
from optparse import OptionParser

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Pnt2d, gp_Pln, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BRepOffset import BRepOffset_MakeOffset
from OCC.Core.IMeshData import IMeshData_Failure
from OCC.Core.IMeshTools import IMeshTools_MeshBuilder, IMeshTools_MeshAlgo
from OCC.Core.MeshVS import MeshVS_Array1OfSequenceOfInteger

sys.path.append(os.path.join('../'))
from base_occ import dispocc

obj = dispocc(touch=True)

pts = []
pts.append(gp_Pnt(0, 0, 0))
pts.append(gp_Pnt(0, 1, 0.1))
pts.append(gp_Pnt(1, 1, -0.1))
pts.append(gp_Pnt(1, 0, 0))
pts.append(pts[0])

face = obj.make_FaceByOrder(pts)
sold = BRepPrimAPI_MakePrism(face, gp_Vec(0, 0, 2)).Shape()

obj.display.DisplayShape(sold)
obj.export_stp(sold)
obj.show()
