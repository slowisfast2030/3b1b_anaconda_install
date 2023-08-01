from manimlib import *


class test(Scene):
	def construct(self):
		obj1 = Square(fill_opacity=1).set_color(ORANGE).shift(LEFT*2)
		obj2 = Circle(fill_opacity=1).set_color(BLUE).shift(RIGHT*2)

		self.play(TransformFromCopy(obj1, obj2))
		

class test1(Scene):
    def construct(self):
        x = ValueTracker(1)
        # 合理的猜测: x的值的变化也是在插值中完成的
        """
        start对象和target对象有一个value属性
        这个value可以插值
        """
        self.play(ApplyMethod(x.increment_value, 3, run_time=5))
        print("^"*100)
        print(x.get_value())





