import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class trans(Scene):
	def construct(self): 
		obj1 = Square(fill_opacity=1).set_color(BLUE)
		obj2 = Circle(fill_opacity=1).set_color(YELLOW).shift(UP*2)
		self.play(Transform(obj1, obj2))
		# vm = VMobject()

		# vm.interpolate(obj1, obj2, alpha=0.5)
		# self.add(vm)
		# self.wait(1)