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

from OCC.Core.IntWalk import IntWalk_ArretSurPoint

if __name__ == "__main__":
    mat = math_Matrix(1, 4, 1, 4, 0.0)
    mat.SetValue(1, 1, 1)
    mat.SetValue(2, 2, 1)
    mat.SetValue(3, 3, 1)
    mat.SetValue(3, 4, 1)
    mat.SetValue(4, 4, 0.5)
    print(mat, mat.Determinant())
