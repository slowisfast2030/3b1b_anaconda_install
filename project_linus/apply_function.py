from manimlib import *

class AnimatingMethods(Scene):
    def construct(self):
        grid = Tex(R"\pi").get_grid(10, 10, height=4)
        self.add(grid)

        # You can animate the application of mobject methods with the
        # ".animate" syntax:
        #self.play(grid.animate.shift(LEFT))

        # Both of those will interpolate between the mobject's initial
        # state and whatever happens when you apply that method.
        # For this example, calling grid.shift(LEFT) would shift the
        # grid one unit to the left, but both of the previous calls to
        # "self.play" animate that motion.

        # The same applies for any method, including those setting colors.
        # self.play(grid.animate.set_color(YELLOW))
        # self.wait()
        self.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN))
        self.wait()
        #self.play(grid.animate.set_height(TAU - MED_SMALL_BUFF))
        #self.wait()

        # The method Mobject.apply_complex_function lets you apply arbitrary
        # complex functions, treating the points defining the mobject as
        # complex numbers.
        self.play(grid.animate.apply_complex_function(np.exp), run_time=1)
        self.wait()

        # Even more generally, you could apply Mobject.apply_function,
        # which takes in functions form R^3 to R^3
        # self.play(
        #     grid.animate.apply_function(
        #         lambda p: [
        #             p[0] + 0.5 * math.sin(p[1]),
        #             p[1] + 0.5 * math.sin(p[0]),
        #             p[2]
        #         ]
        #     ),
        #     run_time=5,
        # )

        self.play(
            grid.animate.apply_function(
                lambda p: [
                    p[0] + 3,
                    p[1] + 3,
                    p[2]
                ]
            ),
            run_time=1,
        )
        self.wait()