import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class test(InteractiveScene):
    def construct(self):
        plane = NumberPlane()
        m = VMobject()

        points = [
            np.array([-2, -1, 0]),  # start of first curve
            np.array([-3, 1, 0]),
            np.array([0, 3, 0]),
            np.array([1, 3, 0]),  # end of first curve
            np.array([0, 1, 0]),
            np.array([4, 3, 0]),
            np.array([4, -2, 0]),  # end of second curve
            ]
        #m.set_points_as_corners(points)

        m.set_points_smoothly(points)

        self.add(m, plane)
        self.wait()

        for point in points:
            self.add(Dot(point).set_color(RED).scale(2))
        self.wait()

        for point in m.get_points():
            self.add(Dot(point).set_color(YELLOW_C))
        self.wait()