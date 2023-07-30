import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class updatering(Scene):
	def construct(self): 
		text = Text("Updating II: Updaters")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Updating II: Updaters").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		obj1 = Text("This is text").shift(LEFT*4)
		obj2 = Square(fill_opacity=1).set_color(BLUE)
		obj3 = Circle(fill_opacity=1).set_color(YELLOW).shift(UP*2)
		obj4 = Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*1)

		x = 0
		def moveSquare(mob):
			mob.become( Square(fill_opacity=1).set_color(BLUE).shift(LEFT*x) )
		obj2.add_updater(moveSquare)
		self.add(obj2)

		while x < 3:
			x += 0.01
			self.wait(0.001)

		# 和tracker.py的代码对比起来，很有启发