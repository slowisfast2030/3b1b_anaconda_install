from manimlib import *
import numpy as np
import random

class tops2(Scene):
	def construct(self): 
		text = Text("Transforming Ops II: wag, rotate_about_origin, apply_function, apply_matrix").scale(0.6)
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Transforming Ops II: wag, rotate_about_origin, apply_function, apply_matrix").shift(UP*3.5).scale(0.6)
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

		#Function & Matrix
		func = lambda m : m/2 + rotate_vector(m/2, PI/3)
		mskew = [[1, 0.5], 
				[0, 1]]

		
		stuff[1].target.rotate_about_origin(PI/3)
		stuff[2].target.apply_matrix(mskew)
		stuff[3].target.apply_function(func)
		stuff[0].target.wag(direction=LEFT, axis=DOWN, wag_factor=0.5)

		for i in stuff:
			self.play(MoveToTarget(i))

		stuff[0].target.wag(direction=RIGHT, axis=DOWN, wag_factor=0.5)
		self.play(MoveToTarget(stuff[0]))






