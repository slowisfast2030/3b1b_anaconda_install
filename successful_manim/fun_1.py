import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class Test(Scene):
    frame_center = [0, 0, 2]

    def construct(self):
        
        self.camera.frame.reorient(-30, 75)
        self.camera.frame.move_to(self.frame_center)

        text = Text("This is a test").shift(UP)
        self.play(Write(text))
        self.wait()

        width, height = 20, 20
        grid = NumberPlane(
            x_range=(-width // 2, width // 2, 2),
            y_range=(-height // 2, height // 2, 2),
            background_line_style={
                "stroke_color": GREY_C,
                "stroke_width": 1,
            },
            faded_line_ratio=4,
        )
        grid.shift(-grid.get_origin())
        grid.set_width(width)
        grid.axes.match_style(grid.background_lines)
        grid.set_flat_stroke(True)
        grid.insert_n_curves(3)

        self.add(grid)
        self.wait()

        plane = Rectangle()
        plane.replace(grid, stretch=True)

        plane_style = {
        "stroke_width": 0,
        "fill_color": YELLOW_E,
        "fill_opacity": 0.3,
        #"gloss": 0.5,
        #"shadow": 0.2,
        }
        plane.set_style(**plane_style)
        self.add(plane)
        self.wait()
        print("\ngrid:")
        print(grid.get_all_points())
        print(grid.submobjects)
        print(grid.submobjects[-2].get_points())
        print("\nplane:")
        print(plane.get_points())
        print(plane.get_family())


        