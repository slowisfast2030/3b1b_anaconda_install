from manimlib import *
import numpy as np
import random

class spacemaker(Scene):
	def construct(self): 
		text = Text("Space Operations")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Space Operations").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		stuff = []
		stuff.append( Text("This is text").shift(LEFT*4) )
		stuff.append(  Cube(fill_opacity=1).set_color(YELLOW).shift(RIGHT*4) )
		stuff.append(  Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*2) )
		stuff.append(  Sphere(fill_opacity=1).set_color(RED).shift(UP*2) )
		

		for i in stuff:
			i.generate_target()
		self.add(*stuff)
		#self.wait(3)

		a = angle_of_vector([1, 1, 1])/DEGREES #on XY axis
		b = normalize([2, 0, 1])
		c = midpoint([0, -1, 0], [1, 2, 1])
		d = rotation_matrix(PI/2,[0, 0, -1])
		e = get_norm([1, 1, 2])
		print(a)
		print(b)
		print(c)
		print(d)
		print(e)
		
			






