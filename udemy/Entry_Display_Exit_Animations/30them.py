from manimlib import *
import numpy as np
import random

class applystuff(Scene):
	def construct(self): 
		text = Text("ApplyMatrix, ApplyComplexFunction")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("ApplyMatrix, ApplyComplexFunction").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		obj1 = Text("This is text").shift(LEFT*4)
		obj2 = Square(fill_opacity=1).set_color(BLUE)
		obj3 = Circle(fill_opacity=1).set_color(YELLOW).shift(UP*2)
		obj4 = Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*2)

		self.add(obj1, obj2, obj3)

		mskew = [[1, 0.5], 
				[0, 1]]
		mflip = [[0, 1],
				[1, 0]]
		cfunc1 = lambda w: w*1j
		cfunc2 = lambda w: w*1j/2 + w/2 #i^2 -> 180 rotation /2 + 90/2, 135 degree rotation

		self.wait(1)
		self.play(ApplyMatrix(mflip, obj2))
		self.play(ApplyComplexFunction(cfunc2, obj2))
		







