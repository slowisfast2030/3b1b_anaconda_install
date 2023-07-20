import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class test(InteractiveScene):
    def construct(self):
        p = NumberPlane()
        self.add(p)

        a = Arc().scale(5)
        self.add(a)
        self.wait()
        print("\n", "="*100)
        print(a.tip_config)

        points = a.get_points()
        for point in points:
            self.add(Dot(point).scale(0.5).set_color(RED))
        self.wait()
        print("\n", "="*100)
        print(len(points))

        self.add(CurvedArrow(points[0], points[-2]))
        self.wait()
