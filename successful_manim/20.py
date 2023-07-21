import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *
from _2023.clt.main import *


class SumsOfSizeFive(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        self.add(morty)
        self.wait()

class test(InteractiveScene):
    def construct(self):
        pi = PiCreature(color=BLUE_E)
        self.add(pi)
        self.wait()
