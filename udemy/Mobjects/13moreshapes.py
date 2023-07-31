from manimlib import *
import numpy as np

class moreshapes(Scene):
	def construct(self): 
		title = Text("Arc, Sector, Vector, DashedLine, Arrow")
		self.play(FadeIn(title))
		#self.wait(3)
		self.play(FadeOut(title))

		shape1 = Arc(start_angle=np.pi/2+np.pi/3, angle=np.pi)
		self.add(shape1)
		self.wait(0.1)
		self.remove(shape1)

		shape2 = Sector(start_angle=np.pi/2+np.pi/3, angle=np.pi)
		self.add(shape2)
		self.wait(0.1)
		self.remove(shape2)

		shape3 = Vector(direction=[2, 2, 0]) #Direction
		self.add(shape3)
		self.wait(0.1)
		self.remove(shape3)

		shape4 = DashedLine([-3, -2, 0], [2, 1, 0])
		self.add(shape4)
		self.wait(0.1)
		self.remove(shape4)

		shape5 = Arrow([-1, -1, 0], [3, 0, 0]) #2 Points
		self.add(shape5)
		self.wait(0.1)
		#self.remove(shape4)

		





