import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class test(InteractiveScene):
    def construct(self):
        plane = NumberPlane()
        m = VMobject()
        m.add_cubic_bezier_curve(
            np.array([-2, -1, 0]),  # start of first curve
            np.array([-3, 1, 0]),
            np.array([0, 3, 0]),
            np.array([1, 3, 0])
            )
        self.add(m, plane)

        # 本来以为m的点都在曲线上，结果发现不是
        dots = m.get_points()
        print(dots)
        for dot in dots:
            self.add(Dot(dot))
        self.wait()
