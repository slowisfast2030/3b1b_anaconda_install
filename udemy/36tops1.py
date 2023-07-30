from manimlib import *
import numpy as np
import random

class tops1(Scene):
	def construct(self): 
		text = Text("Transforming Ops I: shift, scale, stretch, rotate, flip").scale(0.8)
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Transforming Ops I: shift, scale, stretch, rotate, flip").shift(UP*3.5).scale(0.6)
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

		stuff[0].target.flip([0.2,0.3, 0])
		stuff[1].target.stretch(0.5, 1) #0 is X, 1 is Y, 2 is Z (only 3d objects)
		stuff[2].target.scale(0.5)
		#stuff[3].target.rotate(PI/3)
		stuff[3].target.shift(DOWN*1)

		for i in stuff:
			self.play(MoveToTarget(i))
		
