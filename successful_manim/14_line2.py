import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *
import sympy

# good
class RaceGraph(InteractiveScene):
    race_length = 1500
    y_range = (-4, 30, 2)

    def construct(self):
        # Compute differences
        primes: list[int] = list(sympy.primerange(3, self.race_length))
        diffs = [0]
        colors = [WHITE]
        y_max = self.y_range[1]
        for p in primes:
            diff = diffs[-1] + (p % 4 - 2)
            diffs.append(diff)
            if diff < 0:
                colors.append(BLUE)
            elif diff < y_max / 2:
                colors.append(interpolate_color(WHITE, RED, clip(2 * diff / y_max, 0, 1)))
            else:
                colors.append(interpolate_color(RED, RED_E, clip(2 * (diff - y_max / 2) / y_max, 0, 1)))

        # Axes and graph
        x_unit = 10
        axes = Axes(
            x_range=(0, len(primes) + 10, x_unit),
            y_range=self.y_range,
            width=len(primes) / x_unit / 1.6,
            height=7,
            axis_config=dict(tick_size=0.05),
        )
        axes.to_edge(LEFT, buff=0.8)

        y_label = TexText(R"\#Team3 $-$ \#Team1")
        y_label["Team3"].set_color(RED)
        y_label["Team1"].set_color(BLUE)
        y_label.next_to(axes.y_axis.get_top(), RIGHT)
        y_label.fix_in_frame()

        axes.y_axis.add_numbers(font_size=14, buff=0.15)

        graph = VMobject()
        graph.set_points_as_corners([
            axes.c2p(i, diff)
            for i, diff in enumerate(diffs)
        ])
        graph.set_stroke(colors, width=3)

        self.add(axes)
        self.add(y_label)
        #self.add(graph)

        # Set blocking rectangle
        rect = FullScreenRectangle()
        rect.set_fill(BLACK, 1)
        rect.set_stroke(BLACK, 0)
        rect.match_x(axes.c2p(0, 0), LEFT)

        def set_x_shift(x, anims=[], **kwargs):
            self.play(
                rect.animate.match_x(axes.c2p(x, 0), LEFT),
                *anims,
                **kwargs
            )

        self.clear()
        self.add(graph, rect, axes.x_axis, axes.y_axis, y_label)

        # First blocks, total runtime should be 12
        frame = self.frame
        frame.save_state()
        zoom_point = axes.c2p(0, 0)
        frame.set_height(3, about_point=zoom_point)

        # for x in range(10):
        #     set_x_shift(x + 1)

        # for x in range(10, 30):
        #     set_x_shift(x + 1, run_time = 6 / 20)
        #     self.wait(6 / 20)

        # Next block
        set_x_shift(
            200,
            anims=[Restore(frame)],
            run_time=10, rate_func=linear
        )

        # Squish the graph
        # full_width = get_norm(axes.c2p(200, 0) - axes.c2p(0, 0))
        # origin = axes.c2p(0, 0)

        # prime_label = Integer(primes[200])
        # prime_label.next_to(rect, LEFT, buff=0.7)
        # prime_label.to_edge(DOWN, buff=0.3)
        # prime_label.fix_in_frame()
        # self.add(prime_label)

        # def set_x_squish(x1, x2, **kwargs):
        #     group = VGroup(axes.x_axis, graph)
        #     self.add(group, rect)

        #     self.play(
        #         UpdateFromAlphaFunc(
        #             group,
        #             lambda m, a: m.stretch(
        #                 full_width / get_norm(axes.c2p(interpolate(x1, x2, a), 0) - origin),
        #                 0,
        #                 about_point=origin,
        #             ),
        #         ),
        #         UpdateFromAlphaFunc(
        #             prime_label,
        #             lambda m, a: m.set_value(
        #                 primes[min(int(interpolate(x1, x2, a)), len(primes) - 1)]
        #             )
        #         ),
        #         **kwargs
        #     )

        # set_x_squish(200, len(primes) - 100, rate_func=linear, run_time=20)