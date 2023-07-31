from manimlib import *
import numpy as np

class lsurfaces(Scene):
	CONFIG = {
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
		text = Text("Surfaces: Parametric, Textured")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Surfaces: Parametric, Textured").shift(UP*3.5)
		self.play(FadeIn(title))

		#######
		#FROM LAST LECTURE
		#######

		axes3d = ThreeDAxes(**self.axes3d_kwargs)
		self.play(FadeIn(axes3d))
		"""
		#stuff in scene
		obj1 = Cube().shift(LEFT*4 + IN*4).set_color(GREEN)
		obj2 = Prism().shift(RIGHT*3 + UP*1 + OUT*1).set_color(RED)
		obj3 = Sphere().shift(DOWN*2).set_color(BLUE)

		func = lambda q: q**2 #Not a VMobject
		func2 = lambda q: [np.sin(q), np.cos(q), q]
		graph = axes3d.get_parametric_curve(func2, color=BLUE, step_size=0.001, t_range=[-3, 3]) #VMobject
		self.play(FadeIn(axes3d), FadeIn(graph), FadeIn(Group(obj1, obj2, obj3)))
		"""

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
		"""
		rotateScene()
		sphereMesh = SurfaceMesh(obj3, resolution=(7, 7), flat_stroke=True, color=WHITE, stroke_width=5)
		self.play(FadeOut(graph), FadeOut(obj3), FadeOut(obj2), FadeOut(obj1), FadeIn(sphereMesh))
		rotateScene()
		self.play(FadeOut(sphereMesh))
		"""

		func3 = lambda u, v: [
			3*np.cos(u)*np.cos(4*u)*np.cos(v)**9,
			3*np.sin(u)*np.cos(4*u)*np.cos(v)**9,
			3*np.sin(v)*np.cos(4*u)*np.cos(v)**8]
		#Function has u and v parameters
		psurface = ParametricSurface(func3, u_range=(-PI, PI), v_range=(-PI, PI), color=BLUE)
		self.play(FadeIn(psurface))
		rotateScene()
		self.play(FadeOut(psurface))

		#Need Parametric Surface to Texture
		tsurface = TexturedSurface(psurface, "./flowers.jpeg")
		self.play(FadeIn(tsurface))





