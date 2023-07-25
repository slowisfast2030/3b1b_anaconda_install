import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *
import sympy

# 无穷无尽的素数
class PrimeRace(InteractiveScene):
    race_length = 1500

    def construct(self):
        ONE_COLOR = BLUE
        THREE_COLOR = RED
        colors = [ONE_COLOR, THREE_COLOR]

        # Labels
        labels = VGroup(
            Tex(R"p \equiv 1 \mod 4", t2c={"1": ONE_COLOR}),
            Tex(R"p \equiv 3 \mod 4", t2c={"3": THREE_COLOR}),
        )
        labels.arrange(DOWN, buff=0.75)
        labels.to_edge(LEFT)

        h_line = Line(LEFT, RIGHT)
        h_line.set_width(100)
        h_line.to_edge(LEFT)

        v_line = Line(UP, DOWN)
        v_line.set_height(1.5 * labels.get_height())
        v_line.next_to(labels, RIGHT)
        v_line.set_y(0)
        VGroup(h_line, v_line).set_stroke(width=2)

        self.add(h_line, v_line)
        self.add(labels)

        # Start the race
        """
        It takes two parameters, a and b, which are integers that define the range of interest. 
        The function will return all prime numbers in the range [a, b), 
        meaning that a is included but b is not.
        """
        primes: list[int] = list(sympy.primerange(3, self.race_length))
        print("*"*100, primes)
        team1 = VGroup()
        team3 = VGroup()
        teams = [team1, team3]
        blocks = []
        for prime in primes:
            index = int((prime % 4) == 3)
            square = Square(side_length=1)
            square.set_fill(colors[index], 0.5) # 被3整除的质数，填充红色
            square.set_stroke(colors[index], 1.0)
            p_mob = Integer(prime)
            p_mob.set_max_width(0.8 * square.get_width())
            block = VGroup(square, p_mob)

            teams[index].add(block)
            blocks.append(block)

        for team, label in zip(teams, labels):
            team.arrange(RIGHT, buff=0) # 有点小牛逼
            team.next_to(v_line, RIGHT, buff=SMALL_BUFF)
            team.match_y(label)

        h_line.set_width(teams[1].get_width() + 10, about_edge=LEFT)

        for block in blocks[:10]:
            self.play(FadeIn(block[0]), Write(block[1]))

        # Next sets
        frame = self.frame
        frame.target = frame.generate_target()
        frame.target.scale(1.75, about_edge=LEFT)
        self.play(
            LaggedStartMap(
                FadeIn, VGroup(*blocks[10:30]),
                lag_ratio=0.9, # 将lag_ratio设置为0，所有的block同时出现
            ),
            MoveToTarget(frame, rate_func=rush_into), # 这里需要进一步思考frame和frame中的mobject的区别
            run_time=12,
        )

        # Last set
        curr = 30
        tups = [
            (200, 10, linear, 1.25),
            (len(blocks) - 100, 60, linear, 1.25),
            (len(blocks) - 1, 5, smooth, 0.8)
        ]
        print("*"*100, tups)
        """
        [
        (200, 10, <function linear at 0x13eb36160>, 1.25)
        (138, 60, <function linear at 0x13eb36160>, 1.25)
        (237, 5, <function smooth at 0x13eb361f0>, 0.8)
        ]
        """

        for index, rt, func, sf in tups:
            frame.target = frame.generate_target()
            frame.target.scale(sf)
            frame.target.set_x(blocks[index].get_right()[0] + 1)
            self.play(
                ShowIncreasingSubsets(VGroup(*blocks[curr:index])),
                MoveToTarget(frame),
                run_time=rt,
                rate_func=func,
            )
            curr = index

        blocks = VGroup(*blocks)
        self.add(blocks)
        self.play(frame.animate.set_height(8, about_point=blocks.get_right() + 2 * LEFT), run_time=3)
        self.wait()