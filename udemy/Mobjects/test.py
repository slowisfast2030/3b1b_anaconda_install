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
		
		




