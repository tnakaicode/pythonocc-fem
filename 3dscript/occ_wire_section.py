import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from linecache import getline, clearcache
from optparse import OptionParser

basename = os.path.dirname(__file__)

sys.path.append(os.path.join("../"))
from base_occ import dispocc

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.gp import gp_Pln
from OCC.Core.TopExp import topexp
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Section
from OCC.Extend.ShapeFactory import get_aligned_boundingbox
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCCUtils.Topology import Topo
from OCCUtils.Construct import make_box, make_face, make_line, make_wire, make_edge
from OCCUtils.Construct import make_plane, make_polygon
from OCCUtils.Construct import point_to_vector, vector_to_point
from OCCUtils.Construct import dir_to_vec, vec_to_dir


class OCCSection(dispocc):

    def __init__(self):
        dispocc.__init__(self)

    def Space_Section(self, aShape, Elevation=0.5):
        # Intersects a plane and a space in a certain elevation and returns the result as a List of ordered points
        

        # middel of the Space coordination (zMidP), type: number
        center, dxyz, box_shp = get_aligned_boundingbox(aShape)

        # defining a (Horizontal) plane to intersect with the space shape. (z = "Elevation")
        plane = gp_Pln(center, gp_Dir(0, 0, 1))

        # intersect the plane and the space:
        section_face = BRepBuilderAPI_MakeFace(
            plane, -dxyz[0], dxyz[0], -dxyz[1], dxyz[1]).Face()
        section = BRepAlgoAPI_Section(section_face, aShape).Shape()
        #self.display.DisplayShape(section_face)
        self.display.DisplayShape(section)

        # get the edges and vertices of the intersection:
        Unordered_Edge_List = []
        Ordered_Vertex_List = []

        edges = list(TopologyExplorer(section).edges())
        #for i in range(len(edges)):
        #    firstVert = topexp.FirstVertex(edges[i])
        #    p1_edge = BRep_Tool.Pnt(firstVert)
        #    lastVert = topexp.LastVertex(edges[i])
        #    p2_edge = BRep_Tool.Pnt(lastVert)
        #    TheEdge = make_edge([p1_edge, p2_edge])
        #    Unordered_Edge_List.append(TheEdge)
#
        #if Unordered_Edge_List != []:
        #    Ordered_Vertex_List.append(Unordered_Edge_List[0][1])
#
        ## order the points (to extract a polygon from ordered points)
        #while Unordered_Edge_List:
        #    for x in Unordered_Edge_List:
        #        if Ordered_Vertex_List[-1] == x[0]:
        #            Ordered_Vertex_List.append(x[1])
        #            Unordered_Edge_List.remove(x)
#
        # #Space_polygon = Polygon(Ordered_Vertex_List)
        #return Ordered_Vertex_List


if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    obj = OCCSection()
    axs = gp_Ax3()
    
    aShape = obj.read_cadfile("./as1_pe_203.stp")
    
    obj.Space_Section(aShape)
    #wire = make_polygon(pts, closed=True)
    #obj.display.DisplayShape(wire)

    obj.show()
