import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mp_colors
import pymap3d
import math
import random
import sys
import os
from linecache import getline, clearcache
from optparse import OptionParser

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCCUtils.Construct import make_face, make_polygon

sys.path.append(os.path.join("../"))
from base import plot2d, plot3d
from base_occ import dispocc
from src import japanmap

DEG2RAD = math.pi / 180.0

# pip install pymap3d
# pip install japanmap
#
# https://github.com/nagitausu/misc.git
# https://tjkendev.github.io/procon-library/python/convex_hull_trick/deque.html


def cross3(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def convex_hull(ps):
    qs = []
    N = len(ps)
    for p in ps:
        while len(qs) > 1 and cross3(qs[-1], qs[-2], p) > 0:
            qs.pop()
        qs.append(p)
    t = len(qs)
    for i in range(N - 2, -1, -1):
        p = ps[i]
        while len(qs) > t and cross3(qs[-1], qs[-2], p) > 0:
            qs.pop()
        qs.append(p)
    return qs


def calc_area(ps):
    ret = 0.0
    for (x0, y0), (x1, y1) in zip(ps, ps[1:]):
        ret += x0 * y1 - x1 * y0
    ret *= 0.5
    return ret


if __name__ == '__main__':
    argvs = sys.argv
    parser = OptionParser()
    parser.add_option("--dir", dest="dir", default="./")
    parser.add_option("--pxyz", dest="pxyz",
                      default=[0.0, 0.0, 0.0], type="float", nargs=3)
    opt, argc = parser.parse_args(argvs)
    print(opt, argc)

    obj = dispocc(touch=True)

    qpqo = japanmap.get_data(rough=False)
    pnts = japanmap.pref_points(qpqo)

    # We don't have to care for presice scalling
    lat0 = pnts[20][0][1] * DEG2RAD
    lon0 = pnts[20][0][0] * DEG2RAD

    ranking = []
    for i in range(47):
        xy = []
        enus = []
        for lon, lat in pnts[i]:
            lat *= DEG2RAD
            lon *= DEG2RAD
            e, n, u = pymap3d.geodetic2enu(lat, lon, 0.0, lat0, lon0, 0.0)
            # values have to be distinct
            enus.append([e + random.random(), n + random.random()])
            xy.append(np.array([e, n, 0]))
        xy = np.array(xy)
        pts = [gp_Pnt(*xyz) for xyz in xy]
        rim = make_polygon(pts, closed=True)
        fce = make_face(rim, True)
        print(japanmap.pref_names[i + 1])
        obj.display.DisplayShape(rim)
        obj.display.DisplayShape(fce)

    obj.show()
