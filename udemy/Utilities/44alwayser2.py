from manimlib import *
import numpy as np
import random

class alwayser2(Scene):
	def construct(self): 
		text = Text("always, always_shift, always_rotate").scale(0.6)
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("always, always_shift, always_rotate").shift(UP*3.5).scale(0.6)
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

		# 右移
		always_shift(stuff[0], RIGHT, rate=0.1) 
		# 原地旋转
		always_rotate(stuff[1], axis=OUT) 
		# 绕原点旋转
		always(stuff[2].rotate_about_origin, angle=0.01) #rotate, scale, shift, set_color
		self.wait(10)


		
			



