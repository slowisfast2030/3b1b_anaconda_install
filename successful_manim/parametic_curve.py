import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *


class test(InteractiveScene):

    def construct(self):
        # 为什么这种写法？直接定义不好吗？
        axes = self.get_axes()
        self.add(axes)
        # 设置曲线的采样点
        axes.num_sampled_graph_points_per_tick = 1

        curve = axes.get_graph(lambda x: self.func(x, 0.5), use_smoothing=False)
        curve.set_stroke(RED, 3)
        self.add(curve)
        self.wait()

        # a = MotionMobject(axes)
        # self.add(a)
        # self.wait()

    def get_axes(self):
        axes = Axes(
            (-1, 5), (0, 4),
            width=6, height=4,
        )
        return axes

    def func(self, x, c):
        return np.exp(c * x)