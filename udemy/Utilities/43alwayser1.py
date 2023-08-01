from manimlib import *
import numpy as np
import random

class alwayser1(Scene):
	def construct(self): 
		text = Text("always, f_always").scale(0.6)
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("always, f_always").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		stuff = []
		stuff.append( Text("This is text").shift(LEFT*4) )
		stuff.append(  Square(fill_opacity=1).set_color(YELLOW).shift(RIGHT*4) )
		stuff.append(  Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*2) )
		stuff.append(  Triangle(fill_opacity=1).set_color(RED).shift(UP*2) )
		
		for i in stuff:
			i.generate_target()
		self.add(*stuff)
		self.wait(1)


		always(stuff[0].next_to, stuff[1], LEFT, buff=MED_SMALL_BUFF)
		always(stuff[2].next_to, stuff[3], RIGHT, buff=MED_SMALL_BUFF)

		stuff[1].target.shift(LEFT*5)
		stuff[3].target.shift(DOWN*3)

		for i in stuff:
			self.play(MoveToTarget(i))

		
		self.remove(*stuff)
		stuff = []
		stuff.append( Text("This is text").shift(LEFT*4) )
		stuff.append(  Square(fill_opacity=1).set_color(YELLOW).shift(RIGHT*4) )
		stuff.append(  Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*2) )
		stuff.append(  Triangle(fill_opacity=1).set_color(RED).shift(UP*2) )
		
		for i in stuff:
			i.generate_target()
		self.add(*stuff)
		self.wait(1)
		x = ValueTracker(-3)
		f_always(stuff[0].set_x, x.get_value)
		self.play(ApplyMethod(x.increment_value, 10, run_time=20))
		

