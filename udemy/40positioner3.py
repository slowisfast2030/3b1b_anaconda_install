from manimlib import *
import numpy as np
import random

class positioner3(Scene):
	def construct(self): 
		text = Text("Positioning Functions III: stretch_to_fit, set_width/height/depth, set_coord").scale(0.6)
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Positioning Functions III: stretch_to_fit, set_width/height/depth, set_coord").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		stuff = []
		stuff.append( Text("This is text").shift(LEFT*4) )
		stuff.append(  Square(fill_opacity=1).set_color(YELLOW).shift(RIGHT*4) )
		stuff.append(  Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*2) )
		stuff.append(  Circle(fill_opacity=1).set_color(RED).shift(UP*2) )
		
		for i in stuff:
			i.generate_target()
		self.add(*stuff)
		self.wait(1)

		stuff[0].target.stretch_to_fit_width(2) #height or depth
		stuff[1].target.set_width(5)
		stuff[2].target.set_height(0.2)
		stuff[3].target.set_coord(-5, 0) #0 for x, 1 for y, 2 for z
		stuff[3].target.set_coord(-3, 1) #0 for x, 1 for y, 2 for z
		stuff[3].target.set_coord(2, 2) #0 for x, 1 for y, 2 for z
		

		for i in stuff:
			self.play(MoveToTarget(i))







