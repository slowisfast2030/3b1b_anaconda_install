from manimlib import *
import numpy as np
import random

class homoto(Scene):
	def construct(self): 
		text = Text("Homotopy")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Homotopy").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		obj1 = Text("This is text").shift(LEFT*4)
		obj2 = Square(fill_opacity=1).set_color(YELLOW).shift(LEFT*3 + DOWN*3)
		obj3 = Circle(fill_opacity=1).set_color(BLUE).shift(UP*2)
		obj4 = Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*2)

		self.add(obj2)


		test_homotopy = lambda x, y, z, t: (
			x + interpolate(-3, 3, 2*t if t<=0.5 else 1), # First 5 Seconds
			y + interpolate(0, 3, 2*(t-0.5) if t>0.5 else 0), # Next 5 Seconds
			z)

		test_homotopy2 = lambda x, y, z, t: (
			x + interpolate(-3, 3, 4*t if t<=0.25 else 1) 
				+ interpolate(3, -3, 4*(t-0.5) if (t>=0.5 and t<=0.75) else (0 if t<=0.5 else 1)), 
			y + interpolate(-3, 3, 4*(t-0.25) if (t>0.25 and t<0.5) else (0 if t<=0.25 else 1)) 
				+ interpolate(3, -3, 4*(t-0.75) if (t>0.75) else (0 if t<=0.75 else 1)), 
			z)


		

		
		self.play(Homotopy(test_homotopy, obj2, run_time=10, rate_func=linear))
		#ComplexHomotopy









		









		





		