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



class Vector3D(SGroup):
	CONFIG = {
		"end_position": [0, 0, 0],
		"start_position": [-3, 2, 0],
		"tip_scale": 1,
		"base_scale": 1,
		"tip_color": "#000000",
		"base_color": "#000000",
		"rotate_speed": 0,
		"rotate_value": 0,
		"color": RED,
		"opacity": 1,
		"gloss": 0.5,
		"shadow": 0.2,
	}

	def init_points(self):
		if (self.tip_color=="#000000"):
			self.tip_color=self.color
		if (self.base_color=="#000000"):
			self.base_color=self.color
		diffvec = [(i-j) for (i, j) in zip(self.end_position, self.start_position)]
		norm_of_diffvec = get_norm(diffvec)
		obj1 = TriangularPrism(
			width=0.3*self.tip_scale, 
			length=0.3*self.tip_scale, 
			height=0.3*self.tip_scale).shift(OUT*norm_of_diffvec)
		#Start Position
		obj2 = Cylinder(
			radius=0.2*self.base_scale, 
			height=norm_of_diffvec).shift(OUT*norm_of_diffvec/2)
		thv = Group(obj1, obj2)

		#End Position
		thv.apply_matrix(z_to_vector(diffvec))
		thv.shift(self.start_position)


		def update_vector3d(self2):
			if (self.rotate_speed != 0):
				self.rotate_value += 0.1*self.rotate_speed
			diffvecu = [(i-j) for (i, j) in zip(self.end_position, self.start_position)]
			norm_of_diffvecu = get_norm(diffvec)
			obj1u = TriangularPrism(
				width=0.3*self.tip_scale, 
				length=0.3*self.tip_scale, 
				height=0.3*self.tip_scale,
				color=self.tip_color).rotate(self.rotate_value).shift(OUT*norm_of_diffvecu)
			#Start Position
			obj2u = Cylinder(
				radius=0.2*self.base_scale, 
				height=norm_of_diffvecu,
				color=self.base_color).rotate(self.rotate_value).shift(OUT*norm_of_diffvecu/2)
			thvu = Group(obj1u, obj2u)

			#End Position
			thvu.apply_matrix(z_to_vector(diffvecu))
			thvu.shift(self.start_position)
			self2.become( thvu )
		thv.add_updater(update_vector3d)
		self.add(thv)
	def get_length(self):
		diffvec = [(i-j) for (i, j) in zip(self.end_position, self.start_position)]
		norm_of_diffvec = get_norm(diffvec)
		return norm_of_diffvec
	def get_start(self):
		return self.start_position
	def get_end(self):
		return self.end_position
	def get_tip_scale(self):
		return self.tip_scale
	def get_base_scale(self):
		return self.base_scale
	def get_rotate_speed(self):
		return self.rotate_speed

	def set_start(self, inp):
		self.start_position = inp
	def set_end(self, inp):
		self.end_position = inp
	def set_tip_scale(self, inp):
		self.tip_scale = inp
	def set_base_scale(self, inp):
		self.base_scale = inp
	def set_rotate_speed(self, inp):
		self.rotate_speed = inp



		

		
		




class test(Scene):
	def construct(self): 
		title = Text("Rotate Triangular Prism").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		for i in range(100):
			p1 = [random.randint(-50, 50)/10, random.randint(-30, 30)/10, random.randint(-50, 50)/10]
			p2 = [random.randint(-50, 50)/10, random.randint(-30, 30)/10, random.randint(-50, 50)/10]

			obj1 = Sphere(radius=0.3).shift(p1)
			obj2 = Sphere(radius=0.3).shift(p2)
			dots = Group(obj1, obj2).set_color(WHITE)

			obj = Vector3D(
				start_position=p1, 
				end_position=p2, 
				tip_scale=1, 
				base_scale=0.7, 
				color=GREEN,
				base_color=GREEN,
				tip_color="#6688FF",
				rotate_speed=0.5)
			obj.set_tip_scale(random.randint(1,15)/10)
			print(obj.get_tip_scale())
			self.add(obj)
			#self.add(dots)
			self.wait(2)
			self.remove(obj, dots)
		
		








