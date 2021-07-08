import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import os
from optparse import OptionParser

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Pnt2d, gp_Pln, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BRepOffset import BRepOffset_MakeOffset, BRepOffset_Skin, BRepOffset_Interval
from OCC.Core.GeomAbs import GeomAbs_C0, GeomAbs_C1, GeomAbs_C2
from OCC.Core.GeomAbs import GeomAbs_G1, GeomAbs_G2
from OCC.Core.GeomAbs import GeomAbs_Intersection, GeomAbs_Arc

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
#sold = BRepPrimAPI_MakePrism(face, gp_Vec(0, 0, 2)).Shape()

# generate SOILD
sold = BRepOffset_MakeOffset(
    face, 1.0, 1.0E-5, BRepOffset_Skin, False, True, GeomAbs_Arc, True, True).Shape()

obj.display.DisplayShape(sold)
obj.export_stp(sold)
obj.show()
