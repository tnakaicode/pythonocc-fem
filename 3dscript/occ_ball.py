import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from base_occ import dispocc

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
from OCC.Core.BRepGProp import brepgprop_VolumeProperties
from OCC.Core.BRepGProp import brepgprop_LinearProperties
from OCC.Core.GProp import GProp_GProps

if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    prop = GProp_GProps()

    obj = dispocc(touch=True)
    shp = obj.show_ellipsoid(rxyz=[10.0, 15.0, 20.0])

    brepgprop_VolumeProperties(shp, prop)
    mas = prop.Mass()
    print(mas)
    obj.display.DisplayMessage(gp_Pnt(), "{:.3f}".format(mas), 30.0)
    obj.show_axs_pln(scale=10.0)
    obj.show()
