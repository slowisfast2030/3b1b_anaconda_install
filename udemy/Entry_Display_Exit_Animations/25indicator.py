from manimlib import *
import numpy as np
import random

class indicator(Scene):
	def construct(self): 
		text = Text("GrowFromPoint, FocusOn, Indicate, Flash, CircleIndicate").scale(0.7)
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("GrowFromPoint, FocusOn, Indicate, Flash, CircleIndicate").shift(UP*3.5).scale(0.7)
		self.play(FadeIn(title))

		obj1 = Text("This is text").shift(LEFT*4)
		obj2 = Square().set_color(BLUE)
		obj3 = Circle(fill_opacity=1).set_color(YELLOW)
		obj4 = Rectangle(fill_opacity=1).set_color(GREEN)

		# self.play(GrowFromPoint(obj1, [5, 3, 0]), FadeIn(obj2)) #Not FadeInFromPoint, Not GrowFromCenter
		# self.play(FocusOn(obj2), FocusOn(obj1))
		self.play(Indicate(obj2), Indicate(obj1))
		# self.play(Flash(obj1), Flash(obj2))
		# self.play(CircleIndicate(obj1), CircleIndicate(obj2))
		



