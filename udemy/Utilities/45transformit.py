from manimlib import *
import numpy as np
import random

class transformit(Scene):
	def construct(self): 
		text = Text("turn_animation_into_updater, cycle_animation")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("turn_animation_into_updater, cycle_animation").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		stuff = []
		stuff.append( Text("This is text").shift(LEFT*4) )
		stuff.append(  Cube(fill_opacity=1).set_color(YELLOW).shift(RIGHT*4) )
		stuff.append(  Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*2) )
		stuff.append(  Sphere(fill_opacity=1).set_color(RED).shift(UP*2) )
		
		for i in stuff:
			i.generate_target()
		self.add(*stuff)
		self.wait(3)


		turn_animation_into_updater(Write(stuff[0]), cycle=True)
		turn_animation_into_updater(ShowCreation(stuff[1]), cycle=True)
		turn_animation_into_updater(FadeIn(stuff[2]), cycle=False)
		cycle_animation(FadeOut(stuff[3]))
		self.wait(30)


		
			






