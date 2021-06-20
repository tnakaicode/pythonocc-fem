import math
import time
import sys

from OCC.Core.FairCurve import FairCurve_MinimalVariation, FairCurve_DistributionOfEnergy, FairCurve_DistributionOfJerk, FairCurve_AnalysisCode
from OCC.Core.FEmTool import FEmTool_ElementsOfRefMatrix, FEmTool_LinearJerk, FEmTool_LinearFlexion
from OCC.Core.math import math_Vector, math_Matrix

from OCC.Core.BRepMesh import BRepMesh_BaseMeshAlgo
from OCC.Core.BRepMeshData import BRepMeshData_PCurve
from OCC.Core.MeshVS import MeshVS_Array1OfSequenceOfInteger
from OCC.Core.IMeshTools import IMeshTools_Context
from OCC.Core.IMeshData import IMeshData_Failure
from OCC.Core.RWMesh import RWMesh_CafReader
from OCC.Core.XBRepMesh import xbrepmesh

if __name__ == "__main__":
    mat = math_Matrix(1, 10, 1, 10, 0.0)
    print(mat)
