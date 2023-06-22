import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

# 除了上面这种方式，有没有更加优雅的方式
import sys
print(sys.path)

from manim_imports_ext import *
from _2023.clt.main import *

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
        # bell_halves = Group(*(
        #     axes.get_parametric_surface(
        #         lambda r, theta: np.array(
        #             [r * np.cos(theta), r * np.sin(theta), np.exp(-r**2)
        #         ]),
        #         u_range=(0, 3),
        #         v_range=v_range,
        #     )
        #     for v_range in [(0, PI), (PI, TAU)]
        # ))
        
            
        



        # for half in bell_halves:
        #     half.match_style(graph)
        #     half.set_opacity(0.5)

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

        # self.play(
        #     ShowCreation(bell_halves[0]),
        #     ShowCreation(bell_halves[1]),
        #     Rotate(bell2d, PI, axis=OUT, about_point=axes.c2p(0, 0, 0)),
        #     frame.animate.move_to(ORIGIN).reorient(-20, 70),
        #     Restore(axes),
        #     TransformMatchingTex(label2d.copy(), label3d, time_span=(0, 2)),
        #     label2d.animate.next_to(label3d, UP, MED_LARGE_BUFF, LEFT),
        #     run_time=6
        # )
        self.wait()
        # self.play(
        #     FadeOut(bell_halves, 0.01 * IN),
        #     FadeOut(bell2d, 0.1 * IN),
        #     FadeIn(graph, 0.01 * IN),
        # )
        self.play(Write(graph_mesh, stroke_width=1, lag_ratio=0.01))
        self.wait()

        # Rotate the frame
        self.play(
            frame.animate.set_theta(20 * DEGREES),
            rate_func=there_and_back,
            run_time=30,
        )

        # Reposition to 2d view
        frame.save_state()
        graph_mesh.save_state()
        func_labels.use_winding_fill(False)
        self.play(
            frame.animate.reorient(0, 0).set_height(10).move_to(1.5 * LEFT).set_field_of_view(1 * DEGREES),
            graph.animate.set_opacity(0.25),
            func_labels.animate.scale(0.75).to_corner(UL),
            graph_mesh.animate.set_stroke(width=1),
            run_time=3,
        )

        # Explain meaning of r
        x, y = (1.5, 0.75)
        dot = Dot(axes.c2p(x, y), fill_color=RED)
        dot.set_stroke(WHITE, 0.5)
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
        self.play(ShowCreation(r_label_rect))
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

        functions = VGroup(label2d, label3d, r_func)
        functions.fix_in_frame()

        # Emphasize rotational symmetry
        self.always_depth_test = True
        x_label, y_label, r_label = labels
        self.play(
            *map(FadeOut, [x_line, y_line, x_label, y_label, pythag])
        )

        def get_circle(point, z_shift=0.02):
            origin = axes.c2p(0, 0, 0)
            point[2] = origin[2]
            radius = get_norm(point - origin)
            circle = Circle(radius=radius, n_components=96)
            x = axes.x_axis.p2n(point)
            y = axes.y_axis.p2n(point)
            circle.move_to(axes.c2p(0, 0, self.func(x, y) + z_shift))
            circle.set_stroke(RED, 2)
            circle.rotate(np.arctan2(y, x))
            circle.set_flat_stroke(False)
            return circle

        r_label.add_updater(lambda m: m.next_to(r_line.get_center(), UL, SMALL_BUFF))
        dot.add_updater(lambda m: m.move_to(r_line.get_start()))
        coords.add_updater(lambda m: m.next_to(dot, UR, SMALL_BUFF))
        circle = get_circle(r_line.get_start())

        self.play(
            Rotate(r_line, TAU, about_point=axes.get_origin()),
            ShowCreation(circle),
            frame.animate.reorient(30, 60).move_to(ORIGIN).set_height(8).set_field_of_view(45 * DEGREES),
            Restore(graph_mesh),
            run_time=7,
        )
        self.wait()
        self.play(
            r_line.animate.scale(0.1, about_point=axes.get_origin()),
            UpdateFromFunc(circle, lambda c: c.replace(get_circle(r_line.get_start()))),
            rate_func=there_and_back,
            run_time=8,
        )
        self.wait()
        self.play(*map(FadeOut, [r_line, dot, r_label, coords, circle]))

        # Dynamic cylinder
        cylinder, r_tracker = self.get_dynamic_cylinder(axes)
        delta_r = 0.1
        cylinders = Group(*(
            self.get_cylinder(axes, r, opacity=0.5)
            for r in np.arange(0, 3, delta_r)
        ))

        r_tracker.set_value(0)
        self.add(cylinder, cylinders, graph, graph_mesh)
        self.play(
            graph.animate.set_opacity(0.1).set_anim_args(time_span=(0, 2)),
            FadeIn(cylinders, lag_ratio=0.9),
            r_tracker.animate.set_value(3).set_anim_args(
                rate_func=linear,
                time_span=(0.5, 10),
            ),
            frame.animate.reorient(-15, 75).set_height(5.5),
            run_time=10,
        )
        self.wait()

        # Isolate one particular cylinder
        self.play(
            r_tracker.animate.set_value(0.7),
            cylinders.animate.set_opacity(0.1),
            frame.animate.reorient(-27, 71),
            run_time=3,
        )

        # Unwrap cylinder
        axes.labels[2].set_opacity(0)
        R = cylinder.get_width() / 2
        rect = Square3D(resolution=cylinder.resolution)
        rect.set_width(TAU * R)
        rect.set_height(cylinder.get_depth(), stretch=True)
        rect.match_color(cylinder)
        rect_top = Line(rect.get_corner(UL), rect.get_corner(UR))
        rect_top.set_stroke(RED, 3)
        rect_side = Line(rect.get_corner(DL), rect.get_corner(UL))
        rect_side.set_stroke(PINK, 3)
        VGroup(rect_top, rect_side).set_flat_stroke(False)
        rect_group = Group(rect, rect_top, rect_side)
        rect_group.apply_matrix(frame.get_orientation().as_matrix())
        rect_group.next_to(cylinder, [1, 0, 1], LARGE_BUFF)

        eq_kw = dict(
            font_size=35,
            t2c={"{r}": RED},
        )
        area_eq1 = TexText("Area = (Circumference)(Height)", **eq_kw)
        area_eq2 = TexText(R"Area = $2 \pi {r} \cdot e^{-{r}^2}$", **eq_kw)
        for eq in area_eq1, area_eq2:
            eq.fix_in_frame()
            eq.to_corner(UL)
        area_eq1.shift(area_eq2[0].get_center() - area_eq1[0].get_center())

        self.add(functions)
        functions.fix_in_frame()
        functions.deactivate_depth_test()
        functions.use_winding_fill(False)
        self.play(
            FadeIn(area_eq1, DOWN),
            functions.animate.shift(1.5 * DOWN).scale(0.7, about_edge=DL).set_fill(opacity=0.75)
        )
        self.wait()

        pre_rect = cylinder.copy()
        pre_rect.clear_updaters()
        self.add(pre_rect, graph)
        self.play(
            pre_rect.animate.scale(0.95).next_to(cylinder, OUT, buff=1.0),
            frame.animate.set_height(7).move_to([1.0, 0.15, 1.0]),
            run_time=2,
        )
        self.play(ReplacementTransform(pre_rect, rect), run_time=2)
        self.wait()

        # Show cylinder area
        circle = get_circle(cylinder.get_points()[0], z_shift=0)
        height_line = Line(cylinder.get_corner(IN + DOWN), cylinder.get_corner(OUT + DOWN))
        height_line.set_stroke(PINK, 3)
        height_line.set_flat_stroke(False)

        circ_brace = Brace(area_eq2[R"2 \pi {r}"], DOWN, SMALL_BUFF)
        height_brace = Brace(area_eq2[R"e^{-{r}^2}"], DOWN, SMALL_BUFF)
        VGroup(circ_brace, height_brace).fix_in_frame()

        circ_word = area_eq1["(Circumference)"]
        height_word = area_eq1["(Height)"]

        self.add(circle, set_depth_test=False)
        self.play(
            ShowCreation(circle),
            ShowCreation(rect_top),
        )
        self.play(
            FadeIn(circ_brace),
            circ_word.animate.scale(0.75).next_to(circ_brace, DOWN, SMALL_BUFF),
            Write(area_eq2[R"2 \pi {r}"]),
            height_word.animate.next_to(area_eq2[R"2 \pi {r}"], RIGHT)
        )
        self.wait()
        self.add(height_line, set_depth_test=False)
        self.play(
            FadeOut(circle),
            FadeOut(rect_top),
            ShowCreation(rect_side),
            ShowCreation(height_line),
        )
        self.play(
            FadeIn(height_brace),
            height_word.animate.scale(0.75).next_to(height_brace, DOWN, SMALL_BUFF, aligned_edge=LEFT),
            circ_word.animate.align_to(circ_brace, RIGHT),
            FadeInFromPoint(area_eq2[R"\cdot e^{-{r}^2}"], r_func[1:].get_center()),
        )
        self.remove(area_eq1)
        self.add(area_eq2, circ_word, height_word)
        self.wait()
        self.play(
            frame.animate.center().reorient(-15, 66).set_height(4).set_anim_args(run_time=15),
            *map(FadeOut, [rect, rect_side, height_line]),
        )

        # Show thickness
        volume_word = Text("Volume", **eq_kw)
        volume_word.fix_in_frame()
        volume_word.move_to(area_eq2, DL)
        area_part = area_eq2[R"= $2 \pi {r} \cdot e^{-{r}^2}$"]
        annotations = VGroup(circ_brace, height_brace, circ_word, height_word)
        dr_tex = Tex("d{r}", **eq_kw)
        dr_tex.fix_in_frame()

        thick_cylinder = self.get_thick_cylinder(cylinder, delta_r * axes.x_axis.get_unit_size())
        thin_cylinder = self.get_thick_cylinder(cylinder, 0.1 * delta_r * axes.x_axis.get_unit_size())
        _, annulus, outer_cylinder = thick_cylinder

        dr_brace = Brace(
            Line(axes.get_origin(), axes.c2p(delta_r, 0, 0)), UP
        )
        dr_brace.stretch(0.5, 1)
        brace_label = dr_brace.get_tex("d{r}", buff=SMALL_BUFF)
        brace_label["r"].set_color(RED)
        brace_label.scale(0.35, about_edge=DOWN)
        dr_brace.add(brace_label)
        dr_brace.rotate(90 * DEGREES, RIGHT)
        dr_brace.move_to(thick_cylinder.get_corner(OUT + LEFT), IN + LEFT)

        self.remove(cylinder)
        self.add(thin_cylinder, cylinders, graph, graph_mesh)
        self.play(Transform(thin_cylinder, thick_cylinder))
        self.add(dr_brace, set_depth_test=False)
        self.play(Write(dr_brace))
        self.wait()

        self.play(
            LaggedStartMap(FadeOut, annotations, shift=DOWN, run_time=1),
            FadeOut(area_eq2["Area"], DOWN),
            FadeIn(volume_word, DOWN),
            area_part.animate.next_to(volume_word, RIGHT, SMALL_BUFF, DOWN),
        )
        dr_tex.next_to(area_part, RIGHT, SMALL_BUFF, DOWN)
        self.play(FadeIn(dr_tex))
        self.wait()

        # Show all cylinders
        integrand = VGroup(*area_part[0][1:], *dr_tex)
        integrand.fix_in_frame()
        integral = Tex(R"\int_0^\infty", **eq_kw)
        integral.fix_in_frame()
        integral.move_to(volume_word, LEFT)

        thick_cylinders = Group(*(
            self.get_thick_cylinder(cyl, delta_r * axes.x_axis.get_unit_size())
            for cyl in cylinders
        ))
        thick_cylinders.set_opacity(0.8)
        thick_cylinders.set_shading(0.25, 0.25, 0.25)
        small_dr = 0.02
        thin_cylinders = Group(*(
            self.get_thick_cylinder(self.get_cylinder(axes, r), small_dr)
            for r in np.arange(0, 5, small_dr)
        ))
        thin_cylinders.set_opacity(0.5)

        self.play(
            FadeOut(volume_word, LEFT),
            FadeOut(area_part[0][0], LEFT),
            FadeIn(integral, LEFT),
            integrand.animate.next_to(integral, RIGHT, buff=0),
        )

        self.add(thick_cylinders, cylinders, graph, graph_mesh)
        self.play(ShowIncreasingSubsets(thick_cylinders, run_time=8))
        self.play(FadeOut(thick_cylinders, 0.1 * IN))
        self.wait()

        self.add(dr_brace[:-1], dr_brace[-1], set_depth_test=False)
        self.play(
            Transform(thin_cylinder, thin_cylinders[int(np.round(r_tracker.get_value() / small_dr))]),
            dr_brace[:-1].animate.stretch(small_dr / delta_r, 0, about_edge=RIGHT),
            UpdateFromFunc(dr_brace[-1], lambda m: m.next_to(dr_brace[:-1], OUT, SMALL_BUFF)),
            run_time=3,
        )
        self.add(thin_cylinders, cylinders, graph, graph_mesh)
        self.add(dr_brace)
        dr_brace.deactivate_depth_test()
        self.play(
            ShowIncreasingSubsets(thin_cylinders),
            frame.animate.reorient(20, 70).set_height(8).move_to(OUT),
            FadeOut(dr_brace, time_span=(0, 2)),
            FadeOut(thin_cylinder, 2 * IN, time_span=(0, 2)),
            FadeOut(functions, time_span=(0, 2)),
            FadeOut(integral, time_span=(0, 2)),
            FadeOut(integrand, time_span=(0, 2)),
            run_time=20,
        )
        self.wait()

        # Ambient rotation
        t0 = self.time
        frame.add_updater(lambda m: m.reorient(20 * math.cos(0.1 * (self.time - t0))))
        self.wait(30)
