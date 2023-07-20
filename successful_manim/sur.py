import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class test(InteractiveScene):
    frame_center = [0, 0, 2]

    def construct(self):
        def func(x, y):
            z = x**2 + y**2
            return np.array([x, y, z])
        
        self.camera.frame.reorient(-30, 75)
        self.camera.frame.move_to(self.frame_center)

        a = ThreeDAxes()

        s = ParametricSurface(func, u_range=(-2,2), v_range=(-2,2), resolution=(4, 4))
        self.add(a, s)
        self.wait()

        points = s.get_points()
        for point in points:
            self.add(Dot(point).scale(2).set_color(RED))
        self.wait()

        print('\n')
        for point in points:
            z = point[0]**2 + point[1]**2
            print(np.append(point, z))
        print(len(points))
        
