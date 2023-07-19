import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class test(InteractiveScene):
    def construct(self):
        plane = NumberPlane()
        m = VMobject()
        """
        看源码可以发现：
        add_cubic_bezier_curve函数是三阶贝塞尔曲线，需要四个点，第一个和最后一个是anchor，中间两个是handle
        在add_cubic_bezier_curve内部，会将三阶贝塞尔曲线转化为两个二阶贝塞尔曲线
        二阶贝塞尔曲线需要三个点，第一个和最后一个是anchor，中间一个是handle
        两条二阶贝塞尔曲线一共有5个点

        self.data["points"]中存储的就是这5个点
        """
        m.add_cubic_bezier_curve(
            np.array([-2, -1, 0]),  
            np.array([-3, 1, 0]),
            np.array([0, 3, 0]),
            np.array([1, 3, 0])
            )
        self.add(m, plane)

        # 本来以为m的点都在曲线上，结果发现不是
        dots = m.get_points()
        print(dots)
        for dot in dots:
            self.add(Dot(dot))
        self.wait()

        m2 = VMobject()
        m2.set_points(dots)
        m2.set_color(RED)
        self.add(m2)
        self.wait()
        print("\n", m2.get_points())

        m3 = VMobject()
        m3.start_new_path(dots[0])
        m3.add_quadratic_bezier_curve_to(dots[1], dots[2])
        m3.set_color(BLUE)
        self.add(m3)
        self.wait()
        print("\n", m3.get_points())

        m4 = VMobject()
        m4.start_new_path(dots[2])
        m4.add_quadratic_bezier_curve_to(dots[3], dots[4])
        m4.set_color(GREEN)
        self.add(m4)
        self.wait()
        print("\n", m4.get_points())
