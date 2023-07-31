from manimlib import *
import numpy as np
import random

class applystuff(Scene):
	def construct(self): 
		text = Text("""
			ApplyMethod, ApplyFunction, 

			ScaleInPlace, Restore
			""")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("ApplyMethod, ApplyFunction, ScaleInPlace, Restore").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		obj1 = Text("This is text").shift(LEFT*4)
		obj2 = Square(fill_opacity=1).set_color(BLUE).shift(UP*2)
		obj3 = Circle(fill_opacity=1).set_color(YELLOW)
		obj4 = Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*2)

		self.add(obj1, obj2, obj3)

		#Save Point
		obj1.save_state()
		obj2.save_state()
		obj3.save_state()
		self.wait(1)
		self.play(ApplyMethod(obj2.shift, 3*RIGHT+DOWN*2))
		self.play(ApplyMethod(obj2.set_color, WHITE))

		#ApplyFuntion is GENERAL
		self.play(ApplyFunction(lambda m : m.scale(0.5).fade(0.3),obj1))
		self.play(ScaleInPlace(obj3, 2))


		#Restore Objects that were saved
		self.play(Restore(obj1), Restore(obj2), Restore(obj3))








