from manimlib import *
import numpy as np
import random

class camgym(Scene):
	def construct(self): 
		text = Text("Camera Gymnastics")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Camera Gymnastics").shift(UP*3.5)#.scale(0.6)
		self.play(FadeIn(title))

		stuff = []
		stuff.append( Text("This is text").shift(LEFT*4) )
		stuff.append(  Cube(fill_opacity=1).set_color(YELLOW).shift(RIGHT*4) )
		stuff.append(  Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*2) )
		stuff.append(  Sphere(fill_opacity=1).set_color(RED).shift(UP*2) )
		
		for i in stuff:
			i.generate_target()
		self.add(*stuff)

		frame = self.camera.frame
		#Old Method
		"""
		frame2 = frame.copy()
		frame2.set_euler_angles(
			theta = -10*DEGREES,
			phi = 50 *DEGREES
		)
		self.play(Transform(frame, frame2))
		"""

		#New Method
		frame.generate_target()
		frame.target.set_euler_angles(
			theta = -10*DEGREES,
			phi = 50 *DEGREES
		)
		frame.target.set_width(9)
		self.play(MoveToTarget(frame))


		#Old Method
		"""
		#Rotating Camera (without updaters)
		for i in range(1000):
			frame.increment_theta(0.001)
			self.wait(0.001)
		"""

		#New Method
		def rotCam(self):
			self.increment_theta(0.005)
		frame.add_updater(rotCam)
		self.wait(10)
		frame.remove_updater(rotCam)
		self.wait(1)
		frame.target.shift(LEFT*7) #Camera to look at (x, y, z) that is not (0, 0, 0)
		#Then shift target amount RIGHT*x + UP*y + OUT*z
		self.play(MoveToTarget(frame))
		



