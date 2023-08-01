from manimlib import *


class test(Scene):
	def construct(self):
		obj1 = Square(fill_opacity=1).set_color(RED).shift(LEFT*2)
		obj2 = Circle(fill_opacity=1).set_color(BLUE).shift(RIGHT*2)

		self.play(ReplacementTransform(obj1, obj2))
		








