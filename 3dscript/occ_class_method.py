from OCC.Core.gp import gp_Ax3
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from linecache import getline, clearcache
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from base import plotocc
from base_occ import dispocc as plotocc

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)


class OCCCoord(plotocc):

    def __init__(self, touch=False):
        # super().__init__(touch=touch)
        axs = gp_Ax3()
        self.rootname = "test"
        
        #
        # self.create_tempdir(self)
        # got error
        #
        
        plotocc.create_tempdir(self)
        plotocc.export_stp(self, plotocc.make_EllipWire(self))

    def test_root(self, name="test01"):
        self.rootname = name
        plotocc.create_tempdir(self)
        plotocc.export_stp(self, plotocc.make_EllipWire(self))


if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    obj = OCCCoord()
    obj.test_root()
