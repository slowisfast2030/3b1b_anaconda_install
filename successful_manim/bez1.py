import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class test(InteractiveScene):
    def construct(self):
        plane = NumberPlane()
        m1 = VMobject()
        m2 = VMobject()
    
        m1.add_cubic_bezier_curve(
            np.array([-2, -1, 0]),  # start of first curve
            np.array([-3, 1, 0]),
            np.array([0, 3, 0]),
            np.array([1, 3, 0]),  # end of first curve
            )
        m2.add_cubic_bezier_curve(
            np.array([1, 3, 0]),  # start of second curve
            np.array([0, 1, 0]),
            np.array([4, 3, 0]),
            np.array([4, -2, 0]),  # end of second curve
        )

        self.add(m1, m2, plane)

        dots = np.concatenate((m1.get_points(), m2.get_points()[1:]))
        print(dots)
        for dot in dots:
            self.add(Dot(dot).set_color(RED))
        self.wait()

        m3 = VMobject()
        m3.set_points(dots)
        m3.set_color(YELLOW_B)
        m3.shift(DOWN*2)
        self.add(m3)
        self.wait()

        dots = m3.get_points()
        for dot in dots:
            self.add(Dot(dot).set_color(YELLOW_B))
        self.wait()