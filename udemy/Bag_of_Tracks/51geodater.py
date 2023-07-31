from manimlib import *
import numpy as np
import random

class geodater(Scene):
	def construct(self): 
		text = Text("Geometry Updaters")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Geometry Updaters").shift(UP*5)#.scale(0.6)
		self.play(FadeIn(title))

		frame = self.camera.frame
		frame.generate_target()
		frame.target.set_euler_angles(
			theta = -10*DEGREES,
			phi = 50 *DEGREES
		)
		self.play(MoveToTarget(frame))
		def rotCam(self):
			self.increment_theta(-0.005)
		frame.add_updater(rotCam)


		obj = Prism(dimensions=[2, 2, 2], color=ORANGE)
		self.play(FadeIn(obj, UP))

		def dimMeasure(dir, dic, ord):
			brace = always_redraw(Brace, obj, dir)
			text, number = label = Group(
				Text(dic + " = "),
				DecimalNumber(0,num_decimal_places=2,include_sign=True)
			)
			label.arrange(RIGHT)
			always(label.next_to, brace, dir)
			f_always(number.set_value, ord)
			return Group(brace, label)

		d1 = dimMeasure(UP, "Width", obj.get_width)
		d2 = dimMeasure(RIGHT, "Depth", obj.get_height)
		self.add(d1, d2)
		self.play(
			obj.animate.set_width(5, stretch=True),
			run_time=3,
		)
		self.play(
			obj.animate.set_height(5, stretch=True),
			run_time=3,
		)
		self.play(
			obj.animate.set_width(1, stretch=True),
			run_time=3,
		)
		self.play(
			obj.animate.set_height(1, stretch=True),
			run_time=3,
		)






		







