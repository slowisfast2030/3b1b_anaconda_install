from manimlib import *
import numpy as np
import random

class flashstyle(Scene):
	def construct(self): 
		text = Text("ShowPassingFlash, ShowPassingFlashAround, ShowCreationThenFadeAround, ApplyWave").scale(0.5)
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("ShowPassingFlash, ShowPassingFlashAround, ShowCreationThenFadeAround, ApplyWave").shift(UP*3.5).scale(0.5)
		self.play(FadeIn(title))

		obj1 = Text("This is text").shift(LEFT*4)
		obj2 = Square(fill_opacity=1).set_color(BLUE)
		obj3 = Circle(fill_opacity=1).set_color(YELLOW)
		obj4 = Rectangle(fill_opacity=1).set_color(GREEN)

		#
		self.play(ShowPassingFlash(obj1, remover=False))
		#self.play(ShowPassingFlash(obj2, run_time=5))
		self.add(obj2)
		#self.play(ShowPassingFlashAround(obj1))
		#self.play(ShowPassingFlashAround(obj2))
		self.wait(2)
		self.play(ShowCreationThenFadeAround(obj1))
		self.play(ShowCreationThenFadeAround(obj2))
		self.wait(2)
		self.play(ApplyWave(obj1))
		self.play(ApplyWave(obj2))




