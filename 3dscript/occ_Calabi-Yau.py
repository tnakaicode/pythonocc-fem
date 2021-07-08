import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from optparse import OptionParser

sys.path.append(os.path.join("../"))
from base_occ import dispocc

import logging
logging.getLogger('matplotlib').setLevel(logging.ERROR)

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepMesh import BRepMesh_Triangle

if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--nm", dest="nm", default=[6, 10], type="int", nargs=2)
    parser.add_option("--alpha", dest="alpha",
                      default=0.5, type="float")
    parser.add_option("--coeff", dest="coeff",
                      default=[1.0, 1.0], type="float", nargs=2)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    obj = dispocc(touch=True)

    #
    # $z_1^n + z_2^n = 1$
    #
    # z_1 = e^{i\phi_1} [ \cos(x + iy) ]^{n/2}
    # z_2 = e^{i\phi_2} [ \sin(x + iy) ]^{n/2}
    #

    n = opt.nm[0]
    phi1 = np.linspace(0, 1, n + 1)[:-1] * 2 * np.pi
    phi2 = np.linspace(0, 1, n + 1)[:-1] * 2 * np.pi
    print(phi1)

    m = opt.nm[1]
    px = np.linspace(0, 1, m) * np.pi / 2
    py = np.linspace(-1, 1, m) * np.pi / 2
    mesh = np.meshgrid(px, py)

    alph = opt.alpha * 2 * np.pi
    c1, c2 = opt.coeff

    #indx = 2
    #z1 = np.exp(1j * phi1[indx]) * np.cos(mesh[0] + 1j * mesh[1])**(n / 2)
    #z2 = np.exp(1j * phi1[indx]) * np.sin(mesh[0] + 1j * mesh[1])**(n / 2)
    #x = np.real(z1)
    #y = np.real(z2)
    #z = np.imag(z1) * np.cos(alph) + np.imag(z2) * np.sin(alph)
    # plt2d.contourf_sub(
    #    mesh, x, pngname=plt2d.tempname + "_x.png")
    # plt2d.contourf_sub(
    #    mesh, y, pngname=plt2d.tempname + "_y.png")
    # plt2d.contourf_sub(
    #    mesh, z, pngname=plt2d.tempname + "_z.png")

    for idx1, ph1 in enumerate(phi1):
        for idx2, ph2 in enumerate(phi2):
            z1 = np.exp(1j * ph1) * \
                np.cos(mesh[0] / c1 + 1j * mesh[1] / c2)**(n / 2)
            z2 = np.exp(1j * ph2) * \
                np.sin(mesh[0] / c1 + 1j * mesh[1] / c2)**(n / 2)
            x = np.real(z1)
            y = np.real(z2)
            z = np.imag(z1) * np.cos(alph) + np.imag(z2) * np.sin(alph)
            #face = spl_face(x, y,z)
            # print(face)
            # obj.display.DisplayShape(face)
            for idx, val in np.ndenumerate(x):
                pnt = gp_Pnt(x[idx], y[idx], z[idx])
                obj.display.DisplayShape(pnt)
    obj.show()
