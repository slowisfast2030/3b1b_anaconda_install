from __future__ import annotations

from manimlib.animation.animation import Animation

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable

    from manimlib.mobject.mobject import Mobject


"""
rect = Rectangle().set_color(BLUE)
ball_1 = Dot().set_color(RED)
ball_2 = Dot().set_color(YELLOW)
self.play(
    ShowCreation(rect, run_time=2),
    UpdateFromFunc(ball_1, lambda m: m.move_to(rect.get_end())),
    ball_2.animate.move_to(rect.get_end())              
)

ball_1的动画符合预期
ball_2的动画不符合预期
这里需要对animate函数的本质有着进一步的理解
animate后面可以跟着很多的属性设置，本质上会产生一个target_mobject
整个animate动画等价于MoveToTarget(ball_2)
"""
class UpdateFromFunc(Animation):
    """
    update_function of the form func(mobject), presumably
    to be used when the state of one mobject is dependent
    on another simultaneously animated mobject
    """
    def __init__(
        self,
        mobject: Mobject,
        update_function: Callable[[Mobject], Mobject | None],
        suspend_mobject_updating: bool = False,
        **kwargs
    ):
        self.update_function = update_function
        super().__init__(
            mobject,
            suspend_mobject_updating=suspend_mobject_updating,
            **kwargs
        )

    def interpolate_mobject(self, alpha: float) -> None:
        self.update_function(self.mobject)


class UpdateFromAlphaFunc(Animation):
    def __init__(
        self,
        mobject: Mobject,
        update_function: Callable[[Mobject, float], Mobject | None], # update函数需要mob和dt两个参数
        suspend_mobject_updating: bool = False,
        **kwargs
    ):
        self.update_function = update_function
        super().__init__(mobject, suspend_mobject_updating=suspend_mobject_updating, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        self.update_function(self.mobject, alpha)


"""
ball_1 = Dot().set_color(RED).shift(LEFT*2)
ball_2 = Dot().set_color(YELLOW)
self.add(ball_1, ball_2)

self.play(
    ball_2.animate.shift(RIGHT*2),
    MaintainPositionRelativeTo(ball_1, ball_2)
)
"""
class MaintainPositionRelativeTo(Animation):
    def __init__(
        self,
        mobject: Mobject,
        tracked_mobject: Mobject,
        **kwargs
    ):
        self.tracked_mobject = tracked_mobject
        self.diff = mobject.get_center() - tracked_mobject.get_center()
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        target = self.tracked_mobject.get_center()
        location = self.mobject.get_center()
        self.mobject.shift(target - location + self.diff)
        # 下面代码是自己加的，可以将整个向量的移动分解为两个部分
        # self.mobject.shift(target - location)
        # self.mobject.shift(self.diff)
