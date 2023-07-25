import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class Text(Scene):
    def construct(self):
        tex = ["=",
                "0.0000"]
        result = VGroup(*Tex(*tex))
        self.add(result)
        self.wait(3)