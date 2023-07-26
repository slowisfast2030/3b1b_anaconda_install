import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *


SUB_ONE_FACTOR = "0.99999999998529"


def sinc(x):
    return np.sinc(x / PI)


def multi_sinc(x, n):
    return np.prod([sinc(x / (2 * k + 1)) for k in range(n)])


def rect_func(x):
    result = np.zeros_like(x)
    result[(-0.5 < x) & (x < 0.5)] = 1.0
    return result


def get_fifteenth_frac_tex():
    return R"{467{,}807{,}924{,}713{,}440{,}738{,}696{,}537{,}864{,}469 \over 467{,}807{,}924{,}720{,}320{,}453{,}655{,}260{,}875{,}000}"


def get_sinc_tex(k=1):
    div_k = f"/ {k}" if k > 1 else ""
    return Rf"{{\sin(x {div_k}) \over x {div_k}}}"


def get_multi_sinc_integral(ks=[1], dots_at=None, rhs="", insertion=""):
    result = Tex(
        R"\int_{-\infty}^\infty",
        insertion,
        *(
            get_sinc_tex(k) if k != dots_at else R"\dots"
            for k in ks
        ),
        "dx",
        rhs,
    )
    t2c = {
        R"\sin": BLUE,
        "x / 3": TEAL,
        "x / 5": GREEN_B,
        "x / 7": GREEN_C,
        "x / 9": interpolate_color(GREEN, YELLOW, 1 / 3),
        "x / 11": interpolate_color(GREEN, YELLOW, 2 / 3),
        "x / 13": YELLOW,
        "x / 15": RED_B,
    }
    for tex, color in t2c.items():
        result.set_color_by_tex(tex, color)
    return result

# good
class ShowIntegrals(InteractiveScene):
    # add_axis_labels = True
    add_axis_labels = False

    def construct(self):
        # Setup axes
        axes = self.get_axes()

        graph = axes.get_graph(sinc, color=BLUE)
        graph.set_stroke(width=3)
        
        # 二阶贝塞尔曲线，每一段两个anchor，一个handle
        points = graph.get_anchors()
        # vg = VGroup() 
        # for point in points[::-1]:
        #     dot = Dot(point, radius=0.03, fill_color=WHITE)
        #     vg.add(dot)

        # #self.play(Write(vg))
        # self.add(vg)

        right_sinc = VMobject().set_points_smoothly(points[len(points) // 2:])
        left_sinc = VMobject().set_points_smoothly(points[:len(points) // 2+1]).reverse_points()
        VGroup(left_sinc, right_sinc).match_style(graph).make_jagged()

        func_label = Tex(R"{\sin(x) \over x}")
        func_label.move_to(axes, UP).to_edge(LEFT)

        self.add(axes)
        self.play(
            Write(func_label),
            ShowCreation(right_sinc, remover=True, run_time=3),
            ShowCreation(left_sinc, remover=True, run_time=3),
        )
        self.add(graph)
        self.wait()

        # Discuss sinc function?
        # sinc_label = OldTex(R"\text{sinc}(x)")
        # sinc_label.next_to(func_label, UR, buff=LARGE_BUFF)
        # arrow = Arrow(func_label, sinc_label)

        # one_over_x_graph = axes.get_graph(lambda x: 1 / x, x_range=(0.1, 8 * PI))
        # one_over_x_graph.set_stroke(YELLOW, 2)
        # one_over_x_label = OldTex("1 / x")
        # one_over_x_label.next_to(axes.i2gp(1, one_over_x_graph), RIGHT)
        # sine_wave = axes.get_graph(np.sin, x_range=(0, 8 * PI)).set_stroke(TEAL, 3)
        # half_sinc = axes.get_graph(sinc, x_range=(0, 8 * PI)).set_stroke(BLUE, 3)

        # self.play(
        #     GrowArrow(arrow),
        #     FadeIn(sinc_label, UR)
        # )
        # self.wait()

        # self.play(
        #     ShowCreation(sine_wave, run_time=2),
        #     graph.animate.set_stroke(width=1, opacity=0.5)
        # )
        # self.wait()
        # self.play(
        #     ShowCreation(one_over_x_graph),
        #     FadeIn(one_over_x_label),
        #     Transform(sine_wave, half_sinc),
        # )
        # self.wait()
        # self.play(
        #     FadeOut(one_over_x_graph),
        #     FadeOut(one_over_x_label),
        #     FadeOut(sine_wave),
        #     graph.animate.set_stroke(width=3, opacity=1),
        # )

        # At 0
        hole = Dot()
        hole.set_stroke(BLUE, 2)
        hole.set_fill(BLACK, 1)
        hole.move_to(axes.c2p(0, 1))

        zero_eq = OldTex(R"{\sin(0) \over 0} = ???")
        zero_eq.next_to(hole, UR)
        lim = OldTex(R"\lim_{x \to 0} {\sin(x) \over x} = 1")
        lim.move_to(zero_eq, LEFT)

        x_tracker = ValueTracker(2.5 * PI)
        get_x = x_tracker.get_value
        dots = GlowDot().replicate(2)
        # 这是啥？注释掉似乎没影响
        #globals().update(locals()) 

        dots.add_updater(lambda d: d[0].move_to(axes.i2gp(-get_x(), graph)))
        dots.add_updater(lambda d: d[1].move_to(axes.i2gp(get_x(), graph)))
        # 下面一行注释掉，似乎对效果没影响
        #dots.update()

        self.play(Write(zero_eq), FadeIn(hole, scale=0.35))
        self.wait()
        self.play(FadeTransform(zero_eq, lim))
        self.add(dots)
        self.play(
            x_tracker.animate.set_value(0).set_anim_args(run_time=2),
            UpdateFromAlphaFunc(dots, lambda m, a: m.set_opacity(a)),
        )
        self.wait()
        self.play(FadeOut(dots), FadeOut(hole), FadeOut(lim))
        #self.play(FadeOut(arrow), FadeOut(sinc_label))

    def get_axes(self,
                 x_range=(-10 * PI, 10 * PI, PI),
                 y_range=(-0.5, 1, 0.5),
                 width=1.3 * FRAME_WIDTH,
                 height=3.5,
                 ):
        axes = Axes(x_range, y_range, width=width, height=height)
        axes.center()
        if self.add_axis_labels:
            axes.y_axis.add_numbers(num_decimal_places=1, font_size=20)
            for u in -1, 1:
                axes.x_axis.add_numbers(
                    u * np.arange(PI, 15 * PI, PI),
                    unit=PI,
                    unit_tex=R"\pi",
                    font_size=20
                )
        return axes