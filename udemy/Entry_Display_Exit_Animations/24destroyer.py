from manimlib import *
import numpy as np
import random

class destroyed(Scene):
	def construct(self): 
		text = Text("Uncreate, DrawBorderThenFill, GrowFromCenter, SpinInFromNothing").scale(0.7)
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Uncreate, DrawBorderThenFill, GrowFromCenter, SpinInFromNothing").shift(UP*3.5).scale(0.7)
		self.play(FadeIn(title))

		obj1 = Text("This is text").shift(LEFT*4)
		obj2 = Square(fill_opacity=1).set_color(YELLOW)
		obj3 = Circle(fill_opacity=1).set_color(BLUE)
		obj4 = Rectangle(fill_opacity=1).set_color(GREEN)

		"""
		self.add(obj2)
		self.wait(2)
		self.play(Uncreate(obj2))
		self.wait(2)

		self.play(DrawBorderThenFill(obj3))
		self.wait(2)
		self.remove(obj3)

		self.play(GrowFromCenter(obj1))
		self.wait(2)
		self.remove(obj1)
		"""
		self.play(SpinInFromNothing(obj4, path_arc=PI/2)) #[0, PI]
		self.wait(2)
		self.remove(obj4)





