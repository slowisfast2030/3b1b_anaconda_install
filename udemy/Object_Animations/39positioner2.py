from manimlib import *
import numpy as np
import random

class positioner2(Scene):
	def construct(self): 
		text = Text("Positioning Functions II: to_corner, to_edge, next_to, set_x/y/z").scale(0.6)
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Positioning Functions II: to_corner, to_edge, next_to, set_x/y/z").shift(UP*3.5).scale(0.6)
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

		stuff[0].target.next_to([-6, 2, 0])
		stuff[1].target.to_corner(LEFT + UP)
		stuff[2].target.set_z(-3)
		stuff[3].target.to_edge(DOWN)
		

		for i in stuff:
			self.play(MoveToTarget(i))







