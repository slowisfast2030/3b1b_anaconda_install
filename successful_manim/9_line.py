import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *
from _2023.clt.main import *
from _2022.convolutions.discrete import *

import scipy.stats


def wedge_func(x):
    return np.clip(-np.abs(x) + 1, 0, 1)


def double_lump(x):
    return 0.45 * np.exp(-6 * (x - 0.5)**2) + np.exp(-6 * (x + 0.5)**2)


def uniform(x):
    return 1.0 * (-0.5 < x) * (x < 0.5)


def get_conv_graph(axes, f, g, dx=0.1):
    dx = 0.1
    x_min, x_max = axes.x_range[:2]
    x_samples = np.arange(x_min, x_max + dx, dx)
    f_samples = np.array([f(x) for x in x_samples])
    g_samples = np.array([g(x) for x in x_samples])
    full_conv = np.convolve(f_samples, g_samples)
    x0 = len(x_samples) // 2 - 1  # TODO, be smarter about this
    conv_samples = full_conv[x0:x0 + len(x_samples)]
    conv_graph = VMobject()
    conv_graph.set_stroke(TEAL, 2)
    conv_graph.set_points_smoothly(axes.c2p(x_samples, conv_samples * dx))
    return conv_graph

class RepeatedSamplesFromContinuousDistributions(InteractiveScene):
    sigma1 = 1.0
    sigma2 = 1.0

    graph_colors = [BLUE, RED, TEAL]
    graph_stroke_width = 2

    dot_fade_factor = 0.25

    def setup(self):
        super().setup()
        self.random_variables = self.get_random_variables()
        self.all_dots = Group()
        self.add(self.all_dots)

    def get_plots(self):
        # Axes and graphs
        all_axes = self.get_axes()
        left_axes = all_axes[:2]
        left_axes.arrange(DOWN, buff=1.5)
        left_axes.to_edge(LEFT)
        all_axes[2].center().to_edge(RIGHT)

        # 每一个Axes都是由两条NumberLine构成的
        # 真正开发的时候，如果想对某一个对象做更加深入的美化
        # 有两种方法
        # 1.看源代码
        # 2.在3b1b的视频代码库中搜索，看看他是怎么做的，吸取经验
        for axes in all_axes:
            axes.x_axis.add_numbers(font_size=16)
            axes.y_axis.set_stroke(opacity=0.5) # 对坐标轴进行美化

        
        #pdfs = self.get_pdfs()
        graphs = VGroup(*(
            axes.get_graph(func).set_stroke(color)
            for axes, func, color in zip(
                all_axes,
                self.get_pdfs(),
                self.graph_colors
            )
        ))
        graphs.add(self.get_sum_graph(all_axes[2]))
        graphs.set_stroke(width=self.graph_stroke_width)

        # Labels
        labels = self.get_axes_labels(all_axes)

        plots = VGroup(*(
            VGroup(*tup)
            for tup in zip(all_axes, graphs, labels)
        ))
        return plots

    def get_axes(self):
        return VGroup(*(
            Axes(
                (-5, 5), (0, 0.5, 0.25),
                width=5.5,
                height=2,
            )
            for x in range(3)
        ))

    def get_axes_labels(self, all_axes):
        a1, a2, a3 = all_axes
        return VGroup(
            Tex("X").move_to(midpoint(a1.get_corner(UR), a1.get_top())),
            Tex("Y").move_to(midpoint(a2.get_corner(UR), a2.get_top())),
            Tex("X + Y").next_to(a3, UP, buff=1.0)
        )

    def repeated_samples(self, plots, n_repetitions, **kwargs):
        for n in range(n_repetitions):
            self.animate_samples(plots, **kwargs)

    def animate_samples(
        self,
        plots,
        time_between_samples=0.25,
        time_before_fade=1.0,
        animate=True,
    ):
        # Setup
        xy_samples = np.round(self.get_samples(), 2)
        sample_sum = sum(xy_samples)
        samples = [*xy_samples[:2], sample_sum]
        dots = Group()
        labels = VGroup()
        lines = VGroup()
        for sample, plot in zip(samples, plots):
            axes, graph, sym_label = plot
            dot = GlowDot(axes.c2p(sample, 0))
            label = DecimalNumber(sample)
            label.next_to(sym_label, DOWN)
            label.scale(0.75, about_edge=DOWN)
            label.set_fill(GREY_A)

            line = axes.get_v_line_to_graph(sample, graph, line_func=Line)
            line.set_stroke(YELLOW, 2)

            dots.add(dot)
            labels.add(label)
            lines.add(line)

        if len(plots) > 2:
            sum_label = VGroup(
                DecimalNumber(samples[0]),
                Tex("+") if samples[1] > 0 else Tex("-"),
                DecimalNumber(abs(samples[1])),
                Tex("="),
                DecimalNumber(samples[2]),
            )
            sum_label.arrange(RIGHT, buff=0.15)
            sum_label[-1].align_to(sum_label[0], DOWN)
            sum_label.match_height(labels[2])
            sum_label.match_style(labels[2])
            sum_label.move_to(labels[2], DL)
            labels.remove(labels[2])
            labels.add(sum_label)
            sum_label.shift((plots[2][2]["+"].get_x() - sum_label[1].get_x()) * RIGHT)

        # Animate
        for i in range(min(2, len(plots))):
            self.add(dots[i], labels[i], lines[i])
            if len(plots) > 2:
                self.add(sum_label[:2 * i + 1])
            self.wait(time_between_samples)
        if len(plots) > 2:
            self.play(LaggedStart(
                Transform(dots[0].copy(), dots[2].copy().set_opacity(0.5), remover=True),
                Transform(dots[1].copy(), dots[2].copy().set_opacity(0.5), remover=True),
                FadeTransform(sum_label[:3].copy(), sum_label[3:]),
                run_time=1.0 if animate else 0,
            ))
            self.add(sum_label)
            self.add(dots[2])
        self.wait(time_before_fade)
        kw = dict(run_time=0.25 if animate else 0)
        self.play(
            LaggedStart(*(
                dot.animate.set_radius(0.1).set_opacity(self.dot_fade_factor)
                for dot in dots
            ), **kw),
            LaggedStartMap(FadeOut, labels, **kw),
            LaggedStartMap(FadeOut, lines[:2], **kw),
        )
        self.all_dots.add(*dots)
        self.add(self.all_dots)

    def get_random_variables(self):
        return [
            scipy.stats.norm(0, self.sigma1),
            scipy.stats.norm(0, self.sigma2),
        ]

    def get_samples(self):
        return [
            np.round(var.rvs(), 2)
            for var in self.random_variables
        ]

    def get_pdfs(self):
        return [var.pdf for var in self.random_variables]

    def get_sum_graph(self, axes):
        graph = get_conv_graph(axes, *self.get_pdfs())
        graph.set_stroke(self.graph_colors[2])
        return graph

class AddTwoGammaDistributions(RepeatedSamplesFromContinuousDistributions):
    dot_fade_factor = 0.75

    def construct(self):
        # Plots
        plots = self.get_plots()
        self.add(plots)

        # Add graph labels
        kw = dict(font_size=30)
        graph_labels = VGroup(
            Tex("e^{-x}", **kw),
            Tex(R"\frac{1}{2} x^2 \cdot e^{-x}", **kw),
            Tex(R"\frac{1}{6} x^3 \cdot e^{-x}", **kw),
        )
        for plot, label, x in zip(plots, graph_labels, [1, 2, 3]):
            axes, graph, var_label = plot
            label.next_to(axes.i2gp(x, graph), UP, SMALL_BUFF)
            label.match_color(graph)
        graph_labels[0].shift(0.3 * UR)

        self.add(graph_labels)

        # Initial samples
        self.repeated_samples(
            plots, 5,
            animate=False,
            time_between_samples=0.1,
            time_before_fade=0.5
        )

        # Graph equation
        frame = self.frame

        fs_rect = FullScreenRectangle()
        fs_rect.set_stroke(RED_E, 2)
        fs_rect.set_fill(BLACK, 1)

        fuller_rect = FullScreenRectangle()
        fuller_rect.set_fill(GREY_E, 1)
        fuller_rect.scale(3)

        self.add(fuller_rect, fs_rect, *self.mobjects)
        self.wait()

        self.play(
            frame.animate.set_height(13, about_point = 3 * DOWN),
            # 下面这两个动作对于整个效果，可有可无
            # FadeIn(fuller_rect),
            # FadeIn(fs_rect)
        )