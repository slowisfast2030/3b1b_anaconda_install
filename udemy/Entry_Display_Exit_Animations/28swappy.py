from manimlib import *
import numpy as np
import random

class rotator(Scene):
	def construct(self): 
		text = Text("""
			ClockwiseTransform, Swap, 

			FadeToColor, ShrinkToCenter
			""")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("ClockwiseTransform, Swap, FadeToColor, ShrinkToCenter").shift(UP*3.5).scale(0.5)
		self.play(FadeIn(title))

		obj1 = Text("This is text").shift(LEFT*4)
		obj2 = Square(fill_opacity=1).set_color(BLUE).shift(UP*2)
		obj3 = Circle(fill_opacity=1).set_color(YELLOW)
		obj4 = Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*2)




		self.add(obj1)
		self.wait(2)
		self.play(ClockwiseTransform(obj1, obj2)) #Obj2 copied to Obj1
		self.play(ClockwiseTransform(obj2, obj3)) #Obj3 copied to Obj2
		self.play(ClockwiseTransform(obj3, obj4)) #Obj4 copied to Obj3


		obj5 = Text("This is text").shift(LEFT*4)
		self.play(Swap(obj2, obj3, obj1, obj5)) #Put in AS MANY OBJECTS!
		self.play(Swap(obj2, obj3, obj1, obj5))
		self.play(Swap(obj2, obj3, obj1, obj5))
		self.play(Swap(obj2, obj3, obj1, obj5))

		

		self.play(FadeToColor(obj1, '#FF8800'))
		#rrggbb


		

		self.play(ShrinkToCenter(obj1))
		self.play(ShrinkToCenter(obj2))
		self.play(ShrinkToCenter(obj3))
		self.play(ShrinkToCenter(obj5))
		








