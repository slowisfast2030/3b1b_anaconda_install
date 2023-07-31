from manimlib import *
import numpy as np
import random

somecode = """
	import numpy
	def func1(obj1, obj2):
		self.cool = obj1
		self.awesome(obj2)
		self.interesting = [*obj1, **obj2]
		return obj1 == obj2
	result = "5+3" + str(5)
	def hameggs(look, at, this):
		look = at + this - look()
	for i in range(10):
		print(i)
		print(i+1)
"""

somecode2 = """
	import math
	def sin(a):
		return a - a^2/2 + a^3/3
	result = sin(a) + "Chocolate"
	def fruits(apple, banana, orange):
		return apple
	for i in range(10):
		print(i)
"""

class CodeText(Text):
	CONFIG = {
		# Mobject
		"color": WHITE,
		"height": 3,
	}
	def __init__(self, text, **config):
		super().__init__(text, **config)
	def set_color_by_t2c(self, t2c=None):
		t2c = t2c if t2c else self.t2c
		for word, color in list(t2c.items()):
			for start, end in self.find_indexes(' ' + word):
				self[start:end].set_color(color)
			for start, end in self.find_indexes(word + ' '):
				self[start:end].set_color(color)
			for start, end in self.find_indexes('\t' + word):
				self[start:end].set_color(color)
			for start, end in self.find_indexes(word + '\t'):
				self[start:end].set_color(color)
		for word in ['*']:
			for start, end in self.find_indexes(word):
				self[start:end].set_color("#bf422b")

		#color strings
		qvals = []
		for word in ['"']:
			for start, end in self.find_indexes(word):
				qvals.append(start)
		for i in range(len(qvals)-1):
			self[qvals[i]:qvals[i+1]+1].set_color("#e0c248")
		

		#color methods/functions
		mvals = []
		for word in ["("]:
			for start, end in self.find_indexes(word):
				mvals.append(start)

		for i in range(len(mvals)):
			extralocs = []
			for start, end in self.find_indexes(" "):
				if (start < mvals[i]):
					extralocs.append(start)
			extralocs = [max(extralocs)]
			for start, end in self.find_indexes("."):
				if (start < mvals[i]):
					extralocs.append(start + 1)
			extralocs = [max(extralocs)]
			for start, end in self.find_indexes("\t"):
				if (start < mvals[i]):
					extralocs.append(start)
			self[max(extralocs):mvals[i]].set_color(BLUE)

		#color defined function/methods
		fvals = []
		for word in ["def"]:
			for start, end in self.find_indexes(word + ' '):
				fvals.append(end+1)
		for i in range(len(fvals)):
			result = [k for k in mvals if k>fvals[i]]
			result = min(result)
			self[fvals[i]-1:result].set_color("#abce0d")
	def get_text(self):
		return self.text
	def get_height(self):
		return self.height
	def get_font(self):
		return self.font
	def get_font_size(self):
		return self.font_size
		



def Visualizer(code, height):
	code2 = ""
	for i in code.splitlines():
		code2 += i
		code2 += "\n\n"
	temp = CodeText(code2,
		height=height,
		t2c={"def": BLUE, "module": BLUE, "class": BLUE, "from":BLUE, "while":BLUE, 
			"import": "#bf422b", "for": "#bf422b", "=": "#bf422b", "in": "#bf422b", "return": "#bf422b", "else":"#bf422b",
			"self":"#d3870d"},
		t2s={"def": ITALIC, "for": ITALIC, " in ": ITALIC, "return": ITALIC, "class": ITALIC,"self": ITALIC,"range": ITALIC,"self": ITALIC, "print": ITALIC,},
		font="Courier"
		)
	return temp


class test(Scene):
	def construct(self): 
		self.wait(0.1)
		title = Text("Visualizer Code").shift(UP*3.5).scale(0.6)
		self.add(title)
		self.wait(0.1)

		coloredCode = Visualizer(somecode2, 4).shift(LEFT*1)
		self.add(coloredCode)




