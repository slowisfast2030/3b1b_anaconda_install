from manimlib import *
import numpy as np
import random

class misc1(Scene):
	def construct(self): 
		text = Text("Matrices, BarChart, SurroundingRectangle, Dot Cloud").scale(0.7)
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Matrices, BarChart, SurroundingRectangle, Dot Cloud").shift(UP*3.5).scale(0.7)
		self.play(FadeIn(title))

		mat = [['3', '5', 'x'], ['1', '2', 'x^2'], ['4', '6', 'x_i']]
		m = Matrix(mat)
		self.play(FadeIn(m))
		self.play(FadeOut(m))

		#BarChart(data, labels) -> kwarg max_value
		#5, 4, 1
		bar_chart = BarChart([(5-k) for k in range(3)], bar_names = ['Q', 'R', 'S'], max_value=10)
		#bar_chart.to_edge(DOWN)
		self.add(bar_chart)


		#BoundingBox, Created Minimum Rectangle that Fills Region, any MOBJECT!!!
		srect = SurroundingRectangle(bar_chart)
		self.play(ShowCreation(srect))
		self.play(FadeOut(bar_chart), FadeOut(srect))
		
		#DotCloud(points) -> points = [ [x, y, z], [x2, y2, z2], .. ]
		pdots = DotCloud([[random.randint(-50, 50)/10, random.randint(-30, 30)/10, 0] for i in range(50)], color=RED)
		self.add(pdots)
		


