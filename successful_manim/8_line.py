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
        all_axes = self.get_axes() # 生成3个坐标轴
        left_axes = all_axes[:2] # all_axes是VGoup，可以用切片
        left_axes.arrange(DOWN, buff=1.5) # 左侧有两个，上下排列
        left_axes.to_edge(LEFT)
        all_axes[2].center().to_edge(RIGHT) # 右侧有一个，居中，靠右

        for axes in all_axes:
            axes.x_axis.add_numbers(font_size=16)
            axes.y_axis.set_stroke(opacity=0.5)

        pdfs = self.get_pdfs() # 这一行似乎是多余的
        graphs = VGroup(*(
            axes.get_graph(func).set_stroke(color)
            for axes, func, color in zip(
                all_axes,
                self.get_pdfs(),
                self.graph_colors
            )
        ))
        # 这里为何又增加一个graph呢？
        graphs.add(self.get_sum_graph(all_axes[2])) 
        graphs.set_stroke(width=self.graph_stroke_width)

        # Labels
        labels = self.get_axes_labels(all_axes)

        # 这里的all_axes, graphs, labels都是VGroup
        # 操作上感觉很像列表
        plots = VGroup(*(
            VGroup(*tup)
            for tup in zip(all_axes, graphs, labels)
        ))
        return plots

    # 好像从来没有深刻思考过VGoup的用法
    # 为什么需要VGoup? 
    # 因为它可以把多个对象组合在一起，然后可以一起操作
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


class SampleTwoNormals(RepeatedSamplesFromContinuousDistributions):
    random_seed = 1
    sigma1 = 1
    sigma2 = 1.5

    annotations = False

    def construct(self):
        # Setup plots
        plots = self.get_plots()
        plots.to_edge(UP, buff=1.0)
        sum_axes, sum_graph, sum_label = plots[2] # 对第三个plot进行特殊操作
        sum_axes.y_axis.set_opacity(0)
        sum_graph.set_opacity(0)
        sum_label.shift(DOWN)

        print("="*100)
        print(plots)
        print(len(plots))
        # 这里的plots应该有3个元素
        # [self.sigma1, self.sigma2]只有两个元素
        # 为什么可以用zip呢？
        normal_parameters = VGroup(*(
            self.get_normal_parameter_labels(plot, 0, sigma)
            for plot, sigma in zip(plots, [self.sigma1, self.sigma2])
        ))
        print(len(normal_parameters))

        normal_words = VGroup(*(
            Text("Normal\ndistribution", font_size=30, alignment="LEFT").next_to(
                parameters, UP, MED_LARGE_BUFF, LEFT
            )
            for parameters in normal_parameters
        ))

        if self.annotations:
            plots.set_opacity(0)

        # Repeated samples of X
        frame = self.frame
        frame.move_to(plots[0])
        frame.set_height(plots[0].get_height() + 2)

        self.add(plots[0])

        # 下面的代码都没有执行
        if self.annotations:
            print("*"*100)
            print("all is well")
            # Describe X
            axes, graph, label = plots[0]
            label_rect = SurroundingRectangle(label, buff=0.05)
            label_rect.set_stroke(YELLOW, 2)
            sample_point = label.get_center() + label.get_height() * DOWN

            rv_words = Text("Random variable", font_size=24)
            rv_words.next_to(label, UR, buff=0.5)
            rv_arrow = Arrow(rv_words, label, buff=0.2, stroke_color=YELLOW)

            sample_words = Text("Samples", font_size=24)
            sample_words.next_to(sample_point, DOWN, LARGE_BUFF)
            sample_words.match_x(rv_words)
            sample_arrow = Arrow(sample_words, sample_point + 0.25 * DR, buff=0.2)
            sample_arrow.set_stroke(BLUE)

            self.play(
                FadeIn(rv_words, lag_ratio=0.1),
                ShowCreation(label_rect),
                GrowArrow(rv_arrow),
            )
            self.wait()
            self.play(
                FadeTransform(rv_words.copy(), sample_words),
                TransformFromCopy(rv_arrow, sample_arrow),
                FadeOut(label_rect),
            )
            self.wait()

            # Describe normal distribution
            curve_copy = graph.copy()
            curve_copy.set_stroke(TEAL, 7, 1)

            self.play(
                LaggedStartMap(FadeOut, VGroup(
                    sample_words, sample_arrow, rv_arrow, rv_words,
                )),
                Write(normal_words[0], run_time=2),
                FadeIn(normal_parameters[0]),
                VShowPassingFlash(curve_copy, time_width=0.7, time_span=(0.5, 5)),
            )
            self.wait()

            # Show area
            bound_tracker = ValueTracker([-1, -1])
            area = always_redraw(lambda: axes.get_area_under_graph(
                graph, bound_tracker.get_value()
            ))

            self.add(area)
            self.play(
                bound_tracker.animate.set_value([-1, 2]),
                run_time=3
            )
            self.wait()
            self.play(FadeOut(area))

        else:
            self.repeated_samples(plots[:1], 30, time_before_fade=0.5)

    def get_normal_parameter_labels(self, plot, mean, sigma, font_size=18, color=GREY_A):
        kw = dict(font_size=font_size)
        labels = VGroup(
            Tex(R"\text{Mean} = 0.0", **kw),
            Tex(R"\text{Std. Dev.} = 0.0", **kw),
        )
        for label, value in zip(labels, [mean, sigma]):
            number = label.make_number_changable("0.0")
            number.set_value(value)

        labels.arrange(DOWN, aligned_edge=LEFT)
        labels.move_to(plot, LEFT)
        labels.shift(0.1 * plot.get_height() * DOWN)
        labels.align_to(plot[0].x_axis.get_start(), LEFT)
        labels.set_color(color)

        return labels
