from manimlib import *
import numpy as np
import random

class rotator(Scene):
	def construct(self): 
		text = Text("Rotate, TurnInsideOut, WiggleOutThenIn")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Rotate, TurnInsideOut, WiggleOutThenIn").shift(UP*3.5)
		self.play(FadeIn(title))

		obj1 = Text("This is text").shift(LEFT*4)
		obj2 = Square(fill_opacity=1).set_color(BLUE)
		obj3 = Circle(fill_opacity=1).set_color(YELLOW)
		obj4 = Rectangle(fill_opacity=1).set_color(GREEN)

		self.add(obj2)
		self.play(Rotate(obj1, TAU, run_time=3))
		#self.play(TurnInsideOut(obj2))
		#self.play(WiggleOutThenIn(obj2))






