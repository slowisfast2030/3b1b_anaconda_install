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


        # 需要深入研究下函数实现
        axes.bind_graph_to_func(curve, lambda x: self.func(x, 0.5))

        self.wait()

        # axes.bind_graph_to_func(curve, lambda x: self.func(x, 1))

        # self.wait()

        # axes.bind_graph_to_func(curve, lambda x: self.func(x, 2))

        # self.wait()

   
    def get_axes(self):
        # 这里的坐标和宽高的关系是什么？
        axes = Axes(
            (-1, 5), (0, 4),
            width=6, height=4,
        )
        return axes

    def func(self, x, c):
        return np.exp(c * x)
