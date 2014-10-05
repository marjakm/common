import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from track_coordinates import inner, outer

class Track(object):

    def __init__(self):
        self.inner_path = Path(inner)
        self.outer_path = Path(outer)

        self.lines = list()
        for arr in (inner, outer):
            for i in range(len(arr)-1):
                self.lines.append(self.get_line_from_two_points(arr[i], arr[i+1]))

    def get_line_from_two_points(self, p1, p2):
        pa,pb = (p1,p2) if p1[0]<p2[0] else (p2,p1)
        a = (pb[1]-pa[1])/(pb[0]-pa[0])
        c = pa[1]-a*pa[0]
        return a, c, pa[0], pb[0]

    def contains(self, points, edges):
        res = True
        for name,point in points.items():
            if self.inner_path.contains_point(point):
                res = False
                print("Point {} iside inner track boundary".format(name))
            elif not self.outer_path.contains_point(point):
                res = False
                print("Point {} outside outer track boundary".format(name))

        for name,edge in edges.items():
            p = Path(edge, [Path.MOVETO, Path.LINETO])
            for k,v in (('inner',self.inner_path),('outer',self.outer_path)):
                if v.intersects_path(p, filled=False):
                    res = False
                    print("Edge {} intersects {} track boundary".format(name,k))
        return res

    def plot(self):
        fig, ax = plt.subplots()
        ax.add_patch(PathPatch(self.outer_path, facecolor='k', alpha=0.8))
        ax.add_patch(PathPatch(self.inner_path, facecolor='w', alpha=0.9))
        ax.grid(which='both')
        ax.axis('equal')
        ax.set_ylabel("Y (cm)")
        ax.set_xlabel("X (cm)")
        plt.show()

if __name__ == "__main__":
    t = Track()
    t.plot()