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
from base_occ import dispocc

from PyQt5.QtGui import QImage
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepTools import breptools_Read
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.gp import gp_Pln, gp_Dir, gp_Pnt
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Section
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Extend.DataExchange import read_iges_file, read_step_file, read_stl_file


class QTDialog (dispocc):

    def __init__(self, touch=False):
        dispocc.__init__(self, touch=touch)

        my_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()

        #self.add_menu("Import File")
        #self.add_function("Import File", self.import_cadfile)

        self.display.DisplayShape(my_box, update=True)

    def import_cadfile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self.wi, 'QFileDialog.getOpenFileName()', '',
                                                  'CAD files (*.stp *.step *.stl *.igs *.iges, *.brep)', options=options)
        print(fileName)
        base_dir = os.path.dirname(fileName)
        basename = os.path.basename(fileName)
        rootname, extname = os.path.splitext(fileName)
        if extname in [".stp", ".step"]:
            shpe = read_step_file(fileName)
            self.display.DisplayShape(shpe, update=True)
        elif extname in [".igs", ".iges"]:
            shpe = read_iges_file(fileName)
            self.display.DisplayShape(shpe, update=True)
        elif extname in [".stl"]:
            shpe = read_stl_file(fileName)
            self.display.DisplayShape(shpe, update=True)
        elif extname in [".brep"]:
            shpe = TopoDS_Shape()
            builder = BRep_Builder()
            breptools_Read(shpe, fileName, builder)
            self.display.DisplayShape(shpe, update=True)
        else:
            print("Incorrect file index")
            #sys.exit(0)
        self.export_cap()


obj = QTDialog(touch=True)
obj.show()
