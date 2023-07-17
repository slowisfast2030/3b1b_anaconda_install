import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

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
        axes: ThreeDAxes,
        color=interpolate_color(BLUE_E, BLACK, 0.6),
        opacity=1.0,
        shading=(0.2, 0.2, 0.4),
    ):
        graph = axes.get_graph(self.func)
        graph.set_color(color)
        graph.set_opacity(opacity)
        graph.set_shading(*shading)
        return graph
    
    def get_x_slice(self, axes, y, x_range=(-3, 3.1, 0.1)):
        xs = np.arange(*x_range)
        ys = np.ones(len(xs)) * y
        points = axes.c2p(xs, ys, self.func(xs, y))
        graph = VMobject().set_points_smoothly(points)
        graph.use_winding_fill(False)
        return graph


class CylinderSlices(GaussianIntegral):
    def construct(self):
        # Setup
        frame = self.frame
        axes = self.get_axes()

        graph = self.get_gaussian_graph(axes)
        graph.set_opacity(0.8)
        graph.always_sort_to_camera(self.camera)

        graph_mesh = SurfaceMesh(graph, resolution=(21, 21))
        graph_mesh.set_stroke(WHITE, 0.5, opacity=0.25)
        graph_mesh.set_flat_stroke(False)

        self.add(axes)

        # Animate in by rotating e^{-x^2}
        bell_halves = Group(*(
            ParametricSurface(
                lambda r, theta: np.array(
                    [r * np.cos(theta), r * np.sin(theta), np.exp(-r**2)
                ]),
                u_range=(0, 3),
                v_range=v_range,
            )
            for v_range in [(0, PI), (PI, TAU)]
        ))
        
        for half in bell_halves:
            #half.match_style(graph)
            half.set_opacity(0.5)

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

        axes.save_state()
        frame.reorient(0, 90)
        frame.move_to(OUT + 2 * UP)
        axes.y_axis.set_opacity(0)
        axes.labels.set_opacity(0)
        self.play(
            ShowCreation(bell2d),
            Write(label2d)
        )
        self.wait()

        self.play(
            ShowCreation(bell_halves[0]),
            ShowCreation(bell_halves[1]),
            Rotate(bell2d, PI, axis=OUT, about_point=axes.c2p(0, 0, 0)),
            frame.animate.move_to(ORIGIN).reorient(-20, 70),
            Restore(axes),
            TransformMatchingTex(label2d.copy(), label3d, time_span=(0, 2)),
            label2d.animate.next_to(label3d, UP, MED_LARGE_BUFF, LEFT),
            run_time=6
        )
        self.wait()
        self.play(
            FadeOut(bell_halves, 0.01 * IN),
            FadeOut(bell2d, 0.1 * IN),
            FadeIn(graph, 0.01 * IN),
        )
        self.play(Write(graph_mesh, stroke_width=1, lag_ratio=0.01))
        self.wait()