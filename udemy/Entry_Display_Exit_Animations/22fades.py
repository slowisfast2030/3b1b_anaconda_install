from manimlib import *
import numpy as np
import random

class fades(Scene):
	def construct(self): 
		text = Text("Fade, FadeIn, FadeOut, FadeInFromPoint, FadeTransform").scale(0.7)
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Fade, FadeIn, FadeOut, FadeInFromPoint, FadeTransform").shift(UP*3.5).scale(0.7)
		self.play(FadeIn(title))

		obj1 = Square(fill_opacity=1).set_color(YELLOW)
		obj2 = Circle(fill_opacity=1).set_color(BLUE)
		obj3 = Rectangle(fill_opacity=1).set_color(GREEN)

		self.play(FadeInFromPoint(obj1, [5, 3, 0]))
		self.play(FadeTransform(obj1, obj2))
		self.play(FadeTransform(obj2, obj3))
		








