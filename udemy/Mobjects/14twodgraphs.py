from manimlib import *
import numpy as np

class twodgraphs(Scene): #2d Coordinate systems
	CONFIG = {
		"axes_kwargs": {
			"x_range": (-1, 10, 1),
			"y_range": (-1, 10, 1),
			"height": 6,
			"width": 12,
			"axis_config": {
				"stroke_color": PINK,
				"stroke_width": 4,
			},
			"y_axis_config": {
				"include_tip": False
			}
		}
	}
	def construct(self): 
		title = Text("Axes, NumberPlane, Complex Plane")
		self.play(FadeIn(title))
		#self.wait(3)
		self.play(FadeOut(title))

		"""
		a1 = Axes()
		a1.add_coordinate_labels()
		self.play(FadeIn(a1))
		self.wait(1)
		self.play(FadeOut(a1))

		a2 = NumberPlane()
		a2.add_coordinate_labels()
		self.play(FadeIn(a2))
		self.wait(1)
		self.play(FadeOut(a2))

		a3 = ComplexPlane()
		a3.add_coordinate_labels()
		self.play(FadeIn(a3))
		self.wait(1)
		self.play(FadeOut(a3))
		"""


		axes = Axes(**self.axes_kwargs)
		axes.add_coordinate_labels(font_size=20, num_decimal_places=1)
		self.add(axes)

		func = lambda q: (q-4.5)**2 #Quadratic Function
		graph = axes.get_graph(func, color=BLUE, step_size=0.001)
		self.play(FadeIn(graph))

		x = 2.5
		ball = Dot(color=RED).scale(2).move_to(axes.c2p(x, func(x)))
		self.add(ball)

		rects = axes.get_riemann_rectangles(graph, x_range=[2, 7.5], dx=0.5)
		self.play(ShowCreation(rects))


		






