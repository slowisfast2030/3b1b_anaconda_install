from __future__ import annotations

from abc import ABC, abstractmethod
import numbers

import numpy as np
import itertools as it

from manimlib.constants import BLACK, BLUE, BLUE_D, BLUE_E, GREEN, GREY_A, WHITE, RED
from manimlib.constants import DEGREES, PI
from manimlib.constants import DL, UL, DOWN, DR, LEFT, ORIGIN, OUT, RIGHT, UP
from manimlib.constants import FRAME_X_RADIUS, FRAME_Y_RADIUS
from manimlib.constants import MED_SMALL_BUFF, SMALL_BUFF
from manimlib.mobject.functions import ParametricCurve
from manimlib.mobject.geometry import Arrow
from manimlib.mobject.geometry import DashedLine
from manimlib.mobject.geometry import Line
from manimlib.mobject.geometry import Rectangle
from manimlib.mobject.number_line import NumberLine
from manimlib.mobject.svg.tex_mobject import Tex
from manimlib.mobject.types.dot_cloud import DotCloud
from manimlib.mobject.types.surface import ParametricSurface
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.utils.dict_ops import merge_dicts_recursively
from manimlib.utils.simple_functions import binary_search
from manimlib.utils.space_ops import angle_of_vector
from manimlib.utils.space_ops import get_norm
from manimlib.utils.space_ops import rotate_vector
from manimlib.utils.space_ops import normalize

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Iterable, Sequence, Type, TypeVar, Optional
    from manimlib.mobject.mobject import Mobject
    from manimlib.typing import ManimColor, Vect3, Vect3Array, VectN, RangeSpecifier, Self

    T = TypeVar("T", bound=Mobject)


EPSILON = 1e-8 # 这个极小值是为了获得一个增量，可以用于计算切线
DEFAULT_X_RANGE = (-8.0, 8.0, 1.0) 
DEFAULT_Y_RANGE = (-4.0, 4.0, 1.0) # 默认的frame_height为8.0

"""
类继承关系：

        CoordinateSystem
              
             Axes

    ThreeDAxes   NumberPlane

                 ComplexPlane
"""

class CoordinateSystem(ABC):
    """
    Abstract class for Axes and NumberPlane
    """
    dimension: int = 2

    def __init__(
        self,
        x_range: RangeSpecifier = DEFAULT_X_RANGE,
        y_range: RangeSpecifier = DEFAULT_Y_RANGE,
        num_sampled_graph_points_per_tick: int = 5,
    ):
        self.x_range = x_range
        self.y_range = y_range
        # 这个属性是干嘛的？
        self.num_sampled_graph_points_per_tick = num_sampled_graph_points_per_tick

    @abstractmethod
    def coords_to_point(self, *coords: float | VectN) -> Vect3 | Vect3Array:
        """
        输入坐标轴上的二维坐标，返回场景中的绝对三维坐标，(x, y) --> array[x', y', 0]
        """
        raise Exception("Not implemented")

    @abstractmethod
    def point_to_coords(self, point: Vect3 | Vect3Array) -> tuple[float | VectN, ...]:
        """
        输入场景中的绝对三维坐标，返回坐标轴上的二维坐标，array[x, y, 0] --> (x', y')
        """
        raise Exception("Not implemented")

    def c2p(self, *coords: float) -> Vect3 | Vect3Array:
        """Abbreviation for coords_to_point"""
        return self.coords_to_point(*coords)

    def p2c(self, point: Vect3) -> tuple[float | VectN, ...]:
        """Abbreviation for point_to_coords"""
        return self.point_to_coords(point)

    def get_origin(self) -> Vect3:
        """
        获取坐标原点的绝对坐标
        """
        return self.c2p(*[0] * self.dimension)

    @abstractmethod
    def get_axes(self) -> VGroup:
        raise Exception("Not implemented")

    @abstractmethod
    def get_all_ranges(self) -> list[np.ndarray]:
        raise Exception("Not implemented")

    def get_axis(self, index: int) -> NumberLine:
        """
        获取第index维的坐标轴Mobject
        """
        return self.get_axes()[index]

    def get_x_axis(self) -> NumberLine:
        """
        获取x轴Mobject
        """
        return self.get_axis(0)

    def get_y_axis(self) -> NumberLine:
        """
        获取y轴Mobject
        """
        return self.get_axis(1)

    def get_z_axis(self) -> NumberLine:
        """
        获取z轴Mobject
        """
        return self.get_axis(2)

    def get_x_axis_label(
        self,
        label_tex: str,
        edge: Vect3 = RIGHT,
        direction: Vect3 = DL,
        **kwargs
    ) -> Tex:
        return self.get_axis_label(
            label_tex, self.get_x_axis(),
            edge, direction, **kwargs
        )

    def get_y_axis_label(
        self,
        label_tex: str,
        edge: Vect3 = UP,
        direction: Vect3 = DR,
        **kwargs
    ) -> Tex:
        return self.get_axis_label(
            label_tex, self.get_y_axis(),
            edge, direction, **kwargs
        )

    def get_axis_label(
        self,
        label_tex: str,
        axis: Vect3,
        edge: Vect3,
        direction: Vect3,
        buff: float = MED_SMALL_BUFF
    ) -> Tex:
        label = Tex(label_tex)
        label.next_to(
            axis.get_edge_center(edge), direction, # 研究
            buff=buff
        )
        label.shift_onto_screen(buff=MED_SMALL_BUFF) # 研究
        return label

    def get_axis_labels(
        self,
        x_label_tex: str = "x",
        y_label_tex: str = "y"
    ) -> VGroup:
        """
        获取x轴和y轴的标签
        """
        self.axis_labels = VGroup(
            self.get_x_axis_label(x_label_tex),
            self.get_y_axis_label(y_label_tex),
        )
        return self.axis_labels

    def get_line_from_axis_to_point(
        self, 
        index: int,
        point: Vect3,
        line_func: Type[T] = DashedLine,
        color: ManimColor = GREY_A,
        stroke_width: float = 2
    ) -> T:
        axis = self.get_axis(index)
        # axis.get_projection(point)：point到坐标轴上的投影
        # 基本的向量知识
        line = line_func(axis.get_projection(point), point)
        line.set_stroke(color, stroke_width)
        return line

    def get_v_line(self, point: Vect3, **kwargs):
        """
        传入一个点，过该点做铅垂线
        """
        return self.get_line_from_axis_to_point(0, point, **kwargs)

    def get_h_line(self, point: Vect3, **kwargs):
        """
        传入一个点，过该点做水平线
        """
        return self.get_line_from_axis_to_point(1, point, **kwargs)

    # Useful for graphing
    def get_graph(
        self,
        function: Callable[[float], float],
        x_range: Sequence[float] | None = None,
        **kwargs
    ) -> ParametricCurve:
        """
        绘制函数图像，并自动移动到坐标轴的相对位置，使用``ParametricCurve``类
        - ``x_range=[x_min, x_max, dx]`` : 图像定义域
        """

        """
        一个问题：哪里可以看出移到了坐标轴的相对位置？

        def parametric_function(t: float) -> Vect3:
            return self.c2p(t, function(t))
        """
        x_range = x_range or self.x_range
        t_range = np.ones(3) # array([1., 1., 1.])
        t_range[:len(x_range)] = x_range
        # For axes, the third coordinate of x_range indicates
        # tick frequency.  But for functions, it indicates a
        # sample frequency
        """
        tick frequency: 刻度频率
        sample frequency: 采样频率
        """
        t_range[2] /= self.num_sampled_graph_points_per_tick # 1/5 = 0.2，即每单位刻度上采样5个点

        def parametric_function(t: float) -> Vect3:
            return self.c2p(t, function(t))

        # 这里给出了ParametricCurve类的实例化方法
        # 何谓参数方程
        graph = ParametricCurve(
            parametric_function,
            t_range=tuple(t_range),
            **kwargs
        )

        # ParametricCurve类的源码中没有定义underlying_function属性
        # 但是这个函数为ParametricCurve类的实例添加了underlying_function属性
        # 进一步思考：为何不在ParametricCurve类中定义underlying_function属性呢？
        graph.underlying_function = function
        graph.x_range = x_range
        return graph

    def get_parametric_curve(
        self,
        function: Callable[[float], Vect3],
        **kwargs
    ) -> ParametricCurve:
        """
        传入一个参数方程，绘制一条参数曲线
        """
        """
        需要注意，这里的function(t)返回的是一个三维向量
        计算顺序如下：
        function(t)
        function(t)[:dim]
        *function(t)[:dim]
        """
        dim = self.dimension
        graph = ParametricCurve(
            lambda t: self.coords_to_point(*function(t)[:dim]),
            **kwargs
        )
        graph.underlying_function = function
        return graph

    def input_to_graph_point(
        self,
        x: float,
        graph: ParametricCurve
    ) -> Vect3 | None:
        """
        传入一个x和一条参数曲线，返回图像上以该x为横坐标的点的绝对坐标
        """
        if hasattr(graph, "underlying_function"):
            return self.coords_to_point(x, graph.underlying_function(x))
        else:
            alpha = binary_search(
                function=lambda a: self.point_to_coords(
                    graph.quick_point_from_proportion(a)
                )[0],
                target=x,
                lower_bound=self.x_range[0],
                upper_bound=self.x_range[1],
            )
            if alpha is not None:
                return graph.quick_point_from_proportion(alpha)
            else:
                return None

    """
    dots.add_updater(lambda d: d[0].move_to(axes.i2gp(get_x(), graph)))
    """
    def i2gp(self, x: float, graph: ParametricCurve) -> Vect3 | None:
        """
        Alias for input_to_graph_point
        """
        """
        给定横坐标，返回图像上的点
        这里的x就是坐标轴的横坐标

        在manim中，有两种坐标系：
        1.axes中的坐标
        2.绝对坐标

        这里的x就是axes中的横坐标
        返回的绝对坐标（三维，第三维为0）
        """
        return self.input_to_graph_point(x, graph)

    """
    curve = axes.get_graph(lambda x: self.func(x, 1))
    axes.bind_graph_to_func(curve, lambda x: self.func(x, get_c()))

    视觉效果是：随着get_c()的变化，curve的图像也在变化
    """
    def bind_graph_to_func(
        self,
        graph: VMobject,
        func: Callable[[Vect3], Vect3],
        jagged: bool = False,
        get_discontinuities: Optional[Callable[[], Vect3]] = None
    ) -> VMobject:
        """
        Use for graphing functions which might change over time, or change with
        conditions
        """
        """
        graph本身是由点构成的
        传入了func，就可以得到新的一系列点
        进而可以绘制新的graph

        如果func是固定的，那么graph也是固定的
        然而，如果func中有一个参数可以变化，那么graph也会随参数变化而变化

        这才是这个函数的正确使用方法
        """
        # graph.get_points(): 获取graph的点（贝塞尔点），三维绝对坐标
        # self.x_axis.p2n(p): 将三维绝对坐标转换为x轴上的坐标
        # 这一步主要是想得到原先graph在x轴上的取值范围，方法会有很多
        # 特别需要注意的是graph.get_points()获得的是二维贝塞尔曲线的点集，包含曲线的首尾两个点
        x_values = np.array([self.x_axis.p2n(p) for p in graph.get_points()])
        #print("+"*100, "\n", x_values)

        def get_graph_points():
            xs = x_values
            if get_discontinuities:
                ds = get_discontinuities()
                ep = 1e-6
                added_xs = it.chain(*((d - ep, d + ep) for d in ds))
                xs[:] = sorted([*x_values, *added_xs])[:len(x_values)]
                
            # 注意，这里的xs是列表，func(xs)也是列表
            # self.c2p(xs, func(xs))返回的是一个三维向量的列表，点集
            return self.c2p(xs, func(xs))

        #print("-"*100, "\n", get_graph_points())
        graph.add_updater(
            lambda g: g.set_points_as_corners(get_graph_points())
        )
        # 同一个Mobject可以有多个updater
        if not jagged:
            graph.add_updater(lambda g: g.make_smooth(approx=True))
        
        """
        如何深入理解add_updater?
        视频是由多个帧组成的，每一个帧内有多个对象需要渲染
        如果对象没有添加任何updater，那么它的渲染是固定的
        如果对象添加了updater，那么它的渲染是动态的，即每一帧的时候都需要重新计算
        """
        return graph

    def get_graph_label(
        self,
        graph: ParametricCurve,
        label: str | Mobject = "f(x)",
        x: float | None = None,
        direction: Vect3 = RIGHT,
        buff: float = MED_SMALL_BUFF,
        color: ManimColor | None = None
    ) -> Tex | Mobject:
        """
        给函数图像标上文本标签
        """
        if isinstance(label, str):
            label = Tex(label)
        if color is None:
            label.match_color(graph)
        if x is None:
            # Searching from the right, find a point
            # whose y value is in bounds
            max_y = FRAME_Y_RADIUS - label.get_height()
            max_x = FRAME_X_RADIUS - label.get_width()

            for x0 in np.arange(*self.x_range)[::-1]:
                pt = self.i2gp(x0, graph)
                if abs(pt[0]) < max_x and abs(pt[1]) < max_y:
                    x = x0
                    break
            if x is None:
                x = self.x_range[1]

        point = self.input_to_graph_point(x, graph)
        angle = self.angle_of_tangent(x, graph)
        # print(point, angle)

        normal = rotate_vector(RIGHT, angle + 90 * DEGREES)
        if normal[1] < 0:
            normal *= -1
        label.next_to(point, normal, buff=buff)
        label.shift_onto_screen()
        return label

    def get_v_line_to_graph(self, x: float, graph: ParametricCurve, **kwargs):
        '''以 x 为横坐标作铅垂线并与函数图像相交'''
        return self.get_v_line(self.i2gp(x, graph), **kwargs)

    def get_h_line_to_graph(self, x: float, graph: ParametricCurve, **kwargs):
        '''以 x 为纵坐标~~（为什么不用 y 呢）~~作水平线并与函数图像相交'''
        return self.get_h_line(self.i2gp(x, graph), **kwargs)

    def get_scatterplot(self,
                        x_values: Vect3Array,
                        y_values: Vect3Array,
                        **dot_config):
        return DotCloud(self.c2p(x_values, y_values), **dot_config)

    # For calculus
    def angle_of_tangent(
        self,
        x: float,
        graph: ParametricCurve,
        dx: float = EPSILON
    ) -> float:
        '''获取横坐标为 x 的点处切线的倾斜角'''
        p0 = self.input_to_graph_point(x, graph)
        p1 = self.input_to_graph_point(x + dx, graph)
        return angle_of_vector(p1 - p0)

    def slope_of_tangent(
        self,
        x: float,
        graph: ParametricCurve,
        **kwargs
    ) -> float:
        '''获取横坐标为 x 的点处切线的斜率'''
        return np.tan(self.angle_of_tangent(x, graph, **kwargs))

    def get_tangent_line(
        self,
        x: float,
        graph: ParametricCurve,
        length: float = 5,
        line_func: Type[T] = Line
    ) -> T:
        '''绘制横坐标为 x 的点处的切线，返回一个 Line Mobject'''
        # 思路巧妙
        line = line_func(LEFT, RIGHT)
        line.set_width(length)
        line.rotate(self.angle_of_tangent(x, graph))
        line.move_to(self.input_to_graph_point(x, graph))
        return line

    """
    colors = (BLUE_E, BLUE_D, TEAL_D, TEAL_E)
    rects = axes.get_riemann_rectangles(curve, dx=0.2, colors=colors)
    """
    def get_riemann_rectangles(
        self,
        graph: ParametricCurve,
        x_range: Sequence[float] = None,
        dx: float | None = None,
        input_sample_type: str = "left",
        stroke_width: float = 1,
        stroke_color: ManimColor = BLACK,
        fill_opacity: float = 1,
        colors: Iterable[ManimColor] = (BLUE, GREEN),
        negative_color: ManimColor = RED,
        stroke_background: bool = True,
        show_signed_area: bool = True
    ) -> VGroup:
        '''
        绘制一系列黎曼矩形填充图像下方的区域

        - ``x_range = [x_min, x_max, dx]`` 可以指定范围，其中 ``dx`` 为分割精度
        - ``input_sample_type`` 指定矩形的左上角、上边缘中心、右上角抵在图像上
        '''
        if x_range is None:
            x_range = self.x_range[:2]
        if dx is None:
            dx = self.x_range[2]
        if len(x_range) < 3:
            x_range = [*x_range, dx]

        rects = []
        x_range[1] = x_range[1] + dx
        xs = np.arange(*x_range)
        
        for x0, x1 in zip(xs, xs[1:]):
            # x0和x1分别是矩形的左下角和右下角的横坐标
            if input_sample_type == "left":
                sample = x0
            elif input_sample_type == "right":
                sample = x1
            elif input_sample_type == "center":
                sample = 0.5 * x0 + 0.5 * x1
            else:
                raise Exception("Invalid input sample type")
            
            # self.i2gp(sample, graph)：返回图像上以sample为横坐标的点的绝对坐标
            # self.c2p(sample, 0)：返回坐标轴上以sample为横坐标的点的绝对坐标
            height_vect = self.i2gp(sample, graph) - self.c2p(sample, 0)
            rect = Rectangle(
                width=self.x_axis.n2p(x1)[0] - self.x_axis.n2p(x0)[0],
                height=get_norm(height_vect),
            )
            # 矩形在x轴上方还是下方
            rect.positive = height_vect[1] > 0
            # 如果矩形在x轴上方，那么矩形的左下角和self.c2p(x0, 0)重合
            # 如果矩形在x轴下方，那么矩形的左上角和self.c2p(x0, 0)重合
            rect.move_to(self.c2p(x0, 0), DL if rect.positive else UL)
            rects.append(rect)
        
        result = VGroup(*rects)
        # 大为震惊，可以为submobject设置渐变色
        result.set_submobject_colors_by_gradient(*colors)
        result.set_style(
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            fill_opacity=fill_opacity,
            stroke_background=stroke_background
        )
        for rect in result:
            if not rect.positive:
                rect.set_fill(negative_color)
        return result

    def get_area_under_graph(self, graph, x_range, fill_color=BLUE, fill_opacity=1):
        # TODO
        pass

# 没想到，Axes继承自VGroup
class Axes(VGroup, CoordinateSystem):
    default_axis_config: dict = dict()
    default_x_axis_config: dict = dict()
    default_y_axis_config: dict = dict(line_to_number_direction=LEFT)

    def __init__(
        self,
        x_range: RangeSpecifier = DEFAULT_X_RANGE,
        y_range: RangeSpecifier = DEFAULT_Y_RANGE,
        axis_config: dict = dict(),
        x_axis_config: dict = dict(),
        y_axis_config: dict = dict(),
        height: float | None = None,
        width: float | None = None,
        unit_size: float = 1.0,
        **kwargs
    ):
        CoordinateSystem.__init__(self, x_range, y_range, **kwargs)
        VGroup.__init__(self, **kwargs)

        axis_config = dict(**axis_config, unit_size=unit_size)
        self.x_axis = self.create_axis(
            self.x_range,
            axis_config=merge_dicts_recursively(
                self.default_axis_config,
                self.default_x_axis_config,
                axis_config,
                x_axis_config
            ),
            length=width,
        )
        self.y_axis = self.create_axis(
            self.y_range,
            axis_config=merge_dicts_recursively(
                self.default_axis_config,
                self.default_y_axis_config,
                axis_config,
                y_axis_config
            ),
            length=height,
        )
        self.y_axis.rotate(90 * DEGREES, about_point=ORIGIN)
        # Add as a separate group in case various other
        # mobjects are added to self, as for example in
        # NumberPlane below
        self.axes = VGroup(self.x_axis, self.y_axis)
        self.add(*self.axes)
        self.center()

    def create_axis(
        self,
        range_terms: RangeSpecifier,
        axis_config: dict,
        length: float | None
    ) -> NumberLine:
        axis = NumberLine(range_terms, width=length, **axis_config)
        axis.shift(-axis.n2p(0))
        return axis

    def coords_to_point(self, *coords: float | VectN) -> Vect3 | Vect3Array:
        """输入坐标轴上的二维坐标，返回场景的绝对坐标，(x, y) -> array([x', y', 0])"""
        # 坐标原点的绝对坐标
        origin = self.x_axis.number_to_point(0)
        # 从向量合成的角度去理解
        """
        1.计算point在x轴的投影向量
        2.计算point在y轴的投影向量
        3.将两个投影向量相加，得到point相对于origin的向量
        4. origin + point相对于origin的向量 = point的绝对坐标
        """
        return origin + sum(
            axis.number_to_point(coord) - origin # x or y向量
            for axis, coord in zip(self.get_axes(), coords)
        )

    def point_to_coords(self, point: Vect3 | Vect3Array) -> tuple[float | VectN, ...]:
        """输入场景的绝对坐标，返回坐标轴上的二维坐标，array([x, y, 0]) -> (x', y')"""
        return tuple([
            axis.point_to_number(point)
            for axis in self.get_axes()
        ])

    def get_axes(self) -> VGroup:
        return self.axes

    def get_all_ranges(self) -> list[Sequence[float]]:
        return [self.x_range, self.y_range]

    def add_coordinate_labels(
        self,
        x_values: Iterable[float] | None = None,
        y_values: Iterable[float] | None = None,
        excluding: Iterable[float] = [0],
        **kwargs
    ) -> VGroup:
        '''给坐标轴标上数字'''
        axes = self.get_axes()
        self.coordinate_labels = VGroup()
        for axis, values in zip(axes, [x_values, y_values]):
            labels = axis.add_numbers(values, excluding=excluding, **kwargs)
            self.coordinate_labels.add(labels)
        return self.coordinate_labels


class ThreeDAxes(Axes):
    dimension: int = 3
    default_z_axis_config: dict = dict()

    def __init__(
        self,
        x_range: RangeSpecifier = (-6.0, 6.0, 1.0),
        y_range: RangeSpecifier = (-5.0, 5.0, 1.0),
        z_range: RangeSpecifier = (-4.0, 4.0, 1.0),
        z_axis_config: dict = dict(),
        z_normal: Vect3 = DOWN,
        depth: float = 6.0,
        flat_stroke: bool = False,
        **kwargs
    ):
        Axes.__init__(self, x_range, y_range, **kwargs)

        self.z_range = z_range
        self.z_axis = self.create_axis(
            self.z_range,
            axis_config=merge_dicts_recursively(
                self.default_axis_config,
                self.default_z_axis_config,
                kwargs.get("axes_config", {}),
                z_axis_config
            ),
            length=depth,
        )
        # 对于rotate函数的理解还不到位
        self.z_axis.rotate(-PI / 2, UP, about_point=ORIGIN)
        self.z_axis.rotate(
            angle_of_vector(z_normal), OUT,
            about_point=ORIGIN
        )
        self.z_axis.shift(self.x_axis.n2p(0))
        self.axes.add(self.z_axis)
        self.add(self.z_axis)

        self.set_flat_stroke(flat_stroke)

    def get_all_ranges(self) -> list[Sequence[float]]:
        return [self.x_range, self.y_range, self.z_range]

    def add_axis_labels(self, x_tex="x", y_tex="y", z_tex="z", font_size=24, buff=0.2):
        x_label, y_label, z_label = labels = VGroup(*(
            Tex(tex, font_size=font_size)
            for tex in [x_tex, y_tex, z_tex]
        ))
        z_label.rotate(PI / 2, RIGHT)
        for label, axis in zip(labels, self):
            label.next_to(axis, normalize(np.round(axis.get_vector()), 2), buff=buff)
            axis.add(label)
        self.axis_labels = labels

    # 研究下代码实现
    def get_graph(self, func, color=BLUE_E, opacity=0.9, **kwargs):
        xu = self.x_axis.get_unit_size()
        yu = self.y_axis.get_unit_size()
        zu = self.z_axis.get_unit_size()
        x0, y0, z0 = self.get_origin()
        # 曲线：需要点集（所有的点在一个平面上）
        # 曲面：需要点集（曲面的底面是一个围棋面）
        return ParametricSurface(
            lambda u, v: [xu * u + x0, yu * v + y0, zu * func(u, v) + z0], # 坐标轴上的刻度 * 单位长度 = 实际的长度
            u_range=self.x_range[:2], # x轴的范围。x_range = (-6.0, 6.0, 1.0)。x_range[:2] = (-6.0, 6.0)。
            v_range=self.y_range[:2],
            color=color,
            opacity=opacity,
            **kwargs
        )


class NumberPlane(Axes):
    '''带有网格线的二维坐标系'''
    default_axis_config: dict = dict(
        stroke_color=WHITE,
        stroke_width=2,
        include_ticks=False,
        include_tip=False,
        line_to_number_buff=SMALL_BUFF,
        line_to_number_direction=DL,
    )
    default_y_axis_config: dict = dict(
        line_to_number_direction=DL,
    )

    def __init__(
        self,
        x_range: RangeSpecifier = (-8.0, 8.0, 1.0),
        y_range: RangeSpecifier = (-4.0, 4.0, 1.0),
        background_line_style: dict = dict(
            stroke_color=BLUE_D,
            stroke_width=2,
            stroke_opacity=1,
        ),
        # Defaults to a faded version of line_config
        faded_line_style: dict = dict(),
        faded_line_ratio: int = 4,
        make_smooth_after_applying_functions: bool = True,
        **kwargs
    ):
        super().__init__(x_range, y_range, **kwargs)
        self.background_line_style = dict(background_line_style)
        self.faded_line_style = dict(faded_line_style)
        self.faded_line_ratio = faded_line_ratio
        self.make_smooth_after_applying_functions = make_smooth_after_applying_functions
        self.init_background_lines()

    def init_background_lines(self) -> None:
        if not self.faded_line_style:
            style = dict(self.background_line_style)
            # For anything numerical, like stroke_width
            # and stroke_opacity, chop it in half
            for key in style:
                if isinstance(style[key], numbers.Number):
                    style[key] *= 0.5
            self.faded_line_style = style

        self.background_lines, self.faded_lines = self.get_lines()
        self.background_lines.set_style(**self.background_line_style)
        self.faded_lines.set_style(**self.faded_line_style)
        self.add_to_back(
            self.faded_lines,
            self.background_lines,
        )

    def get_lines(self) -> tuple[VGroup, VGroup]:
        x_axis = self.get_x_axis()
        y_axis = self.get_y_axis()

        x_lines1, x_lines2 = self.get_lines_parallel_to_axis(x_axis, y_axis)
        y_lines1, y_lines2 = self.get_lines_parallel_to_axis(y_axis, x_axis)
        lines1 = VGroup(*x_lines1, *y_lines1)
        lines2 = VGroup(*x_lines2, *y_lines2)
        return lines1, lines2

    def get_lines_parallel_to_axis(
        self,
        axis1: NumberLine,
        axis2: NumberLine
    ) -> tuple[VGroup, VGroup]:
        freq = axis2.x_step
        ratio = self.faded_line_ratio
        line = Line(axis1.get_start(), axis1.get_end())
        dense_freq = (1 + ratio)
        step = (1 / dense_freq) * freq

        lines1 = VGroup()
        lines2 = VGroup()
        inputs = np.arange(axis2.x_min, axis2.x_max + step, step)
        for i, x in enumerate(inputs):
            if abs(x) < 1e-8:
                continue
            new_line = line.copy()
            new_line.shift(axis2.n2p(x) - axis2.n2p(0))
            if i % (1 + ratio) == 0:
                lines1.add(new_line)
            else:
                lines2.add(new_line)
        return lines1, lines2

    def get_x_unit_size(self) -> float:
        return self.get_x_axis().get_unit_size()

    def get_y_unit_size(self) -> list:
        return self.get_x_axis().get_unit_size()

    def get_axes(self) -> VGroup:
        return self.axes

    def get_vector(self, coords: Iterable[float], **kwargs) -> Arrow:
        '''输入一个二维坐标，绘制一个【从坐标轴原点到该点的向量】'''
        kwargs["buff"] = 0
        return Arrow(self.c2p(0, 0), self.c2p(*coords), **kwargs)

    def prepare_for_nonlinear_transform(self, num_inserted_curves: int = 50) -> Self:
        '''将坐标系的每一条线进行分割，以适配即将施加的非线性变换'''
        for mob in self.family_members_with_points():
            num_curves = mob.get_num_curves()
            if num_inserted_curves > num_curves:
                mob.insert_n_curves(num_inserted_curves - num_curves)
            mob.make_smooth_after_applying_functions = True
        return self


class ComplexPlane(NumberPlane):
    def number_to_point(self, number: complex | float) -> Vect3:
        number = complex(number)
        return self.coords_to_point(number.real, number.imag)

    def n2p(self, number: complex | float) -> Vect3:
        return self.number_to_point(number)

    def point_to_number(self, point: Vect3) -> complex:
        x, y = self.point_to_coords(point)
        return complex(x, y)

    def p2n(self, point: Vect3) -> complex:
        return self.point_to_number(point)

    def get_default_coordinate_values(
        self,
        skip_first: bool = True
    ) -> list[complex]:
        x_numbers = self.get_x_axis().get_tick_range()[1:]
        y_numbers = self.get_y_axis().get_tick_range()[1:]
        y_numbers = [complex(0, y) for y in y_numbers if y != 0]
        return [*x_numbers, *y_numbers]

    def add_coordinate_labels(
        self,
        numbers: list[complex] | None = None,
        skip_first: bool = True,
        font_size: int = 36,
        **kwargs
    ) -> Self:
        if numbers is None:
            numbers = self.get_default_coordinate_values(skip_first)

        self.coordinate_labels = VGroup()
        for number in numbers:
            z = complex(number)
            if abs(z.imag) > abs(z.real):
                axis = self.get_y_axis()
                value = z.imag
                kwargs["unit_tex"] = "i"
            else:
                axis = self.get_x_axis()
                value = z.real
            number_mob = axis.get_number_mobject(value, font_size=font_size, **kwargs)
            # For -i, remove the "1"
            if z.imag == -1:
                number_mob.remove(number_mob[1])
                number_mob[0].next_to(
                    number_mob[1], LEFT,
                    buff=number_mob[0].get_width() / 4
                )
            self.coordinate_labels.add(number_mob)
        self.add(self.coordinate_labels)
        return self
