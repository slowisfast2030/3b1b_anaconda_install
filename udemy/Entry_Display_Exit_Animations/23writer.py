from manimlib import *
import numpy as np
import random

class writer(Scene):
	def construct(self): 
		text = Text("Write, Transform, ShowCreation, ReplacementTransform").scale(0.7)
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Write, Transform, ShowCreation, ReplacementTransform").shift(UP*3.5).scale(0.7)
		self.play(FadeIn(title))

		obj1 = Text("This is text")
		obj2 = Square(fill_opacity=1).set_color(YELLOW)
		obj3 = Circle(fill_opacity=1).set_color(BLUE)
		obj4 = Rectangle(fill_opacity=1).set_color(GREEN)

		self.play(Write(obj1))
		self.play(Transform(obj1, obj2)) #obj2 is copies to obj1, but obj2 not in scene
		#self.play(Transform(obj2, obj3)) #obj2 in scene, becomes obj3
		self.play(Transform(obj1, obj3))
		self.remove(obj1)
		self.wait(2)
		self.play(ShowCreation(obj2))
		self.play(ReplacementTransform(obj2, obj3)) #obj2 is removed, obj3 is added
		self.play(ReplacementTransform(obj3, obj4))



