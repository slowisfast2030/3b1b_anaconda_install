from manimlib import *
import numpy as np
import random

class bullets(Scene):
	def construct(self): 
		text = Text("Windowed Scenes & BulletedList")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Windowed Scenes & BulletedList").shift(UP*3.5)#.scale(0.6)
		self.play(FadeIn(title))

		#While editing video, 
		#put animation of another scene here!
		screen_rect = ScreenRectangle(height=4) 
		screen_rect.shift(LEFT * 2.5)

		topics = BulletedList(
			"Episode 1",
			"Prolog 2",
			"Tape Log 3",
			"VLOG 4",
			"Chocolate cupcakes",
			"Milk, Cheese",
		)
		#no var attached to group
		Group(screen_rect, topics).arrange(RIGHT, buff=0.5)
		self.play(ShowCreation(screen_rect))
		for i in topics:
			self.play(Write(i))


		





