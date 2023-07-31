from manimlib import *
import numpy as np
import random

class friend(Scene):
	def construct(self): 
		text = Text("MaintainPositionRelativeTo")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("MaintainPositionRelativeTo").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		obj1 = Text("This is text").shift(LEFT*4)
		obj2 = Square(fill_opacity=1).set_color(BLUE)
		obj3 = Circle(fill_opacity=1).set_color(YELLOW).shift(UP*2)
		obj4 = Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*2)

		self.add(obj2, obj3)
		self.wait(1)
		self.play(ApplyMethod(obj3.shift, DOWN*2), MaintainPositionRelativeTo(obj2, obj3))


		#Few Other Animations you can do, go ahead and read the code/lirbary
