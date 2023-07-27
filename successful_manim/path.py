import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class test(InteractiveScene):
    def construct(self):
        c = GlowDot()
        self.add(c)
        p = TracedPath(c.get_center, stroke_color=TEAL, time_traced=1)
        
        #p = TracingTail(c.get_center, stroke_color=RED)

        self.add(p)

        self.play(c.animate.shift(200 * RIGHT), run_time=20)
