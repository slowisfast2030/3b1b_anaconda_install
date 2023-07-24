import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *


# 同时运动
class test1(InteractiveScene):
    def construct(self):
        dot1 = Dot(color=RED)
        dot2 = Dot(color=BLUE)
        dot3 = Dot(color=GREEN)

        self.play(
            AnimationGroup(
                dot1.animate.shift(LEFT),
                dot2.animate.shift(RIGHT),
                dot3.animate.shift(UP)
            )
        )

        self.wait()

# 依次运动，一个结束后再运动下一个
class test2(InteractiveScene):
    def construct(self):
        dot1 = Dot(color=RED)
        dot2 = Dot(color=BLUE)
        dot3 = Dot(color=GREEN)

        self.play(
            Succession(
                dot1.animate.shift(LEFT),
                dot2.animate.shift(RIGHT),
                dot3.animate.shift(UP)
            )
        )

        self.wait()

# 依次运动，一个结束前就运动下一个
class test3(InteractiveScene):
    def construct(self):
        dot1 = Dot(color=RED)
        dot2 = Dot(color=BLUE)
        dot3 = Dot(color=GREEN)

        self.play(
            LaggedStart(
                dot1.animate.shift(LEFT),
                dot2.animate.shift(RIGHT),
                dot3.animate.shift(UP),
                lag_ratio = 0.2
            )
        )

        self.wait()