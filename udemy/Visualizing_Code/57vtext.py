from manimlib import *
import numpy as np
import random

somecode = """
	import numpy
	def func1(obj1, obj2):
		return obj1 == obj2
	result = "5+3" + str(5)
	for i in range(10):
		print(i)
"""

class CodeText(Text):
	def __init__(self, text, **config):
		super().__init__(text, **config)
	def set_color_by_t2c(self, t2c=None):
		t2c = t2c if t2c else self.t2c
		for word, color in list(t2c.items()):
			for start, end in self.find_indexes(word + ' '):
				self[start:end].set_color(color)
			for start, end in self.find_indexes(' ' + word):
				self[start:end].set_color(color)

def Visualizer(code, height):
	code2 = ""
	for i in code.splitlines():
		code2 += i
		code2 += "\n\n"
	temp = CodeText(code2,
		height=height,
		t2c={"def": BLUE, "module": BLUE, "class": BLUE, "from":BLUE, "while":BLUE, 
			"import": PURPLE, "for": PURPLE, "=": PURPLE, "in": PURPLE, "return": PURPLE},
		font="Arial"
		)
	return temp


class test(Scene):
	def construct(self): 
		title = Text("VisualizerCode").shift(UP*3.5).scale(0.6)
		self.add(title)
		self.add(Visualizer(somecode, 3).shift(LEFT*3))
		



