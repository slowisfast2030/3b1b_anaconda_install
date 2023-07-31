from manimlib import *
import numpy as np
import random

class vfields(Scene):
	CONFIG = {
		"vector_field_config": {
			"delta_x": 0.5,
			"delta_y": 0.5,
		},
	}
	def construct(self): 
		text = Text("Vector Fields")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Vector Fields").shift(UP*3.5)
		self.play(FadeIn(title))

		func = lambda p: rotate_vector(p/3, PI/2) + p/9
		vector_field = VectorField(
			func,
			**self.vector_field_config
		)
		vector_field.scale(0.5)
		self.play(FadeIn(vector_field))

		
		stream_lines = StreamLines(
			func
		)
		stream_lines.scale(0.5)
		self.play(FadeIn(stream_lines))
		self.play(FadeOut(vector_field))
		




