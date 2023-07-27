import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class test(Scene):
    def construct(self):
        code = '''
                from manim import Scene, Square

                class FadeInSquare(Scene):
                    def construct(self):
                        s = Square()
                        self.play(FadeIn(s))
                        self.play(s.animate.scale(2))
                        self.wait()
                '''
        self.add(Code(code))
        self.wait()
