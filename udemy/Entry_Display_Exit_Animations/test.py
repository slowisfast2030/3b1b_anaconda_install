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

class test2(Scene):
    def construct(self):
        c = Circle().set_color(RED)
        s = Square().set_color(BLUE)
        t = Triangle().set_color(GREEN)
        c.add(s, t)
        self.play(ShowCreation(c, lag_ratio=0, run_time=3))
        print("\n", "-"*100)
        print(c.submobjects)
        print("-"*100)

class test3(Scene):
    def construct(self):
        c = Circle().set_color(RED)
        s = Square().set_color(BLUE)
        t = Triangle().set_color(GREEN)
        c.add(s, t)
        self.play(Uncreate(c, lag_ratio=0, run_time=3, remover=True))
        self.wait()
        print("\n", "-"*100)
        print(c.submobjects)
        print("-"*100)




