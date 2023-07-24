import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *
from _2023.clt.main import *
from _2022.convolutions.discrete import *


class Convolutions(InteractiveScene):
    axes_config = dict(
        x_range=(-3, 3, 1),
        y_range=(-1, 1, 1.0),
        width=6,
        height=2,
    )
    f_graph_style = dict(stroke_color=BLUE, stroke_width=2)
    g_graph_style = dict(stroke_color=YELLOW, stroke_width=2)
    fg_graph_style = dict(stroke_color=GREEN, stroke_width=4)
    conv_graph_style = dict(stroke_color=TEAL, stroke_width=2)
    f_graph_x_step = 0.1
    g_graph_x_step = 0.1
    f_label_tex = "f(x)"
    g_label_tex = "g(s - x)"
    fg_label_tex = R"f(x) \cdot g(s - x)"
    conv_label_tex = R"[f * g](s) = \int_{-\infty}^\infty f(x) \cdot g(s - x) dx"
    label_config = dict(font_size=36)
    t_color = TEAL
    area_line_dx = 0.05
    jagged_product = True
    jagged_convolution = True
    g_is_rect = False
    conv_y_stretch_factor = 2.0

    def setup(self):
        super().setup()
        if self.g_is_rect:
            k1_tracker = self.k1_tracker = ValueTracker(1)
            k2_tracker = self.k2_tracker = ValueTracker(1)

        # Add axes
        all_axes = self.all_axes = self.get_all_axes()
        f_axes, g_axes, fg_axes, conv_axes = all_axes
        x_min, x_max = self.axes_config["x_range"][:2]

        self.disable_interaction(*all_axes)
        self.add(*all_axes)

        # Add f(x)
        f_graph = self.f_graph = f_axes.get_graph(self.f, x_range=(x_min, x_max, self.f_graph_x_step))
        f_graph.set_style(**self.f_graph_style)
        f_label = self.f_label = self.get_label(self.f_label_tex, f_axes)
        if self.jagged_product:
            f_graph.make_jagged()

        self.add(f_graph)
        self.add(f_label)

        # Add g(s - x)
        self.toggle_selection_mode()  # So triangle is highlighted
        s_indicator = self.s_indicator = ArrowTip().rotate(90 * DEGREES)
        s_indicator.set_height(0.15)
        s_indicator.set_fill(self.t_color, 0.8)
        s_indicator.move_to(g_axes.get_origin(), UP)
        s_indicator.add_updater(lambda m: m.align_to(g_axes.get_origin(), UP))

        def get_s():
            return g_axes.x_axis.p2n(s_indicator.get_center())

        self.get_s = get_s
        g_graph = self.g_graph = g_axes.get_graph(lambda x: 0, x_range=(x_min, x_max, self.g_graph_x_step))
        g_graph.set_style(**self.g_graph_style)
        if self.g_is_rect:
            x_min = g_axes.x_axis.x_min
            x_max = g_axes.x_axis.x_max
            g_graph.add_updater(lambda m: m.set_points_as_corners([
                g_axes.c2p(x, y)
                for s in [get_s()]
                for k1 in [k1_tracker.get_value()]
                for k2 in [k2_tracker.get_value()]
                for x, y in [
                    (x_min, 0), (-0.5 / k1 + s, 0), (-0.5 / k1 + s, k2), (0.5 / k1 + s, k2), (0.5 / k1 + s, 0), (x_max, 0)
                ]
            ]))
        else:
            g_axes.bind_graph_to_func(g_graph, lambda x: self.g(get_s() - x), jagged=self.jagged_product)

        g_label = self.g_label = self.get_label(self.g_label_tex, g_axes)

        s_label = self.s_label = VGroup(*Tex("s = "), DecimalNumber())
        s_label.arrange(RIGHT, buff=SMALL_BUFF)
        s_label.scale(0.5)
        s_label.set_backstroke(width=8)
        s_label.add_updater(lambda m: m.next_to(s_indicator, DOWN, buff=0.15))
        s_label.add_updater(lambda m: m[-1].set_value(get_s()))

        self.add(g_graph)
        self.add(g_label)
        self.add(s_indicator)
        self.add(s_label)

        # Show integral of f(x) * g(s - x)
        def prod_func(x):
            k1 = self.k1_tracker.get_value() if self.g_is_rect else 1
            k2 = self.k2_tracker.get_value() if self.g_is_rect else 1
            return self.f(x) * self.g((get_s() - x) * k1) * k2

        fg_graph = fg_axes.get_graph(lambda x: 0, x_range=(x_min, x_max, self.g_graph_x_step))
        pos_graph = fg_graph.copy()
        neg_graph = fg_graph.copy()
        for graph in f_graph, g_graph, fg_graph, pos_graph, neg_graph:
            self.disable_interaction(graph)
        fg_graph.set_style(**self.fg_graph_style)
        VGroup(pos_graph, neg_graph).set_stroke(width=0)
        pos_graph.set_fill(BLUE, 0.5)
        neg_graph.set_fill(RED, 0.5)

        get_discontinuities = None
        if self.g_is_rect:
            def get_discontinuities():
                k1 = self.k1_tracker.get_value()
                return [get_s() - 0.5 / k1, get_s() + 0.5 / k1]

        kw = dict(
            jagged=self.jagged_product,
            get_discontinuities=get_discontinuities,
        )
        fg_axes.bind_graph_to_func(fg_graph, prod_func, **kw)
        fg_axes.bind_graph_to_func(pos_graph, lambda x: np.clip(prod_func(x), 0, np.inf), **kw)
        fg_axes.bind_graph_to_func(neg_graph, lambda x: np.clip(prod_func(x), -np.inf, 0), **kw)

        self.prod_graphs = VGroup(fg_graph, pos_graph, neg_graph)

        fg_label = self.fg_label = self.get_label(self.fg_label_tex, fg_axes)

        self.add(pos_graph, neg_graph, fg_axes, fg_graph)
        self.add(fg_label)

        # Show convolution
        conv_graph = self.conv_graph = self.get_conv_graph(conv_axes)
        if self.jagged_convolution:
            conv_graph.make_jagged()
        conv_graph.set_style(**self.conv_graph_style)

        graph_dot = self.graph_dot = GlowDot(color=WHITE)
        graph_dot.add_updater(lambda d: d.move_to(conv_graph.quick_point_from_proportion(
            inverse_interpolate(x_min, x_max, get_s())
        )))
        graph_line = self.graph_line = Line(stroke_color=WHITE, stroke_width=1)
        graph_line.add_updater(lambda l: l.put_start_and_end_on(
            graph_dot.get_center(),
            [graph_dot.get_x(), conv_axes.get_y(), 0],
        ))
        self.conv_graph_dot = graph_dot
        self.conv_graph_line = graph_line

        conv_label = self.conv_label = Tex(self.conv_label_tex, **self.label_config)
        conv_label.match_x(conv_axes)
        conv_label.set_y(np.mean([conv_axes.get_y(UP), FRAME_HEIGHT / 2]))

        self.add(conv_graph)
        self.add(graph_dot)
        self.add(graph_line)
        self.add(conv_label)

    def get_all_axes(self):
        all_axes = VGroup(*(Axes(**self.axes_config) for x in range(4)))
        all_axes[:3].arrange(DOWN, buff=0.75)
        all_axes[3].next_to(all_axes[:3], RIGHT, buff=1.5)
        all_axes[3].y_axis.stretch(
            self.conv_y_stretch_factor, 1
        )
        all_axes.to_edge(LEFT)
        all_axes.to_edge(DOWN, buff=0.1)

        for i, axes in enumerate(all_axes):
            x_label = Tex("x" if i < 3 else "s", font_size=24)
            x_label.next_to(axes.x_axis.get_right(), UP, MED_SMALL_BUFF)
            axes.x_label = x_label
            axes.x_axis.add(x_label)
            axes.y_axis.ticks.set_opacity(0)
            axes.x_axis.ticks.stretch(0.5, 1)

        return all_axes

    def get_label(self, tex, axes):
        label = Tex(tex, **self.label_config)
        label.move_to(midpoint(axes.get_origin(), axes.get_right()))
        label.match_y(axes.get_top())
        return label

    def get_conv_graph(self, conv_axes):
        return get_conv_graph(conv_axes, self.f, self.g)

    def get_conv_s_indicator(self):
        g_s_indicator = VGroup(self.s_indicator, self.s_label)
        f_axes, g_axes, fg_axes, conv_axes = self.all_axes

        def get_s():
            return g_axes.x_axis.p2n(self.s_indicator.get_x())

        conv_s_indicator = g_s_indicator.copy()
        conv_s_indicator.add_updater(lambda m: m.become(g_s_indicator))
        conv_s_indicator.add_updater(lambda m: m.shift(
            conv_axes.c2p(get_s(), 0) - g_axes.c2p(get_s(), 0)
        ))
        return conv_s_indicator

    def f(self, x):
        return 0.5 * np.exp(-0.8 * x**2) * (0.5 * x**3 - 3 * x + 1)

    def g(self, x):
        return np.exp(-x**2) * np.sin(2 * x)

# 可以执行
class ProbConvolutions(Convolutions):
    jagged_product = True

    def construct(self):
        # Hit most of previous setup
        f_axes, g_axes, fg_axes, conv_axes = self.all_axes
        f_graph, g_graph, prod_graphs, conv_graph = self.f_graph, self.g_graph, self.prod_graphs, self.conv_graph
        f_label, g_label, fg_label, conv_label = self.f_label, self.g_label, self.fg_label, self.conv_label
        s_indicator = self.s_indicator
        s_label = self.s_label
        self.remove(s_indicator, s_label)

        f_axes.x_axis.add_numbers(font_size=16, buff=0.1, excluding=[0])
        self.remove(f_axes, f_graph, f_label)

        y_label = Tex("y").replace(g_axes.x_label)
        g_label.shift(0.2 * UP)
        gy_label = Tex("g(y)", **self.label_config).replace(g_label, dim_to_match=1)
        gmx_label = Tex("g(-x)", **self.label_config).replace(g_label, dim_to_match=1)
        g_axes.x_label.set_opacity(0)
        self.remove(g_axes, g_graph, g_label)

        alt_fg_label = Tex(R"p_X(x) \cdot g(-x)", **self.label_config)
        alt_fg_label.move_to(fg_label)

        conv_label.shift_onto_screen()
        sum_label = Tex("[f * g](s)", **self.label_config)
        sum_label.move_to(conv_label)
        self.remove(fg_axes, prod_graphs, fg_label)
        conv_cover = SurroundingRectangle(conv_axes, buff=0.25)
        conv_cover.set_stroke(width=0)
        conv_cover.set_fill(BLACK, 0.5)
        self.add(conv_cover)

        # Show f
        f_term = conv_label["f(x)"][0]
        f_rect = SurroundingRectangle(f_term)
        f_rect.set_stroke(YELLOW, 2)

        self.play(ShowCreation(f_rect))
        self.play(
            TransformFromCopy(f_term, f_label),
            FadeIn(f_axes),
        )
        self.play(
            ShowCreation(f_graph),
            VShowPassingFlash(f_graph.copy().set_stroke(width=5)),
            run_time=2
        )
        self.wait()