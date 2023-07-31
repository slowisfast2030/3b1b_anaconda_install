from manimlib import *
import numpy as np

class threedgraph(Scene):
	CONFIG = {
		"axes_kwargs": {
			"x_range": (-1, 10, 1),
			"y_range": (-1, 10, 1),
			"height": 6,
			"width": 12,
			"axis_config": {
				"stroke_color": PINK,
				"stroke_width": 4,
				#"include_tip": True,
				#"include_ticks":True
			},
			"y_axis_config": {
				"include_tip": False
			}
		},
		"axes3d_kwargs": {
			"x_range": (-5, 5, 1),
			"y_range": (-5, 5, 1),
			"height": 12,
			"width": 12,
			"axis_config": {
				"stroke_color": WHITE,
				"stroke_width": 4,
				"include_tip": True,
				"include_ticks":True
			},
		}
	}
	def construct(self): 
		text = Text("3D Graphs")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		#Scene Material
		title = Text("3D Graphs").shift(UP*3.5)
		self.play(FadeIn(title))

		#######
		#FROM LAST LECTURE
		#######

		"""
		#Axes
		axes = Axes(**self.axes_kwargs)
		axes.add_coordinate_labels(font_size=20, num_decimal_places=1)
		func = lambda q: (q-4.5)**2 #Not a VMobject
		graph = axes.get_graph(func, color=BLUE, step_size=0.001) #VMobject
		self.play(FadeIn(axes), FadeIn(graph))
		"""

		#stuff in scene
		obj1 = Cube().shift(LEFT*4 + IN*4).set_color(GREEN)
		obj2 = Prism().shift(RIGHT*3 + UP*1 + OUT*1).set_color(RED)
		obj3 = Sphere().shift(DOWN*2).set_color(BLUE)
		self.play(FadeIn(Group(obj1, obj2, obj3)))

		#Camera
		frame = self.camera.frame

		frame2 = frame.copy()
		frame2.set_euler_angles(
			theta = -10*DEGREES,
			phi = 50 *DEGREES
		)
		self.play(Transform(frame, frame2))

		def rotateScene():
			for i in range(200):
				frame.increment_theta(0.01)
				self.wait(0.001)
				#pass
		#######
		#FROM LAST LECTURE
		#######
		rotateScene()
		#self.play(FadeOut(Group(axes, graph)))
		#rotateScene()

		axes3d = ThreeDAxes(**self.axes3d_kwargs)
		self.play(FadeIn(axes3d))

		"""
		func = lambda q: q**2 #Not a VMobject
		func2 = lambda q: [np.sin(q), np.cos(q), q]
		graph = axes3d.get_parametric_curve(func2, color=BLUE, step_size=0.001, t_range=[-10, 10]) #VMobject
		self.play(FadeIn(graph))
		"""












		func3 = lambda t: np.array([
			5*np.cos(t)*np.cos(4*t)*np.cos(s)**9,
			5*np.sin(t)*np.cos(4*t)*np.cos(0.5)**9,
			5*np.sin(0.5)*np.cos(4*t)*np.cos(0.5)**8])
		graph = axes3d.get_parametric_curve(func3, color=BLUE, step_size=0.001, t_range=[-10, 10]) #VMobject
		self.play(FadeIn(graph))
		rotateScene()











