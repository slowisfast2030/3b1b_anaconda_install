import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class test(Scene):
    def construct(self):
        so = Speedometer()
        lp = Laptop().shift(4*LEFT)
        cl = Clock().shift(4*RIGHT)
        cm = Checkmark().shift(2*DL)
        em = Exmark().shift(2*DR)
        # p = Piano().shift(2*UP)
        # p3 = Piano3D().shift(2*DOWN)
        df = DieFace(6).shift(2*UR)

        self.add(so, lp, cl, cm, em, df)
        self.wait()

        self.play(ClockPassesTime(cl))