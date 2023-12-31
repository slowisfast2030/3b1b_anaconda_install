from manimlib import *
import numpy as np
import random

class camgym(Scene):
	def construct(self): 
		# text = Text("Camera Gymnastics")
		# self.play(FadeIn(text))
		# #self.wait(3)
		# self.play(FadeOut(text))

		title = Text("Camera Gymnastics").shift(UP*3.5)#.scale(0.6)
		self.play(FadeIn(title))

		stuff = []
		stuff.append( Text("This is text").shift(LEFT*4) )
		#stuff.append(  Prism().set_color(YELLOW).shift(RIGHT*4) )
		stuff.append(  Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*2) )
		stuff.append(  Sphere().set_color(RED).shift(UP*2) )
		
		for i in stuff:
			i.generate_target()
		self.add(*stuff)

		frame = self.camera.frame
		print("+"*100)
		print(frame.get_theta()) # 0
		print(frame.get_phi()) # 0
		print(frame.get_gamma()) # 0
		print(frame.get_euler_angles()) # [0, 0, 0]
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
		# 这里的欧拉角不是极坐标系
		frame.target.set_euler_angles(
			theta = -10 * DEGREES,
			phi = 50 * DEGREES
		)
		frame.target.set_width(9)
		self.play(MoveToTarget(frame))

		# self.play(
		# 	frame.animate.set_width(9).set_euler_angles(-10*DEGREES, 50*DEGREES) # 这里两个属性设置的先后顺序无关
		# )


		#Old Method
		"""
		#Rotating Camera (without updaters)
		for i in range(1000):
			frame.increment_theta(0.001)
			self.wait(0.001)
		"""

		#New Method
		# def rotCam(self):
		# 	self.increment_theta(0.005)
		# frame.add_updater(rotCam)
		# self.wait(5)

		# frame.remove_updater(rotCam)
		# self.wait(1)
		# frame.target.shift(LEFT*7) #Camera to look at (x, y, z) that is not (0, 0, 0)
		# #Then shift target amount RIGHT*x + UP*y + OUT*z
		# self.play(MoveToTarget(frame))
		



