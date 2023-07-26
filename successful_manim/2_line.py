import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *
from _2023.clt.main import *

# /Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master/_2023/gauss_int/herschel.py

# ok
class VariableC(InteractiveScene):
    c_values = [1.0, 0.5, -1.0, -0.7, -0.5, 0.25, -0.2, -0.4, -0.9, -0.1, 0.5, 0.3, 0.1]

    def construct(self):
        # 为什么这种写法？直接定义不好吗？
        axes = self.get_axes()
        self.add(axes)

        curve = axes.get_graph(lambda x: self.func(x, 1))
        curve.set_stroke(RED, 3)
        self.add(curve)

        label = self.get_label(axes)
        self.add(label)

        c_tracker, c_interval, c_tip, c_label = self.get_c_group()
        get_c = c_tracker.get_value

        c_interval.move_to(axes, UR)
        c_interval.shift(0.5 * DOWN)
        # 数轴、箭头、文字 
        self.add(c_interval, c_tip, c_label)

        # 需要深入研究下函数实现
        axes.bind_graph_to_func(curve, lambda x: self.func(x, get_c()))

        # Animate
        for c in self.c_values:
            self.play(c_tracker.animate.set_value(c), run_time=2)
            self.wait()

    def get_c_group(self):
        c_tracker = ValueTracker(1)
        get_c = c_tracker.get_value

        # 数轴
        c_interval = NumberLine(
            (-1, 1, 0.25), width=3, tick_size=0.05, numbers_with_elongated_ticks=[-1, 0, 1],
        )
        c_interval.set_stroke(WHITE, 1)
        c_interval.add_numbers([-1, 0, 1], num_decimal_places=1, font_size=16)
        
        # 箭头
        c_tip = ArrowTip(angle=-90 * DEGREES)
        c_tip.scale(0.5)
        c_tip.set_fill(RED)
        # 数轴也有类似于坐标轴的c2p方法，n2p将数值转换为坐标
        c_tip.add_updater(lambda m: m.move_to(c_interval.n2p(get_c()), DOWN))

        # 文字
        c_label = Tex("c = 1.00", t2c={"c": RED}, font_size=36)
        # 竟然可以tex对象的一部分是可改变的
        c_label.make_number_changable("1.00")
        # tex对象竟然是数组
        c_label[-1].scale(0.8, about_edge=LEFT)
        c_label.add_updater(lambda m: m[-1].set_value(get_c()))
        c_label.add_updater(lambda m: m.next_to(c_tip, UP, aligned_edge=LEFT))

        return [c_tracker, c_interval, c_tip, c_label]

    def get_axes(self):
        # 这里的坐标和宽高的关系是什么？
        axes = Axes(
            (-1, 5), (0, 4),
            width=6, height=4,
        )
        return axes

    def func(self, x, c):
        return np.exp(c * x)

    def get_label(self, axes):
        # 可以为个别字母设置颜色
        label = Tex("e^{cx}", t2c={"c": RED})
        # 这里的坐标是相对于axes的坐标
        label.next_to(axes.c2p(0, 2.7), RIGHT)
        return label