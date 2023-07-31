from manimlib import *
import numpy as np
import random

class positioner1(Scene):
	def construct(self): 
		text = Text("Positioning Functions I: move_to, center, replace, surround, rescale_to_fit").scale(0.6)
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Positioning Functions I: move_to, center, replace, surround, rescale_to_fit").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		stuff = []
		stuff.append( Text("This is text").shift(LEFT*4) )
		stuff.append(  Square(fill_opacity=1).set_color(YELLOW).shift(RIGHT*4) )
		stuff.append(  Circle(fill_opacity=1).set_color(RED).shift(UP*2) )
		stuff.append(  Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*2) )
		for i in stuff:
			i.generate_target()
		self.add(*stuff)
		self.wait(1)

		stuff[0].target.surround(stuff[1]) #mobject
		stuff[1].target.move_to([-3, 2, 0])
		stuff[2].target.center()
		#stuff[3].target.replace(stuff[1].target) #mobject
		stuff[3].target.rescale_to_fit(2, 0) #0 is x, 1 is y, 2 is z (only 3D)
		

		for i in stuff:
			self.play(MoveToTarget(i))







