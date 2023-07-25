import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *
import numpy as np

class TextExample(Scene):
    def construct(self):
        # To run this scene properly, you should have "Consolas" font in your computer
        # for full usage, you can see https://github.com/3b1b/manim/pull/680
        text = Text("slow", font="Consolas", font_size=90)
        print("-_"*200)
        print(len(text))
        s = text[0]
        self.add(text)
        self.wait(3)