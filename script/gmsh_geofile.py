import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from scipy.spatial import ConvexHull, Delaunay
from linecache import getline, clearcache
from optparse import OptionParser

import bempp.api

sys.path.append(os.path.join("../"))
from base import plot2d, plot3d
from base_occ import dispocc

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)


class plotBEM (plot2d):

    def __init__(self):
        plot2d.__init__(self)
        self.k = 15.
        self.grid = self.reference_triangle()

    def reference_triangle(self):
        """Return a grid consisting of only the reference triangle."""

        vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]).T
        elements = np.array([[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]).T
        return bempp.api.Grid(vertices, elements)

    def multitrace_cube(self, h=0.1):
        """
        Definitition of a cube with an interface at z=.5.

        The normal direction at the interface shows into the
        positive z-direction and has the domain index
        and has the domain index 11. The lower half of the cube
        is given through the segments [1, 2, 3, 4, 5, 6]. The
        top half of the cube is defined by the segments
        [6, 7, 8, 9, 10, 11]. For the upper half the normal
        direction of segment 6 shows in the interior of the domain.
        """
        stub = """
        Point(1) = {0, 0.0, 0, cl};
        Point(2) = {1, 0, 0, cl};
        Point(3) = {1, 1, 0, cl};
        Point(4) = {0, 1, 0, cl};
        Point(5) = {1, 0, 1, cl};
        Point(6) = {0, 1, 1, cl};
        Point(7) = {1, 1, 1, cl};
        Point(8) = {0, 0, 1, cl};
        Point(9) = {1, 0, .5, cl};
        Point(10) = {0, 1, .5, cl};
        Point(11) = {1, 1, .5, cl};
        Point(12) = {0, 0, .5, cl};
        Line(1) = {8, 5};
        Line(3) = {2, 1};
        Line(5) = {6, 7};
        Line(7) = {3, 4};
        Line(9) = {7, 5};
        Line(10) = {6, 8};
        Line(11) = {3, 2};
        Line(12) = {4, 1};
        Line(13) = {12, 9};
        Line(14) = {9, 11};
        Line(15) = {11, 10};
        Line(16) = {10, 12};
        Line(17) = {2, 9};
        Line(18) = {3, 11};
        Line(19) = {11, 7};
        Line(20) = {9, 5};
        Line(21) = {4, 10};
        Line(22) = {1, 12};
        Line(23) = {12, 8};
        Line(24) = {10, 6};
        Line Loop(1) = {3, -12, -7, 11};
        Plane Surface(1) = {1};
        Line Loop(3) = {14, 19, 9, -20};
        Plane Surface(3) = {3};
        Line Loop(4) = {13, 20, -1, -23};
        Plane Surface(4) = {4};
        Line Loop(6) = {12, 22, -16, -21};
        Plane Surface(6) = {6};
        Line Loop(7) = {16, 23, -10, -24};
        Plane Surface(7) = {7};
        Line Loop(9) = {7, 21, -15, -18};
        Plane Surface(9) = {9};
        Line Loop(10) = {15, 24, 5, -19};
        Plane Surface(10) = {10};
        Line Loop(11) = {16, 13, 14, 15};
        Plane Surface(11) = {11};
        Line Loop(12) = {1, -9, -5, 10};
        Plane Surface(12) = {12};
        Line Loop(13) = {-3, 17, -13, -22};
        Plane Surface(13) = {13};
        Line Loop(14) = {-11, 18, -14, -17};
        Plane Surface(14) = {14};
        Physical Surface(1) = {6};
        Physical Surface(2) = {13};
        Physical Surface(3) = {14};
        Physical Surface(4) = {9};
        Physical Surface(5) = {1};
        Physical Surface(6) = {11};
        Physical Surface(7) = {3};
        Physical Surface(8) = {10};
        Physical Surface(9) = {7};
        Physical Surface(10) = {4};
        Physical Surface(11) = {12};
        """
        geometry = "cl = " + str(h) + ";\n" + stub
        return self.__generate_grid_from_geo_string(geometry)

    def cuboid(self, length=(1, 1, 1), origin=(0, 0, 0), h=0.1):
        """
        Return a cuboid mesh.

        Parameters
        ----------
        length : tuple
            Side lengths of the cube.
        origin : tuple
            Coordinates of the origin (bottom left corner)
        h : float
            Element size.

        """
        cuboid_stub = """
        Point(1) = {orig0,orig1,orig2,cl};
        Point(2) = {orig0+l0,orig1,orig2,cl};
        Point(3) = {orig0+l0,orig1+l1,orig2,cl};
        Point(4) = {orig0,orig1+l1,orig2,cl};
        Point(5) = {orig0,orig1,orig2+l2,cl};
        Point(6) = {orig0+l0,orig1,orig2+l2,cl};
        Point(7) = {orig0+l0,orig1+l1,orig2+l2,cl};
        Point(8) = {orig0,orig1+l1,orig2+l2,cl};

        Line(1) = {1,2};
        Line(2) = {2,3};
        Line(3) = {3,4};
        Line(4) = {4,1};
        Line(5) = {1,5};
        Line(6) = {2,6};
        Line(7) = {3,7};
        Line(8) = {4,8};
        Line(9) = {5,6};
        Line(10) = {6,7};
        Line(11) = {7,8};
        Line(12) = {8,5};

        Line Loop(1) = {-1,-4,-3,-2};
        Line Loop(2) = {1,6,-9,-5};
        Line Loop(3) = {2,7,-10,-6};
        Line Loop(4) = {3,8,-11,-7};
        Line Loop(5) = {4,5,-12,-8};
        Line Loop(6) = {9,10,11,12};

        Plane Surface(1) = {1};
        Plane Surface(2) = {2};
        Plane Surface(3) = {3};
        Plane Surface(4) = {4};
        Plane Surface(5) = {5};
        Plane Surface(6) = {6};

        Physical Surface(1) = {1};
        Physical Surface(2) = {2};
        Physical Surface(3) = {3};
        Physical Surface(4) = {4};
        Physical Surface(5) = {5};
        Physical Surface(6) = {6};

        Surface Loop (1) = {1,2,3,4,5,6};

        Volume (1) = {1};

        Mesh.Algorithm = 6;
        """

        cuboid_geometry = (
            "l0 = "
            + str(length[0])
            + ";\n"
            + "l1 = "
            + str(length[1])
            + ";\n"
            + "l2 = "
            + str(length[2])
            + ";\n"
            + "orig0 = "
            + str(origin[0])
            + ";\n"
            + "orig1 = "
            + str(origin[1])
            + ";\n"
            + "orig2 = "
            + str(origin[2])
            + ";\n"
            + "cl = "
            + str(h)
            + ";\n"
            + cuboid_stub
        )

        return self.__generate_grid_from_geo_string(cuboid_geometry)

    def __generate_grid_from_geo_string(self, geo_string):
        """Create a grid from a gmsh geo string."""
        import os
        import subprocess
        import bempp.api

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
        import os
        import tempfile

        geo, geo_name = tempfile.mkstemp(
            suffix=".geo", dir=self.tmpdir, text=True)
        geo_file = os.fdopen(geo, "w")
        msh_name = os.path.splitext(geo_name)[0] + ".msh"
        return (geo_file, geo_name, msh_name)

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


@bempp.api.complex_callable
def combined_data(x, n, domain_index, result):
    result[0] = 1j * 15 * np.exp(1j * 15 * x[0]) * (n[0] - 1)


if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    obj = plotBEM()
    bempp.api.export(obj.tempname + ".msh", obj.grid)
    obj.convex_3d()

    piecewise_const_space = bempp.api.function_space(obj.grid, "DP", 0)

    identity = bempp.api.operators.boundary.sparse.identity(
        piecewise_const_space, piecewise_const_space, piecewise_const_space)
    adlp = bempp.api.operators.boundary.helmholtz.adjoint_double_layer(
        piecewise_const_space, piecewise_const_space, piecewise_const_space, obj.k)
    slp = bempp.api.operators.boundary.helmholtz.single_layer(
        piecewise_const_space, piecewise_const_space, piecewise_const_space, obj.k)
    lhs = 0.5 * identity + adlp - 1j * obj.k * slp

    grid_fun = bempp.api.GridFunction(piecewise_const_space, fun=combined_data)

    neumann_fun, info = bempp.api.linalg.gmres(lhs, grid_fun, tol=1E-5)

    print(obj.grid.element_to_element_matrix)
    print(obj.grid)
