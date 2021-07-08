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

from PyQt5.QtGui import QImage
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from base_occ import dispocc

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog

from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox


class QTDialog (dispocc):

    def __init__(self, touch=False):
        dispocc.__init__(self, touch=touch)

        my_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()

        self.add_menu("Change Background")
        self.add_function("Change Background", self.background1)
        self.add_function("Change Background", self.change_background)

        self.display.SetBackgroundImage(
            '../img/universe_Horsehead_Nebula.jpg', stretch=True)
        self.display.DisplayShape(my_box, update=True)

    def background1(self):
        self.display.SetBackgroundImage(
            '../img/20200605115919.png', stretch=True)

    def change_background(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self.wi, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        print(fileName)
        if os.path.exists(fileName):
            self.display.SetBackgroundImage(fileName, stretch=True)
            self.export_cap()


obj = QTDialog(touch=True)
obj.show()
