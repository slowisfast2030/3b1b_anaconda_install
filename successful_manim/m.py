import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class test(Scene):
    def construct(self):
        m = Matrix(matrix = np.ones((3, 4)), 
                   include_background_rectangle=False, 
                   add_background_rectangles_to_entries=False
                   )
        for row in m.mob_matrix:
            for col in row:
                print(col)

        print(m.elements)

        print("-"*100)

        for i in range(len(m)):
            print(m[i])

        self.add(m)
        self.wait()