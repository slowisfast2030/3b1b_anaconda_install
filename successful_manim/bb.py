import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *


class test(InteractiveScene):
    def construct(self):
        c = Circle()
        self.add(c)
        bb = c.compute_bounding_box()
        print("+"*100, "\n", bb)

        all_points = np.vstack([
            c.get_points()])
        # print(all_points.min(0))
        # print(all_points.max(0))
        print("-"*100, "\n", all_points)

        for point in bb:
            dot = Dot(point)
            self.add(dot)
        self.wait() 
