import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class colorme2(Scene):
	def construct(self): 
		text = Text("Color Functions II: set_color_by_gradient").scale(0.6)
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Color Functions II: set_color_by_gradient").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		stuff = []
		stuff.append( Text("This is text").shift(LEFT*4) )
		stuff.append(  Square().set_color(YELLOW).shift(RIGHT*4) )
		stuff.append(  Rectangle().set_color(GREEN).shift(DOWN*2) )
		stuff.append(  Sphere().set_color(RED).shift(UP*2) )
		
		for i in stuff:
			i.generate_target()
		self.add(*stuff)
		self.wait(1)

		stuff[0].target.set_color_by_gradient(RED, BLUE, GREEN, YELLOW)

		for i in stuff:
			self.play(MoveToTarget(i))









