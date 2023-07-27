import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class test(Scene):
    def construct(self):
        bg_rect = FullScreenRectangle()
        bg_rect.set_fill(GREY_E, 1)
        bg_rect.set_stroke(BLACK, 0)
        self.add(bg_rect)

        title = OldTexText("Ben Eater implementing Hamming codes")
        title.set_width(FRAME_WIDTH - 2)
        title.to_edge(UP)
        self.add(title)

        screen_rect = ScreenRectangle()
        screen_rect.set_fill(BLACK, 1)
        screen_rect.set_height(6)
        screen_rect.next_to(title, DOWN, MED_LARGE_BUFF)
        self.add(screen_rect)

        self.add(AnimatedBoundary(screen_rect))
        self.wait(6)