import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class targetmaker(Scene):
	def construct(self): 
		text = Text("Generating Targets")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Generating Targets").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		obj1 = Text("This is text").shift(LEFT*4)
		obj2 = Square(fill_opacity=1).set_color(BLUE)
		obj3 = Circle(fill_opacity=1).set_color(YELLOW).shift(UP*2)
		obj4 = Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*1)

		self.add(obj2)
		self.wait(1)
		obj2.generate_target()
		obj2.target.scale(0.5).set_color(YELLOW).shift(LEFT*3) #Important, type .target
		self.play(MoveToTarget(obj2))