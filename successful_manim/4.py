import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *
from _2023.convolutions2.continuous import *
from _2023.clt.main import *

# /Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master/_2023/gauss_int/integral.py

class AntiDerivative(InteractiveScene):
    def construct(self):
        # Add both planes
        x_min, x_max = (-3, 3)
        planes = VGroup(*(
            NumberPlane(
                (x_min, x_max), (0, 2),
                width=5.5, height=2.75,
                background_line_style=dict(stroke_color=GREY, stroke_width=1, stroke_opacity=1.0),
                faded_line_ratio=3,
            ) # 不得不说，这个NumberPlane很漂亮。
            for x in range(2)
        ))
        planes.arrange(DOWN, buff=LARGE_BUFF)
        planes.to_corner(UL)
        self.add(planes)

        # Titles
        titles = VGroup(
            Tex("f(x) = e^{-x^2}", font_size=66),
            Tex(R"F(x) = \int_0^x e^{-t^2} dt"),
        )
        for title, plane in zip(titles, planes):
            title.next_to(plane, RIGHT)

        ad_word = Text("Antiderivative")
        ad_word.next_to(titles[1], UP, MED_LARGE_BUFF)
        VGroup(ad_word, titles[1]).match_y(planes[1]) # match_y()是什么意思？这里的VGroup有什么用吗？

        self.add(titles)
        self.add(ad_word)

        # High graph
        x_tracker = ValueTracker(0)
        get_x = x_tracker.get_value
        high_graph = planes[0].get_graph(lambda x: np.exp(-x**2))
        high_graph.set_stroke(BLUE, 3)

        # 一开始以为area随着graph的变化而变化，但实际上area和graph同时随着x的变化而变化
        # 进而导致area和graph的变化是一致的，看上去就像是area随着graph的变化而变化
        high_area = high_graph.copy()

        # 这个函数真是不好理解
        # 即使不理解，但是可以模仿这个函数的用法
        """
        from manim import *

        class BecomeScene(Scene):
            def construct(self):
                circ = Circle(fill_color=RED, fill_opacity=0.8)
                square = Square(fill_color=YELLOW, fill_opacity=0.2)
                self.add(circ)
                self.wait(1)
                circ.become(square)
                self.wait(1)
                circ.pointwise_become_partial(square, 0, 0.6)
                self.wait(0.5)
        """
        """
        终于搞明白update_area函数的细节了!!!哈哈哈
        这里的关键是明白become()和pointwise_become_partial()的区别和联系

        become()函数的作用是将一个VMobject变成另一个VMobject
        pointwise_become_partial()函数的作用是将一个VMobject的一部分变成另一个VMobject的一部分

        遗留问题：
        pointwise_become_partial()函数是部分变换，但是部分变换可以有无穷种方式
        如何指定部分变换的方式？从上到下 or 从左到右？
        """
        """
        class MyScene(Scene):
        def construct(self):
            # Create a VMobject
            my_vmobject = VMobject()

            # Add points to the VMobject
            my_vmobject.set_points_as_corners([ORIGIN, RIGHT, UP, LEFT-1, LEFT+DOWN+RIGHT])
            self.add(my_vmobject)
            self.wait(1)
            print("*"*100)
            print(my_vmobject.get_last_point())

            # Add a line to the VMobject
            my_vmobject.add_line_to(2*RIGHT)

            # Display the VMobject on the screen
            self.play(Create(my_vmobject))
            self.wait()
        """
        def update_area(area: VMobject):
            x = get_x()
            # 这一行不是很明白。为什么要用become()函数？用copy()函数不行吗？实际执行的结果是不行的。
            area.become(high_graph) # 如果manimgl版本的源码不好懂，可以查看manimce版本的实现。manimce版本的实现更加清晰
            #area = high_graph.copy()
            area.set_stroke(width=0)
            area.set_fill(BLUE, 0.5) # 对一个graph进行填充，会给graph和坐标轴之间上色

            # 这一行什么意思？
            area.pointwise_become_partial( # 很庆幸，在manimce版本中也有实现。不过没有给示例，所以还是不太清楚
                high_graph, 0, inverse_interpolate(x_min, x_max, x) # inverse_interpolate()函数的返回结果是一个float
            )
            
            # 这两行不是很明白。add_line_to()函数是什么意思？有没有办法能够测试一下？
            area.add_line_to(planes[0].c2p(x, 0)) # 这一行不能注释。否则会有一条线倾斜着改变矩形的大小
            area.add_line_to(planes[0].c2p(x_min, 0)) # 这一行注释掉似乎影响不大
            #print("*"*200)
            #print(area.get_last_point())
            return area

        high_area.add_updater(update_area) # x.add_updater(func)，func的参数是x本身

        # 这里需要深刻思考下high_area的实现
        self.add(high_graph, high_area)
        # self.add(high_area)

        # Low graph
        dist = scipy.stats.norm(0, 1)
        low_graph = planes[1].get_graph(lambda x: math.sqrt(PI) * dist.cdf(x))
        low_graph.set_stroke(YELLOW, 2)
        low_dot = GlowDot()
        low_dot.add_updater(lambda m: m.move_to(planes[1].i2gp(get_x(), low_graph))) # dot在curve上移动

        low_line = always_redraw(lambda: DashedLine(
            planes[1].c2p(get_x(), 0), planes[1].i2gp(get_x(), low_graph), # 这里可以更加清楚的看到c2p和i2gp的用法
        ).set_stroke(WHITE, 2))

        self.add(low_graph, low_dot, low_line)

        # Animations
        for value in [1.5, -2, -1, 1, -0.5, 0.5, 3.0, -1.5]:
            self.play(x_tracker.animate.set_value(value), run_time=3)
            self.wait()
