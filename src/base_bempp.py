from OCCUtils.Construct import make_polygon
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
import subprocess
import tempfile
import meshio
from scipy.spatial import ConvexHull, Delaunay
from linecache import getline, clearcache
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from src.base import plot2d, plot3d
from src.base_occ import dispocc

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)
logging.getLogger('numba').setLevel(logging.ERROR)
logging.getLogger('bempp').setLevel(logging.ERROR)

# pip install meshio[all]
import bempp.api

from PyQt5.QtWidgets import QApplication, qApp
from PyQt5.QtWidgets import QDialog, QCheckBox
from PyQt5.QtWidgets import QFileDialog
# pip install PyQt5

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRep import BRep_Builder, BRep_Tool
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_SOLID, TopAbs_VERTEX, TopAbs_SHAPE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound, topods_Face


def bempp_triangle_grid(comp=TopoDS_Shape(), isR=0.1, thA=0.1):
    # Mesh the shape
    BRepMesh_IncrementalMesh(comp, isR, True, thA, True)
    bild1 = BRep_Builder()
    bt = BRep_Tool()
    ex = TopExp_Explorer(comp, TopAbs_FACE)
    sl = TopExp_Explorer(comp, TopAbs_SOLID)
    print(sl.Depth())
    vertices = []
    elements = []
    while ex.More():
        face = topods_Face(ex.Current())
        location = TopLoc_Location()
        facing = bt.Triangulation(face, location)
        tab = facing.Nodes()
        tri = facing.Triangles()
        print(facing.This(), facing.NbTriangles(), facing.NbNodes())
        for i in range(1, facing.NbNodes() + 1):
            v = tab.Value(i)
            vertices.append([v.X(), v.Y(), v.Z()])
        for i in range(1, facing.NbTriangles() + 1):
            trian = tri.Value(i)
            index1, index2, index3 = trian.Get()
            elements.append([index1, index2, index3])
            # for j in range(1, 4):
            #    if j == 1:
            #        m = index1
            #        n = index2
            #    elif j == 2:
            #        n = index3
            #    elif j == 3:
            #        m = index2
            #    me = BRepBuilderAPI_MakeEdge(tab.Value(m), tab.Value(n))
        ex.Next()
    vertices = np.array(vertices).T
    elements = np.array(elements).T
    return bempp.api.Grid(vertices, elements)


class plotBEM (plot2d, dispocc):

    def __init__(self, disp=True, touch=True):
        plot2d.__init__(self)
        dispocc.__init__(self, disp=disp, touch=touch)
        self.grid = self.reference_triangle()

        self.add_function("Mesh", self.import_mshfile)

    def show_msh(self):
        build = BRep_Builder()
        comp1 = TopoDS_Compound()
        build.MakeCompound(comp1)

    def import_mshfile(self):
        options = QFileDialog.Options()
        mshfile, _ = QFileDialog.getOpenFileName(self.wi, 'QFileDialog.getOpenFileName()', '',
                                                 'CAD files (*.msh *.stl *.vtu)',
                                                 options=options)

        # Abaqus (.inp), ANSYS msh (.msh), AVS-UCD (.avs),
        # CGNS (.cgns), DOLFIN XML (.xml), Exodus (.e, .exo),
        # FLAC3D (.f3grid), H5M (.h5m), Kratos/MDPA (.mdpa),
        # Medit (.mesh, .meshb), MED/Salome (.med),
        # Nastran (bulk data, .bdf, .fem, .nas),
        # Netgen (.vol, .vol.gz),
        # Neuroglancer precomputed format,
        # Gmsh (format versions 2.2, 4.0, and 4.1, .msh),
        # OBJ (.obj), OFF (.off),
        # PERMAS (.post, .post.gz, .dato, .dato.gz),
        # PLY (.ply), STL (.stl), Tecplot .dat,
        # TetGen .node/.ele, SVG (2D output only) (.svg), SU2 (.su2),
        # UGRID (.ugrid), VTK (.vtk), VTU (.vtu), WKT (TIN) (.wkt),
        # XDMF (.xdmf, .xmf).

        #self.grid = bempp.api.import_grid(mshfile)
        mesh = meshio.read(mshfile)

        build = BRep_Builder()
        comp1 = TopoDS_Compound()
        build.MakeCompound(comp1)
        for num in mesh.cells_dict["triangle"]:
            print(num)
            pts = [gp_Pnt(*mesh.points[i]) for i in num]
            build.Add(comp1, make_polygon(pts, closed=True))
        self.display.DisplayShape(comp1)

    def reference_triangle(self):
        """Return a grid consisting of only the reference triangle."""

        vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]).T
        elements = np.array([[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]).T
        return bempp.api.Grid(vertices, elements)

    def __generate_grid_from_geo_string(self, geo_string):
        """Create a grid from a gmsh geo string."""

        def msh_from_string(geo_string):
            """Create a mesh from a string."""
            gmsh_command = bempp.api.GMSH_PATH
            if gmsh_command is None:
                raise RuntimeError("Gmsh is not found. Cannot generate mesh")
            f, geo_name, msh_name = self.get_gmsh_file()
            f.write(geo_string)
            f.close()

            fnull = open(os.devnull, "w")
            cmd = gmsh_command + " -2 " + geo_name + " -format msh2"
            try:
                subprocess.check_call(
                    cmd, shell=True, stdout=fnull, stderr=fnull)
            except:
                print("The following command failed: " + cmd)
                fnull.close()
                raise
            # os.remove(geo_name)
            fnull.close()
            # self.open_filemanager(geo_name)
            return msh_name

        msh_name = msh_from_string(geo_string)
        grid = bempp.api.import_grid(msh_name)
        # os.remove(msh_name)
        # self.open_filemanager(msh_name)
        return grid

    def get_gmsh_file(self):
        """
        Create a new temporary gmsh file.

        Return a 3-tuple (geo_file,geo_name,msh_name), where
        geo_file is a file descriptor to an empty .geo file, geo_name is
        the corresponding filename and msh_name is the name of the
        Gmsh .msh file that will be generated.

        """

        geo, geo_name = tempfile.mkstemp(
            suffix=".geo", dir=self.tmpdir, text=True)
        geo_file = os.fdopen(geo, "w")
        msh_name = os.path.splitext(geo_name)[0] + ".msh"
        return (geo_file, geo_name, msh_name)

    def export_bempp_msh(self):
        bempp.api.export(self.tempname + ".msh", self.grid, write_binary=False)

    def convex_3d(self):
        self.new_3Dfig()

        self.axs.scatter(
            self.grid.vertices[0, :],
            self.grid.vertices[1, :],
            self.grid.vertices[2, :],
            s=0.5
        )
        self.SavePng(self.tempname + "_pnt.png")

        for idx in range(self.grid.edges.shape[1]):
            xi = self.grid.vertices[:, self.grid.edges[0, idx]]
            yi = self.grid.vertices[:, self.grid.edges[1, idx]]
            self.axs.plot([xi[0], yi[0]], [xi[1], yi[1]],
                          [xi[2], yi[2]], "k", lw=0.5)
        self.SavePng(self.tempname + "_edg.png")


if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    obj = plotBEM()
    obj.show()
    #bempp.api.export(obj.tempname + ".msh", obj.grid, write_binary=False)
    # obj.convex_3d()

    # meshio-convert    input.msh output.vtk   # convert between two formats
    # 
    # meshio-info       input.xdmf             # show some info about the mesh
    #
    # meshio-compress   input.vtu              # compress the mesh file
    # meshio-decompress input.vtu              # decompress the mesh file
    #
    # meshio-binary     input.msh              # convert to binary format
    # meshio-ascii      input.msh              # convert to ASCII format
