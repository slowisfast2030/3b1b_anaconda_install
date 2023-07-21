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


class Interpolate(InteractiveScene):
    def construct(self):
        c = Circle()
        s = Square()
        m = VMobject()
        mm = m.interpolate(c, s, 0.5)
        self.add(mm)
        self.wait()
