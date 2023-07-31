from manimlib import *
import numpy as np

class cam(Scene):
	def construct(self): 
		text = Text("Camera")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		#Scene Material
		title = Text("Camera").shift(UP*3.5)
		self.play(FadeIn(title))
		self.play(FadeIn(Square(fill_opacity=1).set_color(YELLOW)))

		#Camera
		frame = self.camera.frame

		frame2 = frame.copy()
		frame2.set_euler_angles(
			theta = -10*DEGREES,
			phi = 50 *DEGREES
		)
		self.play(Transform(frame, frame2))

		frame3 = frame2.copy()
		frame3.set_width(25)
		self.play(Transform(frame, frame3))

		#Directly change frame
		self.play(
			frame.increment_phi, -10*DEGREES,
			frame.increment_theta, -20*DEGREES,
			run_time=3
			)

		frame4 = frame3.copy()
		frame4.set_width(15)
		self.play(Transform(frame, frame4))
		#Rotating Camera (without updaters)
		for i in range(1000):
			frame.increment_theta(0.001)
			self.wait(0.001)






