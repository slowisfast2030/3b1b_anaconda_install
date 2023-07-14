import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *
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

        # 这里定义了xyz轴的标签
        # 不过后面没有用
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
        # 下面几个参数反应了图像的颜色、透明度、阴影
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

    def get_x_slice(self, axes, y, x_range=(-3, 3.1, 0.1)):
        xs = np.arange(*x_range)
        ys = np.ones(len(xs)) * y
        points = axes.c2p(xs, ys, self.func(xs, y))
        graph = VMobject().set_points_smoothly(points)
        graph.use_winding_fill(False)
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
        x_slice = self.get_x_slice(axes, 0)
        x_slice.set_stroke(stroke_color, stroke_width)
        x_slice.set_fill(fill_color, fill_opacity)
        x_slice.add_updater(
            lambda m: m.set_depth(self.func(0, get_y()) * z_unit, stretch=True)
        )
        x_slice.add_updater(lambda m: m.move_to(axes.c2p(0, get_y(), 0), IN))

        return x_slice, y_tracker

"""
启发：
1.本来是三维的坐标轴，通过调整camera的角度，变成了二维的坐标轴
2.在上述二维的坐标轴上，画出了二维的高斯函数图像
3.所有camera的操作都是通过frame来实现的
4.这里把3维通过视角转换变成了2维，也可以反过来
"""
class CylinderSlices(GaussianIntegral):
    def construct(self):
        # Setup
        frame = self.frame
        axes = self.get_axes()

        # graph可以单独显示，也可以用来生成graph_mesh
        graph = self.get_gaussian_graph(axes)
        graph.set_opacity(0.8)
        # 什么意思？
        graph.always_sort_to_camera(self.camera) # 对比了注释后的视频，没发现区别

        graph_mesh = SurfaceMesh(graph, resolution=(21, 21)) # 分辨率越高，网格越密集
        graph_mesh.set_stroke(WHITE, 0.5, opacity=0.25) #opacity=0全透明，opacity=1不透明
        graph_mesh.set_flat_stroke(False)

        self.add(axes)

        # xoz平面的曲线
        bell2d = self.get_x_slice(axes, 0)
        bell2d.set_stroke(TEAL, 3)
        kw = dict(t2c={"x": BLUE, "y": YELLOW})
        label2d, label3d = func_labels = VGroup(
            Tex("f_1(x) = e^{-x^2}", **kw),
            Tex("f_2(x, y) = e^{-(x^2 + y^2)}", **kw),
        )
        for label in func_labels:
            label.fix_in_frame()
            label.move_to(4 * LEFT + 2 * UP)
        # 需要分开两个label，重合了
        label.move_to(4 * LEFT + UP)

        # 这一行代码作用？
        axes.save_state()
        # frame的角度
        frame.reorient(0, 90)
        # frame在平面的位置
        frame.move_to(OUT + 2 * UP)

        # 之前还好奇：y轴怎么不见了
        axes.y_axis.set_opacity(0)
        # xyz轴的标签
        axes.labels.set_opacity(1)
        self.play(
            ShowCreation(bell2d),
            Write(label2d)
        )
        self.wait()

        self.play(Write(graph_mesh, stroke_width=1, lag_ratio=0.01))
        self.wait()

        # Rotate the frame
        self.play(
            frame.animate.set_theta(20 * DEGREES), #调整camera的角度 
            rate_func=there_and_back,
            run_time=5,
        )

        # Reposition to 2d view
        # 下面这几行有什么用？
        frame.save_state()
        graph_mesh.save_state()
        func_labels.use_winding_fill(False)

        # 这几个动作是同时进行的吗？
        self.play(
            #frame.animate.reorient(0, 0).set_height(10).move_to(1.5 * LEFT).set_field_of_view(1 * DEGREES), # 调整视角为俯视图
            frame.animate.reorient(0, 0).set_height(10).move_to(1.5 * LEFT).set_field_of_view(1 * DEGREES),
            graph.animate.set_opacity(0.25), # 这一行很重要，显示出了图像，而不是只有网格
            func_labels.animate.scale(0.75).to_corner(UL),
            graph_mesh.animate.set_stroke(width=1), # 线宽
            run_time=3,
        )

        self.wait()

        # Explain meaning of r
        x, y = (1.5, 0.75)
        # 这里的axes是三维的，为何参数只有两个？
        dot = Dot(axes.c2p(x, y), fill_color=RED)
        dot.set_stroke(WHITE, 0.5) # 外围的圆圈
        coords = Tex("(x, y)", font_size=36)
        coords.next_to(dot, UR, SMALL_BUFF)

        x_line = Line(axes.get_origin(), axes.c2p(x, 0, 0))
        y_line = Line(axes.c2p(x, 0, 0), axes.c2p(x, y, 0))
        r_line = Line(axes.c2p(x, y, 0), axes.get_origin())
        x_line.set_stroke(BLUE, 3)
        y_line.set_stroke(YELLOW, 3)
        r_line.set_stroke(RED, 3)
        lines = VGroup(x_line, y_line, r_line)
        labels = VGroup(*map(Tex, "xyr"))
        for label, line in zip(labels, lines):
            label.match_color(line)
            label.scale(0.85)
            label.next_to(line.get_center(), rotate_vector(line.get_vector(), -90 * DEGREES), SMALL_BUFF)

        self.add(dot, coords, set_depth_test=False)
        self.play(
            FadeIn(dot, scale=0.5),
            FadeIn(coords),
        )
        for line, label in zip(lines, labels):
            self.add(line, label, dot, set_depth_test=False)
            self.play(
                ShowCreation(line),
                Write(label),
            )

        # Plug in r
        r_label_rect = SurroundingRectangle(labels[2], buff=SMALL_BUFF)
        r_label_rect.set_stroke(RED, 2)
        arrow = Arrow(r_label_rect, axes.c2p(-3, 3, 0) + 3.2 * LEFT + 0.25 * UP, path_arc=45 * DEGREES)
        arrow.set_stroke(RED)

        self.always_depth_test = False
        self.play(ShowCreation(r_label_rect)) # 效果在哪里？
        self.play(ShowCreation(arrow))
        self.wait()

        # Show Pythagorean equations
        r_func = Tex("= e^{-r^2}", t2c={"r": RED})
        r_func.match_height(label2d["= e^{-x^2}"])
        r_func.next_to(label3d, RIGHT, MED_SMALL_BUFF, UP)
        r_func.fix_in_frame()

        r_rect = SurroundingRectangle(r_func["r^2"], buff=0.025)
        xy_rect = SurroundingRectangle(label3d["x^2 + y^2"], buff=0.025)
        VGroup(r_rect, xy_rect).set_stroke(TEAL, 1)
        VGroup(r_rect, xy_rect).fix_in_frame()

        pythag = Tex("x^2 + y^2 = r^2", t2c={"x": BLUE, "y": YELLOW, "r": RED})
        pythag.next_to(label3d, DOWN, buff=2.0, aligned_edge=LEFT)
        pythag.fix_in_frame()

        self.play(
            FadeTransform(label2d["= e^{-x^2}"].copy(), r_func),
            FadeOut(arrow, scale=0.8, shift=DR + RIGHT),
            FadeOut(r_label_rect)
        )
        self.wait()
        line_copies = lines.copy()
        self.add(*line_copies, set_depth_test=False)
        self.play(
            *(
                VShowPassingFlash(line.insert_n_curves(20).set_stroke(width=8), time_width=1.5)
                for line in line_copies
            ),
            *map(ShowCreation, lines)
        )
        self.play(
            FadeTransform(r_func["r^2"][0].copy(), pythag["r^2"]),
            FadeTransform(label3d["x^2 + y^2"][0].copy(), pythag["x^2 + y^2"]),
            Write(pythag["="]),
        )
        self.wait()
        self.wait()
        self.play(ShowCreation(xy_rect))
        self.wait()
        self.play(Transform(xy_rect, r_rect))
        self.play(FadeOut(xy_rect))