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

class CartesianSlices(GaussianIntegral):
    def construct(self):
        # Setup
        frame = self.frame
        axes = self.get_axes()

        graph = self.get_gaussian_graph(axes)
        graph_mesh = SurfaceMesh(graph, resolution=(21, 21))
        graph_mesh.set_stroke(WHITE, 0.5, opacity=0.25)
        graph_mesh.set_flat_stroke(False)

        self.add(axes, graph, graph_mesh)
        # self.wait() 这一行不能加

        # Dynamic slice
        x_slice, y_tracker = self.get_dynamic_slice(axes)
        y_unit = axes.y_axis.get_unit_size()
        # 这就不是很明白了。需要搞清楚set_clip_plane的用法
        graph.add_updater(lambda m: m.set_clip_plane(UP, -y_tracker.get_value() * y_unit))

        x_max = axes.x_range[1]
        y_tracker.set_value(x_max)
        self.add(x_slice) # 这是一条线，平行于xoz平面。如果不加，动态效果的边缘不好看
        self.play(
            y_tracker.animate.set_value(-x_max),
            run_time=5,
            rate_func=linear,
        )
        self.wait()