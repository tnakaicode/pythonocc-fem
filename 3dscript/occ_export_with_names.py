from OCC.Core.IFSelect import IFSelect_RetError
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.STEPConstruct import stepconstruct_FindEntity
from OCC.Core.STEPControl import (STEPControl_AsIs, STEPControl_Writer)
from OCC.Core.TCollection import TCollection_HAsciiString
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Extend.DataExchange import read_step_file_with_names_colors, read_iges_file


"""
This script demonstrates loading 2d cross-section from iges which can be crated from 2d cad program like autocad.
"""


def get_direction_of_wire(wire):
    """
    A method to detect 2d wire orientation is clockwise or counterclockwise.
    For counterclockwise it should be +z.
    For clockwise it should be -z.
    :param wire: Wire to be investigating
    :return: direction of the normal of wire
    """
    make_face_wire = BRepBuilderAPI_MakeFace(wire)
    make_face_wire.Build()
    surface_wire = BRepAdaptor_Surface(make_face_wire.Shape())
    plane_wire = surface_wire.Plane()
    plane_wire_normal = plane_wire.Axis().Direction()
    return plane_wire_normal


def load_section_from_iges(file):
    """
    A method to create a face entity to be extruded to solid or mesh from iges file

    In 2D drawings all wires should be joint and they should be polyline or composite curve.

    Method firstly calculate bbox of all wires and detect outer wire which have the largest diagonal of bbox.
    Other wires are inner wires.

    After that, orientation of the outer wire should be counterclockwise so check the normal reverse it
    if normal is not upward.
    Orientation of inner wire should be clockwise so check the normals and reverse wire if normal is not downward.

    :param file: Iges file to load
    :return: closed face with inner holes
    """
    data = read_iges_file(file)
    topo_explorer = TopologyExplorer(data)
    wires = list(topo_explorer.wires())

    wire_dict = {'outer': None, 'inner': None}

    bbox_max = 0.0
    index_max = 0
    for i, wire in enumerate(wires):
        bbox = Bnd_Box()
        bbox.SetGap(1e-6)
        brepbndlib_Add(wire, bbox)
        diagonal = bbox.SquareExtent()
        if diagonal > bbox_max:
            bbox_max = diagonal
            index_max = i
    wire_dict['outer'] = wires[index_max]
    wires.pop(index_max)
    wire_dict['inner'] = wires

    plane_outer_normal = get_direction_of_wire(wire_dict['outer'])

    if plane_outer_normal.Z() < 0:
        wire_dict['outer'].Reverse()
    make_face = BRepBuilderAPI_MakeFace(wire_dict['outer'])

    for wire_inner in wire_dict['inner']:
        plane_inner_normal = get_direction_of_wire(wire_inner)
        if plane_inner_normal.Z() > 0:
            wire_inner.Reverse()
        make_face.Add(wire_inner)

    make_face.Build()
    return make_face.Shape()


schema = 'AP203'
assembly_mode = 1

writer = STEPControl_Writer()
fp = writer.WS().TransferWriter().FinderProcess()
Interface_Static_SetCVal('write.step.schema', schema)
Interface_Static_SetCVal('write.step.unit', 'M')
Interface_Static_SetCVal('write.step.assembly', str(assembly_mode))

my_box1 = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()
my_box2 = BRepPrimAPI_MakeBox(20., 1., 30.).Shape()

components = [my_box1, my_box2]
comp_names = ['PartA', 'PartB']
for i, comp in enumerate(components):
    Interface_Static_SetCVal('write.step.product.name', comp_names[i])
    status = writer.Transfer(comp, STEPControl_AsIs)
    if int(status) > int(IFSelect_RetError):
        raise Exception('Some Error occurred')

    # This portion is not working as I hoped
    item = stepconstruct_FindEntity(fp, comp)
    if not item:
        raise Exception('Item not found')

    item.SetName(TCollection_HAsciiString(comp_names[i]))

status = writer.Write('./occ_export_with_names.stp')
if int(status) > int(IFSelect_RetError):
    raise Exception('Something bad happened')

# read_step_file_with_names_colors('my_stepfile.stp')
