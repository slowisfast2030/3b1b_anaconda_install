import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *
from _2023.convolutions2.continuous import *
from _2023.clt.main import *

# /Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master/_2023/gauss_int/integral.py

class GaussianIntegral(ThreeDScene, InteractiveScene):
    def func(self, x, y):
        return np.exp(-x**2 - y**2)

    def get_axes(
        self,
        x_range=(-3, 3),
        y_range=(-3, 3),
        z_range=(0, 1.5, 0.5), # 坐标轴上的刻度，并不是实际的长度。可以认为坐标轴的刻度是虚拟的长度。需要乘以单位长度。
        width=8,
        height=8,
        depth=3, # 坐标轴的高度（视觉）
        center=0.5 * IN, # 这个参数是什么意思？
        include_plane=False
    ):
        axes = ThreeDAxes(
            x_range, y_range, z_range,
            width=width, height=height, depth=depth
        ) 
        axes.set_stroke(GREY_C)

        if include_plane:
            plane = NumberPlane(
                x_range, y_range,
                width=width, height=height,
                background_line_style=dict(
                    stroke_color=GREY_C,
                    stroke_width=1,
                ),
            )
            plane.faded_lines.set_stroke(opacity=0.5)
            plane.shift(0.01 * IN)
            axes.plane = plane
            axes.add(plane)

        """
        map函数语法: map(function, iterable, …)

        def square(x):
            return x ** 2

        lst = [1, 2, 3, 4, 5]
        result = map(square, lst) # 返回一个map对象
        print(list(result)) # 使用list函数将map对象转换为列表
        """
        # 坐标轴上的标签不是axes自带的么？需要自定义？
        # 看了axes的源码后，确实自带标签函数：add_axis_labels()
        # 函数实现方式和下面代码类似
        x, y, z = axis_labels = VGroup(*map(Tex, "xyz")) # 坐标轴标签是Tex对象，不是Text对象
        axis_labels.use_winding_fill(False)
        x.next_to(axes.x_axis, RIGHT)
        y.next_to(axes.y_axis, UP)
        z.rotate(90 * DEGREES, RIGHT)
        z.next_to(axes.z_axis, OUT)
        axes.labels = axis_labels # 这里是为axes添加了一个属性
        axes.add(axis_labels)

        axes.shift(center - axes.c2p(0, 0, 0)) # shift和move_to的区别是什么？前者给出的是相对坐标，后者给出的是绝对坐标
        axes.set_flat_stroke(False)
        return axes

    def get_x_slice(self, axes: ThreeDAxes, y, x_range=(-3, 3.1, 0.1)):
        # xs是一个数组，从-3开始，到3结束，间隔0.1
        xs = np.arange(*x_range)
        ys = np.ones(len(xs)) * y
        # 这里会得到很多个点，然后用这些点构成一个平面？
        # 但这些点都在曲线上啊，怎么会构成一个平面呢？
        # 终于明白了，这里的graph本来就是一条曲线！！！
        # 为了有平面的效果，后面使用了set_fill进行了颜色填充！！！看上去就像一个平面了
        points = axes.c2p(xs, ys, self.func(xs, y)) # 可以和ParametricSurface函数的实现进行对比。本质一样！
        # 这种获取曲线的方法真是暴力
        graph :VMobject = VMobject().set_points_smoothly(points) # 一切二维或者三维的对象都是由点构成的
        print(graph.get_points())
        #graph = VMobject().set_points_as_corners(points) #改成这种方式效果也可以
        graph.use_winding_fill(False)
        #graph.use_winding_fill(True)
        return graph
    
class CartesianSlices(GaussianIntegral):
    def construct(self):
        # Setup
        axes = self.get_axes(include_plane=True)
        x_slice = self.get_x_slice(axes, -1)
        self.add(x_slice, axes)
        self.wait(3)