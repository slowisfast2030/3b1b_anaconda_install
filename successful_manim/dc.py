import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class test(Scene):
    def construct(self):
        points = np.random.randn(10, 3) 
        dc = DotCloud(points, glow_factor=0, color=TEAL, radius=1)
        dc = dc.make_3d()
        self.play(ShowCreation(dc))
        self.wait()