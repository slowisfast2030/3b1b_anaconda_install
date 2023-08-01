from manimlib import *
import numpy as np
import random

class rateit(Scene):
	def construct(self): 
		text = Text("Rate Functions")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Rate Functions").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		stuff = []
		stuff.append(  Text("This is text").shift(LEFT*4) )
		stuff.append(  Square(fill_opacity=1).set_color(YELLOW).shift(RIGHT*4) )
		stuff.append(  Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*2) )
		stuff.append(  Triangle(fill_opacity=1).set_color(RED).shift(UP*2) )
		

		for i in stuff:
			i.generate_target()
		self.add(*stuff)
		stuff[2].target.shift(UP*3)
		self.play(MoveToTarget(stuff[2]), rate_func = there_and_back)
		self.wait(3)


		
			






