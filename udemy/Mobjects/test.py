from manimlib import *
import numpy as np

def pendulum_vector_field_func(theta, omega, mu=0.3, g=9.8, L=3):
    return [omega, -np.sqrt(g / L) * np.sin(theta) - mu * omega]

class test(Scene):
	
	def construct(self): 
		
		plane = NumberPlane()
		
		vector_field = VectorField(
			pendulum_vector_field_func,
			plane,
			step_multiple=0.5,
            magnitude_range=(0, 5),
            length_func=lambda norm: 0.35 * sigmoid(norm)
		)
		vector_field.scale(0.5)
		self.play(FadeIn(vector_field))
		self.play(FadeOut(vector_field))

		
		stream_lines = StreamLines(
			pendulum_vector_field_func,
			plane
		)
		stream_lines.scale(0.5)
		self.play(FadeIn(stream_lines))
		self.play(FadeOut(stream_lines))
		
		asl = AnimatedStreamLines(stream_lines)
		self.add(asl)
		self.wait(3)
		
		
class test1(Scene):
	
	def construct(self): 
		text = Text("3D Graphs")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		#Scene Material
		title = Text("3D Graphs").shift(UP*3.5)
		self.play(FadeIn(title))

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
				

		axes3d = ThreeDAxes(x_range=(-5, 5, 1), 
		      				y_range=(-5, 5, 1),
							height = 12,
							width = 12,
							axis_config = {
								"stroke_color": WHITE,
								"stroke_width": 1,
								"include_tip": True,
								"include_ticks":True
							},
							z_axis_config = {
								"stroke_color": WHITE,
								"stroke_width": 1,
								"include_tip": True,
								"include_ticks":True
							}
							)
		
		self.play(FadeIn(axes3d))

		
		func2 = lambda q: [np.sin(q), np.cos(q), q]

		func3 = lambda t: np.array([
			5*np.cos(t)*np.cos(4*t)*np.cos(t)**9,
			5*np.sin(t)*np.cos(4*t)*np.cos(0.5)**9,
			5*np.sin(0.5)*np.cos(4*t)*np.cos(0.5)**8])
		
		graph = axes3d.get_parametric_curve(
					  func2, 
				      color=BLUE, 
					  #step_size=0.001, 
					  t_range=[-10, 10, 0.01]
					  )
		self.play(FadeIn(graph))
		rotateScene()















