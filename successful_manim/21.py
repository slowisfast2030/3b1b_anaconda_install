import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *


class test(InteractiveScene):
    def construct(self):
        c = Circle()
        s = Square()
        self.add(c)
        self.play(Transform(c, s))
        self.wait()


class temp(InteractiveScene):
    def construct(self):
        c = Circle()
        s = Square()
        #m = Mobject()
        c.interpolate(c, s, 0)
        #self.add(m)
        self.wait()

class test2(InteractiveScene):
    def construct(self):
        c = Circle()
        self.play(DrawBorderThenFill(c))
        self.wait()