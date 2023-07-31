import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class tracker(Scene):
	def construct(self): 
		text = Text("Updating III: Value Trackers")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Updating III: Value Trackers").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		obj1 = Text("This is text").shift(LEFT*4)
		obj2 = Square(fill_opacity=1).set_color(BLUE)
		obj3 = Circle(fill_opacity=1).set_color(YELLOW).shift(UP*2)
		obj4 = Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*1)

		x = ValueTracker(0)
		def moveSquare(self):
			self.become( Square(fill_opacity=1).set_color(BLUE).shift(LEFT*x.get_value()) )
		obj2.add_updater(moveSquare)
		self.add(obj2)

		# 尝试从插值的角度理解AppyMethod
		# Transform类从表面上看是从一个对象变成另一个对象，即obj1 ---> obj2
		# 但，本质上是state1 ---> state2
		# 这里的state可以来源于两个不同的对象，也可以来源于同一个对象
		# 这里的ApplyMethod，本质上是同一个obj的state1 ---> state2
		self.play(ApplyMethod(x.increment_value, 3, run_time=5))