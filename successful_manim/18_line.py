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
        for point in points:
            dot = Dot(point, radius=0.03, fill_color=WHITE)
            self.add(dot)

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