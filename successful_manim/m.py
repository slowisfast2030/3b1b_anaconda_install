import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class test(Scene):
    def construct(self):
        m = Matrix(matrix = np.ones((3, 4)))
        self.add(m)
        self.wait()