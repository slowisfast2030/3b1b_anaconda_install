import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *
from _2023.clt.main import *


class SumsOfSizeFive(TeacherStudentsScene):
    def construct(self):
        #morty = self.teacher
        #self.add(morty)
        self.teacher_says("hello")
        self.wait()

# 这一行可以正常显示svg图像：pi
class test(InteractiveScene):
    def construct(self):
        pi = PiCreature(color=BLUE_E)
        for i in range(len(pi)):
            self.add(pi[i])
            pi[i].move_to(LEFT*3 + i * RIGHT)
            self.add(DecimalNumber(i).next_to(pi[i], UP))
        self.wait()

        pi2 = PiCreature(color=BLUE)
        self.add(pi2)
        pi2.move_to(DOWN*2)
        self.wait()

        pi2.look_at(LEFT)
        self.wait()

        pi2.shrug()
        self.wait()

class logo(InteractiveScene):
    def construct(self):
        logo_path = "/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master/custom/characters/logo.svg"
        logo = SVGMobject(logo_path).scale(3)
        self.play(Write(logo), run_time=7)

        self.wait()