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
        z_range=(0, 1.5, 0.5),
        width=8,
        height=8,
        depth=3,
        center=0.5 * IN,
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

        x, y, z = axis_labels = VGroup(*map(Tex, "xyz"))
        axis_labels.use_winding_fill(False)
        x.next_to(axes.x_axis, RIGHT)
        y.next_to(axes.y_axis, UP)
        z.rotate(90 * DEGREES, RIGHT)
        z.next_to(axes.z_axis, OUT)
        axes.labels = axis_labels
        axes.add(axis_labels)

        axes.shift(center - axes.c2p(0, 0, 0))
        axes.set_flat_stroke(False)
        return axes

    def get_gaussian_graph(
        self,
        axes,
        color=interpolate_color(BLUE_E, BLACK, 0.6),
        opacity=1.0,
        shading=(0.2, 0.2, 0.4),
    ):
        graph = axes.get_graph(self.func)
        graph.set_color(color)
        graph.set_opacity(opacity)
        graph.set_shading(*shading)
        return graph

    def get_dynamic_cylinder(self, axes, r_init=1):
        cylinder = self.get_cylinder(axes, r_init)
        r_tracker = ValueTracker(r_init)
        cylinder.add_updater(lambda m: self.set_cylinder_r(
            m, axes, r_tracker.get_value()
        ))
        return cylinder, r_tracker

    def get_cylinder(
        self, axes, r,
        color=BLUE_E,
        opacity=1
    ):
        cylinder = Cylinder(color=color, opacity=opacity)
        self.set_cylinder_r(cylinder, axes, r)
        return cylinder

    def set_cylinder_r(self, cylinder, axes, r):
        r = max(r, 1e-5)
        cylinder.set_width(2 * r * axes.x_axis.get_unit_size())
        cylinder.set_depth(
            self.func(r, 0) * axes.z_axis.get_unit_size(),
            stretch=True
        )
        cylinder.move_to(axes.c2p(0, 0, 0), IN)
        return cylinder

    def get_thick_cylinder(self, cylinder, delta_r):
        radius = 0.5 * cylinder.get_width()
        outer_cylinder = cylinder.copy()
        factor = (radius + delta_r) / radius
        outer_cylinder.stretch(factor, 0)
        outer_cylinder.stretch(factor, 1)

        annulus = ParametricSurface(
            lambda u, v: (radius + u * delta_r) * np.array([math.cos(v), math.sin(v), 0]),
            u_range=(0, 1),
            v_range=(0, TAU),
        )
        annulus.match_color(cylinder)
        annulus.move_to(cylinder, OUT)

        result = Group(cylinder.copy(), annulus, outer_cylinder)
        result.clear_updaters()
        return result

    """
    class myScene(Scene):
        def construct(self):
            points = [ORIGIN, UP, RIGHT, LEFT]
            dots = VMobject()
            dots.set_points_smoothly(points)
            self.add(dots)
            self.play(Create(dots))
            self.wait()

            dots2 = VMobject()
            dots2.set_points_as_corners(points)
            self.add(dots2)
            self.play(Create(dots2))
            self.wait()
    """
    def get_x_slice(self, axes, y, x_range=(-3, 3.1, 0.1)):
        # xs是一个数组，从-3开始，到3结束，间隔0.1
        xs = np.arange(*x_range)
        ys = np.ones(len(xs)) * y
        # 这里会得到很多个点，然后用这些点构成一个平面？
        # 但这些点都在曲线上啊，怎么会构成一个平面呢？
        # 终于明白了，这里的graph本来就是一条曲线！！！
        # 为了有平面的效果，后面使用了set_fill进行了颜色填充！！！看上去就像一个平面了
        points = axes.c2p(xs, ys, self.func(xs, y))
        graph = VMobject().set_points_smoothly(points)
        #graph = VMobject().set_points_as_corners(points) 改成这种方式效果也可以
        graph.use_winding_fill(False)
        #graph.use_winding_fill(True)
        return graph

    def get_dynamic_slice(
        self,
        axes,
        stroke_color=BLUE,
        stroke_width=2,
        fill_color=BLUE_E,
        fill_opacity=0.5,
    ):
        y_tracker = ValueTracker(0)
        get_y = y_tracker.get_value

        z_unit = axes.z_axis.get_unit_size()
        # 这个函数需要深入研究：如果得到这个平面。
        x_slice = self.get_x_slice(axes, 0)
        
        # 设置属性 
        x_slice.set_stroke(stroke_color, stroke_width)
        # 下面这一行可以注释掉看看效果：将曲线显示为曲面！genius!!!
        x_slice.set_fill(fill_color, fill_opacity)

        # 添加updater
        # 这里是头一次见到为一个对象添加多个updater
        # x_slice的高度随着graph的变化而变化
        x_slice.add_updater(
            lambda m: m.set_depth(self.func(0, get_y()) * z_unit, stretch=True) # depth是高度
        )
        # x_slice的位置随着graph的变化而变化
        x_slice.add_updater(lambda m: m.move_to(axes.c2p(0, get_y(), 0), IN))

        return x_slice, y_tracker

class CartesianSlices(GaussianIntegral):
    def construct(self):
        # Setup
        frame = self.frame
        axes = self.get_axes()

        graph = self.get_gaussian_graph(axes, opacity=0.5)
        graph_mesh = SurfaceMesh(graph, resolution=(21, 21))
        graph_mesh.set_stroke(WHITE, 0.5, opacity=0.25)
        graph_mesh.set_flat_stroke(False)

        self.add(axes, graph, graph_mesh)
        # self.wait() 这一行不能加

        # Dynamic slice
        x_slice, y_tracker = self.get_dynamic_slice(axes)
        y_unit = axes.y_axis.get_unit_size()
        # 这就不是很明白了。需要搞清楚set_clip_plane的用法
        # 需要认真研究这一行：如何使得graph部分显示！！！！！
        """
        Manim中的 set_clip_plane 函数用于将3D对象裁剪到某个平面。
        当您只想显示 3D 对象的一部分或想要创建 3D 对象的横截面时，这非常有用。
        要使用 set_clip_plane ，您首先需要使用 Manim 的 ThreeDScene 类创建一个 3D 对象。
        然后，您可以在对象上调用 set_clip_plane 函数并传入法线向量和平面上的点。
        法线向量确定平面的方向，点确定平面在 3D 空间中的位置。
        """
        # 实现graph的动态效果
        graph.add_updater(lambda m: m.set_clip_plane(UP, -y_tracker.get_value() * y_unit))
        # 测试下set_clip_plane函数的效果。可以用来得到一个三维图形的横截面。
        # 下面代码可以获得垂直于z轴的平面
        #graph.add_updater(lambda m: m.set_clip_plane(OUT, -0.1 * axes.z_axis.get_unit_size()))

        x_max = axes.x_range[1]
        y_tracker.set_value(x_max)
        self.add(x_slice) # 这是一个平面，平行于xoz平面。如果不加，动态效果的边缘不好看
        self.play(
            y_tracker.animate.set_value(-x_max),
            run_time=5,
            rate_func=linear,
        )
        self.wait()

        # Show many slices
        def get_x_slices(dx=0.25):
            original_y_value = y_tracker.get_value()
            x_slices = VGroup()
            x_min, x_max = axes.x_range[:2]
            for y in np.arange(x_max, x_min, -dx):
                y_tracker.set_value(y)
                x_slice.update()
                # x_slice似乎不仅仅是一条线，还是一个平面
                x_slices.add(x_slice.copy().clear_updaters())
            x_slices.use_winding_fill(False)
            x_slices.deactivate_depth_test()
            x_slices.set_stroke(BLUE, 2, 0.5)
            x_slices.set_flat_stroke(False)
            y_tracker.set_value(original_y_value)
            return x_slices

        x_slices = get_x_slices(dx=0.25)
        self.add(x_slice, x_slices, graph, graph_mesh)
        self.play(
            FadeOut(graph, time_span=(0, 1)),
            FadeOut(x_slice, time_span=(0, 1)),
            FadeIn(x_slices, 0.1 * OUT, lag_ratio=0.1), # lag_ratio的效果就是很好
            axes.labels[2].animate.set_opacity(0),
            frame.animate.reorient(-80),
            run_time=4
        )
        self.play(
            frame.animate.reorient(-100),
            run_time=3,
        )
        self.wait()

        y_tracker.set_value(-x_max)
        self.add(x_slice, x_slices, graph, graph_mesh)
        self.play(
            FadeOut(x_slices, 0.1 * IN, time_span=(0, 2.5)),
            FadeIn(graph, time_span=(0, 2.5)),
            VFadeIn(x_slice),
            frame.animate.reorient(-15).set_height(6),
            y_tracker.animate.set_value(0), # 会导致graph发生变化
            run_time=5,
        )