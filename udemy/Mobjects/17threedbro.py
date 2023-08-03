from manimlib import *
import numpy as np

class threedbro(Scene):
	def construct(self): 
		text = Text("""
			3D Shapes: Sphere, Torus, 

			Cylinder, Line3D, Cube, Prism
			""")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		#Scene Material
		title = Text("3D Shapes").shift(UP*3.5)
		self.play(FadeIn(title))

		#######
		#FROM LAST LECTURE
		#######
		#Camera
		frame = self.camera.frame

		frame2 = frame.copy()
		frame2.set_euler_angles(
			theta = -10*DEGREES,
			phi = 50 *DEGREES
		)
		self.play(Transform(frame, frame2))
		#######
		#FROM LAST LECTURE
		#######

		def rotateScene():
			for i in range(200):
				frame.increment_theta(0.01)
				self.wait(0.001)
				#pass
		
		o1 = Sphere().set_color(BLUE)
		self.play(FadeIn(o1))
		#rotateScene()


		o2 = Torus().set_color(RED).scale(0.2).shift(LEFT*3)
		self.play(FadeIn(o2))
		#rotateScene()

		
		o3 = Cylinder(height=3, radius=0.5).set_color(GREEN).shift(RIGHT*3)
		self.play(FadeIn(o3))
		#rotateScene()
		
		
		o4 = Line3D(np.array([-5, 0, -4]), np.array([5, 0, 4]), width=0.1, resolution=(101, 101))
		self.play(FadeIn(o4))
		#rotateScene()
		

		#self.play(FadeOut(Group(o1, o2, o3, o4)))
		rotateScene()
		

		# o5 = Cube().set_color(GREEN).shift(LEFT*2)
		# self.play(FadeIn(o5))
		# rotateScene()

		# o6 = Prism(*[1, 2, 3]).set_color(RED).shift(RIGHT*2)
		# self.play(FadeIn(o6))
		# rotateScene()
		

