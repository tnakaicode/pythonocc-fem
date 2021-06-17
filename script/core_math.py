#!/usr/bin/env python

# Copyright 2009-2015 Jelle Feringa (jelleferinga@gmail.com)
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


import math
import time
import sys

from OCC.Core.FairCurve import FairCurve_MinimalVariation, FairCurve_DistributionOfEnergy, FairCurve_DistributionOfJerk, FairCurve_AnalysisCode
from OCC.Core.FEmTool import FEmTool_ElementsOfRefMatrix, FEmTool_LinearJerk, FEmTool_LinearFlexion
from OCC.Core.math import math_Vector, math_Matrix


if __name__ == "__main__":
    mat = math_Matrix()
