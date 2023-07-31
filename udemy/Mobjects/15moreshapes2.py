from manimlib import *
import numpy as np

class moreshapes2(Scene):
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
		title = Text("Tangent Line, Polygon, Cubic Bezier, Rounded Rectangle").scale(0.7)
		self.play(FadeIn(title))
		#self.wait(3)
		self.play(FadeOut(title))

		"""
		#######
		#FROM LAST LECTURE
		#######
		axes = Axes(**self.axes_kwargs)
		axes.add_coordinate_labels(font_size=20, num_decimal_places=1)
		self.play(FadeIn(axes))

		func = lambda q: (q-4.5)**2 #Not a VMobject
		graph = axes.get_graph(func, color=BLUE, step_size=0.001) #VMobject
		self.play(FadeIn(graph))
		#######
		#FROM LAST LECTURE
		#######

		
		val = 0.2
		obj1 = TangentLine(graph, val).set_color(RED) #Tangent Something!
		self.play(FadeIn(obj1))
		for i in range(500):
			self.remove(obj1)
			val += 0.001
			obj1 = TangentLine(graph, val).set_color(RED)
			self.add(obj1)
			self.wait(0.001)
		

		vertices = [
			[-1, -1, 0],
			[0, 2, 0],
			[-4, -1, 0],
			[2, 0, 0],
		]

		obj2 = Polygon(*vertices)
		self.add(obj2)
		
		obj3 = CubicBezier(*vertices).set_color(RED)
		self.play(ShowCreation(obj3))

		"""

		obj4 = RoundedRectangle(corner_radius=0.5)
		self.add(obj4)








