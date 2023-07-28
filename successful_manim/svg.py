import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class test(Scene):
    def construct(self):
        s = SVGMobject('rabbit.svg').scale(3).set_color(TEAL_E)
        self.add(s)
        self.play(Write(s), run_time=5)
        self.wait()