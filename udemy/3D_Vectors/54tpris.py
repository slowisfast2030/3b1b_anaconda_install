from manimlib import *
import numpy as np
import random

class Rectangle3D(Surface):
	CONFIG = {
		"length": 1,
		"width": 2,
		"u_range": (-1, 1),
		"v_range": (-1, 1),
		"resolution": (2, 2),
	}

	def init_points(self):
		super().init_points()

	def uv_func(self, u, v):
		return [u*self.width, v*self.length, 0]


class Triangle3D(Surface):
	CONFIG = {
		"p0": [0, 0, 0],
		"p1": [1, 0, 0],
		"p2": [1, 1, 0],
		"u_range": (-1, 1),
		"v_range": (-1, 1),
		"resolution": (2, 2),
	}

	def init_points(self):
		super().init_points()

	def uv_func(self, u, v):
		p0 = self.p0
		p1 = self.p1
		p2 = self.p2

		if (u + v <= 1):
			return [
			(1-u-v)*p0[0] + u*p1[0] + v*p2[0], 
			(1-u-v)*p0[1] + u*p1[1] + v*p2[1], 
			(1-u-v)*p0[2] + u*p1[2] + v*p2[2]]
		else:
			return [p0[0], p0[1], p0[2]]


class TriangularPrism(SGroup):
	CONFIG = {
		"color": RED,
		"opacity": 1,
		"gloss": 0.5,
		"width": 1,
		"length": 1,
		"height": 1
	}

	def init_points(self):
		base = Rectangle3D(width=self.width, length=self.length)
		self.add(base)

		t1 = Triangle3D(
			p0=[-self.width/2, -self.length/2, 0], 
			p1=[self.width/2, -self.length/2, 0], 
			p2=[0, 0, self.height]).shift(RIGHT*self.width + OUT*self.height)
		self.add(t1)

		t2 = Triangle3D(
			p0=[-self.width/2, self.length/2, 0], 
			p1=[self.width/2, self.length/2, 0], 
			p2=[0, 0, self.height]).shift(RIGHT*self.width + OUT*self.height)
		self.add(t2)

		t3 = Triangle3D(
			p0=[self.width/2, -self.length/2, 0], 
			p1=[self.width/2, self.length/2, 0], 
			p2=[0, 0, self.height]).shift(UP*self.length + OUT*self.height)
		self.add(t3)

		t4 = Triangle3D(
			p0=[-self.width/2, -self.length/2, 0], 
			p1=[-self.width/2, self.length/2, 0], 
			p2=[0, 0, self.height]).shift(UP*self.length + OUT*self.height)
		self.add(t4)
		




class test(Scene):
	def construct(self): 
		title = Text("Triangular Prism").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		obj1 = TriangularPrism(
			length=2, 
			width=0.5, 
			height=1
			)
		self.add(obj1)

		obj2 = Cube().shift(IN*1)
		self.add(obj2)
		
		



