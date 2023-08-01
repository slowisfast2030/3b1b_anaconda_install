from manimlib import *


class test(Scene):
	def construct(self):
		obj1 = Square(fill_opacity=1).set_color(ORANGE).shift(LEFT*2)
		obj2 = Circle(fill_opacity=1).set_color(BLUE).shift(RIGHT*2)

		self.play(TransformFromCopy(obj1, obj2))
		

class test1(Scene):
    def construct(self):
        x = ValueTracker(1)
        self.play(ApplyMethod(x.increment_value, 3, run_time=5))
        print("^"*100)
        print(x.get_value())





