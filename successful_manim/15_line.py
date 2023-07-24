import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class PoolTableReflections(InteractiveScene):
    def construct(self):
        # Add  table
        #table = ImageMobject("pool_table")
        image = '/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master/_2023/standup_maths/huoying.jpeg'
        table = ImageMobject(image)
        table.set_height(4.0)
        buff = 0.475

        ball = TrueDot(radius=0.1)
        ball.set_color(GREY_A)
        ball.set_shading(1, 1, 1)
        ball.move_to(table)

        self.add(table, ball)

        # Show inner table
        frame = self.frame
        frame.set_height(6)

        irt = Rectangle(  # Inner rect template
            width=table.get_width() - 2 * buff,
            height=table.get_height() - 2 * buff,
        )
        irt.move_to(table)

        # 竟然通过这种方式画矩形
        inner_rect = VMobject()
        inner_rect.start_new_path(irt.get_right())
        for corner in [UR, UL, DL, DR]:
            inner_rect.add_line_to(irt.get_corner(corner))
        inner_rect.add_line_to(irt.get_right())

        inner_rect.set_stroke(RED, 3)
        #inner_rect.insert_n_curves(20)

        self.play(ball.animate.move_to(inner_rect.get_start()))
        # 很有启发性
        self.play(
            ShowCreation(inner_rect, run_time=2),
            UpdateFromFunc(ball, lambda m: m.move_to(inner_rect.get_end()))
        )
        self.wait()