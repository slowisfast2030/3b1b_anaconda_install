from __future__ import annotations

import inspect

import numpy as np

from manimlib.animation.animation import Animation
from manimlib.constants import DEGREES
from manimlib.constants import OUT
from manimlib.mobject.mobject import Group
from manimlib.mobject.mobject import Mobject
from manimlib.utils.paths import path_along_arc
from manimlib.utils.paths import straight_path

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable
    import numpy.typing as npt
    from manimlib.scene.scene import Scene
    from manimlib.typing import ManimColor


class Transform(Animation):
    replace_mobject_with_target_in_scene: bool = False

    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject | None = None,
        path_arc: float = 0.0,
        path_arc_axis: np.ndarray = OUT,
        path_func: Callable | None = None,
        **kwargs
    ):
        self.target_mobject = target_mobject
        self.path_arc = path_arc
        self.path_arc_axis = path_arc_axis
        self.path_func = path_func
        super().__init__(mobject, **kwargs)
        self.init_path_func()

    def init_path_func(self) -> None:
        if self.path_func is not None:
            return
        elif self.path_arc == 0:
            self.path_func = straight_path
        else:
            self.path_func = path_along_arc(
                self.path_arc,
                self.path_arc_axis,
            )

    def begin(self) -> None:
        self.target_mobject = self.create_target()
        self.check_target_mobject_validity()

        if self.mobject.is_aligned_with(self.target_mobject):
            self.target_copy = self.target_mobject
        else:
            # Use a copy of target_mobject for the align_data_and_family
            # call so that the actual target_mobject stays
            # preserved, since calling align_data will potentially
            # change the structure of both arguments
            # 对齐操作会改变两个mobject的结构
            self.target_copy = self.target_mobject.copy()
        """
        以前有一个很大的疑问：如何对circle和square进行插值？
        它们的点集的数目是不一样的
        现在看来，这个问题的关键在于，如何对两个mobject进行对齐
        """
        self.mobject.align_data_and_family(self.target_copy)
        super().begin()
        if not self.mobject.has_updaters:
            self.mobject.lock_matching_data(
                self.starting_mobject,
                self.target_copy,
            )

    def finish(self) -> None:
        super().finish()
        self.mobject.unlock_data()
        #print("-"*100)
        #print("transform class finish method ===>")

    def create_target(self) -> Mobject:
        # Has no meaningful effect here, but may be useful
        # in subclasses
        return self.target_mobject

    def check_target_mobject_validity(self) -> None:
        if self.target_mobject is None:
            raise Exception(
                f"{self.__class__.__name__}.create_target not properly implemented"
            )

    def clean_up_from_scene(self, scene: Scene) -> None:
        """
        play函数真是黑箱啊
        这个clean_up_from_scene函数是在play的哪一个阶段执行的？
        应该是alpha = 1之后才执行

        通过print语句，发现这个函数是在finish函数之后执行的
        """
        #print("-"*100)
        #print("transform class clean_up_from_scene method ===>")
        super().clean_up_from_scene(scene)
        # 一个疑问：动画结束之后，self.mobject和self.target_mobject是不是相等的？
        # 如果相等，这里的remove和add操作是不是多余的？
        if self.replace_mobject_with_target_in_scene:
            scene.remove(self.mobject)
            scene.add(self.target_mobject)

    def update_config(self, **kwargs) -> None:
        Animation.update_config(self, **kwargs)
        if "path_arc" in kwargs:
            self.path_func = path_along_arc(
                kwargs["path_arc"],
                kwargs.get("path_arc_axis", OUT)
            )

    def get_all_mobjects(self) -> list[Mobject]:
        return [
            self.mobject,
            self.starting_mobject,
            self.target_mobject,
            self.target_copy,
        ]

    def get_all_families_zipped(self) -> zip[tuple[Mobject]]:
        return zip(*[
            mob.get_family()
            for mob in [
                self.mobject,
                self.starting_mobject,
                self.target_copy,
            ]
        ])

    # 特别注意，这个函数和父类的同名函数，参数个数不一致
    def interpolate_submobject(
        self,
        submob: Mobject,
        start: Mobject,
        target_copy: Mobject,
        alpha: float
    ):  
        # 想知道这一行代码有没有被执行
        # print("linus"*5)
        # 经过测试，这一行确实被执行了
        # 进一步查看函数的参数
        # print(submob, start, target_copy, alpha)
        # 打印的参数也符合预期
        # 但我直接调用却会报错
        """
        终于找到了原因：因为没有alignment
        begin函数中有对齐操作
        只有对齐了之后的mob之间才能进行插值
        """

        # 这一行代码是没有返回值的，然而，我可以给它加一个
        """
        animation一般有self.mobject和self.target_mobject
        在animation开始的时候，会设置self.starting_mobject = self.mobject.copy()

        然后，在后续所有的插值过程中，都是通过self.starting_mobject和self.target_mobject
        来更新self.mobject的属性
        """
        submob.interpolate(start, target_copy, alpha, self.path_func)
        # mm = submob.interpolate(start, target_copy, alpha, self.path_func)
        # print(start.get_points())
        # print(mm.get_points())
        # mm和submob的points是变化的，start和target_copy的points是不变的
        return self


class ReplacementTransform(Transform):
    """
    经过实际测试，ReplacementTransform和Transform的效果是一样的
    """
    replace_mobject_with_target_in_scene: bool = True


class TransformFromCopy(Transform):
    """
    经过实际测试，TransformFromCopy和Transform的效果是一样的
    """
    replace_mobject_with_target_in_scene: bool = True

    def __init__(self, mobject: Mobject, target_mobject: Mobject, **kwargs):
        super().__init__(mobject.copy(), target_mobject, **kwargs)


"""
frame = self.frame
frame.target = frame.generate_target()
frame.target.scale(1.75, about_edge=LEFT)
self.play(
    LaggedStartMap(
        FadeIn, VGroup(*blocks[10:30]),
        lag_ratio=0.9, # 将lag_ratio设置为0，所有的block同时出现
    ),
    MoveToTarget(frame, rate_func=rush_into),
    run_time=12,
    )
"""
"""
MoveToTarget这个类名字起得不好，容易让人误解
直观的印象就是将mobect移动到target的位置
但实际上，这个类的作用是将mobject的属性变成target的属性
包括点集，颜色，透明度等等

MoveToTarget这个类初始化需要一个mobject
给人的感觉是这个transform只需要一个对象
但实际上，这个类还需要一个target
只是这个target是通过拷贝mobject得到的
"""
"""
MoveToTarget这个类的作用是将mobject的属性变成target的属性
是现在的自己和过去的自己之间的一次变化
"""
class MoveToTarget(Transform):
    def __init__(self, mobject: Mobject, **kwargs):
        # 检查mobject是否有target属性
        self.check_validity_of_input(mobject)
        super().__init__(mobject, mobject.target, **kwargs)

    def check_validity_of_input(self, mobject: Mobject) -> None:
        if not hasattr(mobject, "target"):
            raise Exception(
                "MoveToTarget called on mobject without attribute 'target'"
            )


class _MethodAnimation(MoveToTarget):
    def __init__(self, mobject: Mobject, methods: list[Callable], **kwargs):
        self.methods = methods
        super().__init__(mobject, **kwargs)


"""
x = ValueTracker(0)
self.play(ApplyMethod(x.increment_value, 3, run_time=5))

self.play(ApplyMethod(sine.shift, 4*LEFT, **kwargs))

self.play(*[
            ApplyMethod(mob.scale, 0.5*random.random(), **kwargs)
            for mob in self.intervals
        ])
        
ApplyMethod类隐含了插值么？没搞懂

感觉用updater实现同样的效果更加简单
"""
class ApplyMethod(Transform):
    def __init__(self, method: Callable, *args, **kwargs):
        """
        method is a method of Mobject, *args are arguments for
        that method.  Key word arguments should be passed in
        as the last arg, as a dict, since **kwargs is for
        configuration of the transform itself

        Relies on the fact that mobject methods return the mobject
        """
        self.check_validity_of_input(method)
        self.method = method
        self.method_args = args
        # 需要注意，这里的参数method是mob.func这种格式
        # 所以，method.__self__是mob
        super().__init__(method.__self__, **kwargs)

    def check_validity_of_input(self, method: Callable) -> None:
        if not inspect.ismethod(method):
            raise Exception(
                "Whoops, looks like you accidentally invoked "
                "the method you want to animate"
            )
        assert(isinstance(method.__self__, Mobject))

    def create_target(self) -> Mobject:
        """
        这个函数会在begin函数中被调用
        但是在整个动画过程中，只会被调用一次
        
        而这个方法中
        method.__func__(target, *args, **method_kwargs)
        被调用了
        那么，这次的ApplyMethod不就一步到位了么？
        也就是说，动画在begin函数中就结束了

        困惑...
        搞错了，上述函数是设置了target的属性

        实际print后发现，执行method.__func__(target, *args, **method_kwargs)之后
        self.method.__self__.get_value()仍然是初始值
        """
        method = self.method
        # Make sure it's a list so that args.pop() works
        args = list(self.method_args)

        if len(args) > 0 and isinstance(args[-1], dict):
            method_kwargs = args.pop()
        else:
            method_kwargs = {}
        target = method.__self__.copy()
        # 函数被调用，为target设置属性
        # 这样target就准备好了，后续就可以插值了
        method.__func__(target, *args, **method_kwargs)
        
        #print("&"*100)
        #print(self.method.__self__.get_value())
        # 这里打印的是self.mobject的value值
        return target


class ApplyPointwiseFunction(ApplyMethod):
    """
    将function作用于mobject的每一个点

    本可以直接调用mob.apply_function(function)
    但是这样做的话，就没有动画效果了
    """
    def __init__(
        self,
        function: Callable[[np.ndarray], np.ndarray],
        mobject: Mobject,
        run_time: float = 3.0,
        **kwargs
    ):
        super().__init__(mobject.apply_function, function, run_time=run_time, **kwargs)


class ApplyPointwiseFunctionToCenter(Transform):
    def __init__(
        self,
        function: Callable[[np.ndarray], np.ndarray],
        mobject: Mobject,
        **kwargs
    ):
        self.function = function
        super().__init__(mobject, **kwargs)

    def create_target(self) -> Mobject:
        return self.mobject.copy().move_to(self.function(self.mobject.get_center()))


class FadeToColor(ApplyMethod):
    def __init__(
        self,
        mobject: Mobject,
        color: ManimColor,
        **kwargs
    ):
        super().__init__(mobject.set_color, color, **kwargs)


class ScaleInPlace(ApplyMethod):
    def __init__(
        self,
        mobject: Mobject,
        scale_factor: npt.ArrayLike,
        **kwargs
    ):
        super().__init__(mobject.scale, scale_factor, **kwargs)


class ShrinkToCenter(ScaleInPlace):
    def __init__(self, mobject: Mobject, **kwargs):
        super().__init__(mobject, 0, **kwargs)


class Restore(Transform):
    def __init__(self, mobject: Mobject, **kwargs):
        if not hasattr(mobject, "saved_state") or mobject.saved_state is None:
            raise Exception("Trying to restore without having saved")
        super().__init__(mobject, mobject.saved_state, **kwargs)


class ApplyFunction(Transform):
    """
    和ApplyMethod类进行对比

    通过function对mobject进行变换，得到target
    然后执行插值操作
    """
    def __init__(
        self,
        function: Callable[[Mobject], Mobject],
        mobject: Mobject,
        **kwargs
    ):
        self.function = function
        super().__init__(mobject, **kwargs)

    def create_target(self) -> Mobject:
        target = self.function(self.mobject.copy())
        if not isinstance(target, Mobject):
            raise Exception("Functions passed to ApplyFunction must return object of type Mobject")
        return target


class ApplyMatrix(ApplyPointwiseFunction):
    def __init__(
        self,
        matrix: npt.ArrayLike,
        mobject: Mobject,
        **kwargs
    ):
        matrix = self.initialize_matrix(matrix)

        def func(p):
            return np.dot(p, matrix.T)

        super().__init__(func, mobject, **kwargs)

    def initialize_matrix(self, matrix: npt.ArrayLike) -> np.ndarray:
        matrix = np.array(matrix)
        if matrix.shape == (2, 2):
            new_matrix = np.identity(3)
            new_matrix[:2, :2] = matrix
            matrix = new_matrix
        elif matrix.shape != (3, 3):
            raise Exception("Matrix has bad dimensions")
        return matrix


class ApplyComplexFunction(ApplyMethod):
    def __init__(
        self,
        function: Callable[[complex], complex],
        mobject: Mobject,
        **kwargs
    ):
        self.function = function
        method = mobject.apply_complex_function
        super().__init__(method, function, **kwargs)

    def init_path_func(self) -> None:
        func1 = self.function(complex(1))
        self.path_arc = np.log(func1).imag
        super().init_path_func()

###


class CyclicReplace(Transform):
    def __init__(self, *mobjects: Mobject, path_arc=90 * DEGREES, **kwargs):
        super().__init__(Group(*mobjects), path_arc=path_arc, **kwargs)

    def create_target(self) -> Mobject:
        group = self.mobject
        target = group.copy()
        cycled_targets = [target[-1], *target[:-1]]
        for m1, m2 in zip(cycled_targets, group):
            m1.move_to(m2)
        return target


class Swap(CyclicReplace):
    """Alternate name for CyclicReplace"""
    pass
