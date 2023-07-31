from manimlib import *

class grouper(Scene):
	def construct(self): 
		title = Text("Grouping MObjects")
		self.play(FadeIn(title))
		#self.wait(3)
		self.play(FadeOut(title))

		#obj1 = Dot().shift(LEFT*2)
		#obj2 = Circle().shift(RIGHT*2)
		#obj3 = Square()

		#self.add(obj1, obj2, obj3)
		#self.play(FadeIn(obj1), FadeIn(obj2), FadeIn(obj3))
		obj1 = Dot()
		obj2 = Circle()
		obj3 = Square()
		bigM = Group(obj1, obj2, obj3).arrange(RIGHT)
		self.play(FadeIn(bigM))





