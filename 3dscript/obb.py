from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir, gp_XYZ

from OCC.Core.Bnd import Bnd_OBB
from OCC.Core.GProp import GProp_GProps

from OCC.Core.BRep import BRep_Builder, BRep_Tool
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRepBndLib import brepbndlib_AddOBB
from OCC.Core.BRepGProp import brepgprop_VolumeProperties

from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import TopoDS_Compound, topods_Face
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopLoc import TopLoc_Location

from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.IMeshData import IMeshData_Curve
#from OCC.Core.IMeshTools import IMeshData_Curve
from OCC.Core.MeshVS import MeshVS_Buffer
from OCC.Core.RWMesh import RWMesh_CoordinateSystem
from OCC.Core.XBRepMesh import xbrepmesh

from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer

# For Bounding Box line and transparency modification
from OCC.Core.AIS import AIS_Shape


display, start_display, add_menu, add_function_to_menu = init_display()
display.SetSelectionModeVertex()

# ======================================================================================


def MinimumBBox(filepath):
    shape = read_step_file(filepath)
    display.DisplayShape(shape)

    obb = Bnd_OBB()

    # We call the mesh function to obtain the vertices point cloud
    VerticesContainer = simple_mesh(shape, extractionMode="vertices")

    # ---------------------------------------------------------------------------------
    nbMeshedSurface = len(VerticesContainer)
    # ITERATION OVER ALL FACES OF THE MESH
    for surface in range(nbMeshedSurface):
        vertices = VerticesContainer[surface]
        nbVerticesFace = len(vertices)

        # FOR EACH FACES WE COLLECT VERTICES
        for i in range(nbVerticesFace):
            print(vertices[i])
            p = BRepBuilderAPI_MakeVertex(vertices[i]).Shape()
            # Vertex transfer to the oriented bounding box
            brepbndlib_AddOBB(p, obb)
            display.DisplayShape(vertices[i])
    # ---------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------
    def _ConvertBndToShape(theBox):

        # -----------------------------------------------------------------------------
        aBaryCenter = theBox.Center()
        aXDir = theBox.XDirection()
        aYDir = theBox.YDirection()
        aZDir = theBox.ZDirection()
        aHalfX = theBox.XHSize()
        aHalfY = theBox.YHSize()
        aHalfZ = theBox.ZHSize()

        ax = gp_XYZ(aXDir.X(), aXDir.Y(), aXDir.Z())
        ay = gp_XYZ(aYDir.X(), aYDir.Y(), aYDir.Z())
        az = gp_XYZ(aZDir.X(), aZDir.Y(), aZDir.Z())
        p = gp_Pnt(aBaryCenter.X(), aBaryCenter.Y(), aBaryCenter.Z())
        anAxes = gp_Ax2(p, gp_Dir(aZDir), gp_Dir(aXDir))
        anAxes.SetLocation(
            gp_Pnt(p.XYZ() - ax * aHalfX - ay * aHalfY - az * aHalfZ))
        aBox = BRepPrimAPI_MakeBox(
            anAxes, 2.0 * aHalfX, 2.0 * aHalfY, 2.0 * aHalfZ).Shape()
        # -----------------------------------------------------------------------------

        # VOLUME COMPUTATION
        props = GProp_GProps()
        brepgprop_VolumeProperties(aBox, props)
        # Get inertia properties
        volume = props.Mass()
        print(f"The Minimal Bounding Box Volume is: {volume}mm3")

        # Bounding box appearance modification
        ais_shp = AIS_Shape(aBox)
        ais_shp.SetWidth(4)
        ais_shp.SetTransparency(0.60)

        # Bounding box display
        ais_context = display.GetContext()
        ais_context.Display(ais_shp, True)

        return ais_shp

    # We Call the Oriented Bounding Box Function
    _ConvertBndToShape(obb)

    display.FitAll()
    start_display()


# ======================================================================================
def simple_mesh(shape, extractionMode):
    VerticesContainer = []

    model = TopologyExplorer(shape)

    # ---------------
    # Mesh the shape
    # ---------------
    deflection = 0.6
    BRepMesh_IncrementalMesh(shape, deflection)
    builder = BRep_Builder()
    comp = TopoDS_Compound()
    builder.MakeCompound(comp)

    bt = BRep_Tool()
    ex = TopExp_Explorer(shape, TopAbs_FACE)

    if extractionMode == "vertices":

        while ex.More():
            face = topods_Face(ex.Current())
            location = TopLoc_Location()
            facing = bt.Triangulation(face, location)
            vertices = facing.Nodes()
            #tri = facing.Triangles()

            # We populate the list VerticesContainer
            VerticesContainer.append(vertices)

            ex.Next()
    return VerticesContainer


if __name__ == '__main__':
    MinimumBBox("./as1_pe_203.stp")

    # cube4.STEP
    # Di Pietro Motor V2_STEP.stp
    # Fixation de Ski.stp
    # Stabilisateur Reflex -3Kg.stp
    # Ensemble Circuit Puissance.stp
