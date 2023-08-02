from __future__ import annotations

import numpy as np

from manimlib.animation.animation import Animation
from manimlib.animation.animation import prepare_animation
from manimlib.mobject.mobject import _AnimationBuilder
from manimlib.mobject.mobject import Group
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.utils.bezier import integer_interpolate
from manimlib.utils.bezier import interpolate
from manimlib.utils.iterables import remove_list_redundancies
from manimlib.utils.simple_functions import clip

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Optional

    from manimlib.mobject.mobject import Mobject
    from manimlib.scene.scene import Scene


DEFAULT_LAGGED_START_LAG_RATIO = 0.05


"""
c = Circle().set_color(RED)
s = Square().set_color(BLUE)
t = Triangle().set_color(GREEN)
d = Dot().set_color(YELLOW)
animations = [Write(c),
              Write(s),
              Write(t),
              d.animate.shift(LEFT*2)]   

self.play(AnimationGroup(*animations, lag_ratio=1, run_time=4))

ag = AnimationGroup(*animations, lag_ratio=1, run_time=4)
print(ag.group, ag.group.submobjects)

VGroup 

[
<manimlib.mobject.geometry.Circle object at 0x142e17a90>, 
<manimlib.mobject.geometry.Square object at 0x14300f730>, 
<manimlib.mobject.geometry.Triangle object at 0x14300f790>, 
<manimlib.mobject.geometry.Dot object at 0x14300f8e0>
]
"""
class AnimationGroup(Animation):
    '''动画组，可以传入一系列动画，统一播放'''
    def __init__(self,
        *animations: Animation | _AnimationBuilder,
        run_time: float = -1,  # If negative, default to sum of inputed animation runtimes
        lag_ratio: float = 0.0,
        group: Optional[Mobject] = None,
        group_type: Optional[type] = None,
        **kwargs
    ):  
        # 动画列表
        self.animations = [prepare_animation(anim) for anim in animations]
        # 计算每一个动画的开始时间和结束时间
        self.build_animations_with_timings(lag_ratio)
        # 计算所有动画的最大的结束时间
        self.max_end_time = max((awt[2] for awt in self.anims_with_timings), default=0)
        # 动画的持续时间
        self.run_time = self.max_end_time if run_time < 0 else run_time
        self.lag_ratio = lag_ratio
        # 去除冗余的mobject
        mobs = remove_list_redundancies([a.mobject for a in self.animations])
        # 设置group属性
        if group is not None:
            self.group = group
        if group_type is not None:
            self.group = group_type(*mobs)
        elif all(isinstance(anim.mobject, VMobject) for anim in animations): # 每一个动画都有一个mobject
            self.group = VGroup(*mobs)
        else:
            self.group = Group(*mobs)

        super().__init__(
            self.group,
            run_time=self.run_time,
            lag_ratio=lag_ratio,
            **kwargs
        )

    def get_all_mobjects(self) -> Mobject:
        return self.group

    def begin(self) -> None:
        self.group.set_animating_status(True)
        for anim in self.animations:
            anim.begin()
        # self.init_run_time()

    def finish(self) -> None:
        self.group.set_animating_status(False)
        for anim in self.animations:
            anim.finish()

    def clean_up_from_scene(self, scene: Scene) -> None:
        for anim in self.animations:
            anim.clean_up_from_scene(scene)

    def update_mobjects(self, dt: float) -> None:
        """
        animation和update应该是不能同时执行的
        这里为什么又定义了这个函数？
        """
        for anim in self.animations:
            anim.update_mobjects(dt)

    def calculate_max_end_time(self) -> None:
        """
        计算最大的结束时间

        备注：这个函数似乎没有被调用过
        """
        self.max_end_time = max(
            (awt[2] for awt in self.anims_with_timings),
            default=0,
        )
        if self.run_time < 0:
            self.run_time = self.max_end_time

    def build_animations_with_timings(self, lag_ratio: float) -> None:
        """
        Creates a list of triplets of the form
        (anim, start_time, end_time)
        """
        self.anims_with_timings = []
        curr_time = 0
        for anim in self.animations:
            start_time = curr_time
            end_time = start_time + anim.get_run_time()
            self.anims_with_timings.append(
                (anim, start_time, end_time)
            )
            # Start time of next animation is based on the lag_ratio
            """
            秀的头皮发麻
            """
            curr_time = interpolate(
                start_time, end_time, lag_ratio
            )

    def interpolate(self, alpha: float) -> None:
        # Note, if the run_time of AnimationGroup has been
        # set to something other than its default, these
        # times might not correspond to actual times,
        # e.g. of the surrounding scene.  Instead they'd
        # be a rescaled version.  But that's okay!
        """
        alpha: 整个动画的进度
        sub_alpha: 每一个动画的进度
        可以通过alpha计算出sub_alpha
        """
        time = alpha * self.max_end_time
        for anim, start_time, end_time in self.anims_with_timings:
            anim_time = end_time - start_time
            if anim_time == 0:
                sub_alpha = 0
            else:
                sub_alpha = clip((time - start_time) / anim_time, 0, 1)
            anim.interpolate(sub_alpha)


"""
c = Circle().set_color(RED)
s = Square().set_color(BLUE)
t = Triangle().set_color(GREEN)
d = Dot().set_color(YELLOW)

animations = [Write(c),
              Write(s),
              Write(t),
              d.animate.shift(LEFT*2)]   

self.play(Succession(*animations))

基本功能是实现了，但是不明白为什么在动画开始前，屏幕上已经显示了部分mob
"""
class Succession(AnimationGroup):
    '''使子动画逐一播放'''
    def __init__(
        self,
        *animations: Animation,
        lag_ratio: float = 1.0, #这里即使改成0，各个动画也是依次执行 
        **kwargs
    ):
        super().__init__(*animations, lag_ratio=lag_ratio, **kwargs)

    def begin(self) -> None:
        assert(len(self.animations) > 0)
        self.active_animation = self.animations[0]
        self.active_animation.begin()

    def finish(self) -> None:
        self.active_animation.finish()

    def update_mobjects(self, dt: float) -> None:
        self.active_animation.update_mobjects(dt)

    def interpolate(self, alpha: float) -> None:
        index, subalpha = integer_interpolate(
            0, len(self.animations), alpha
        )
        # print("+-"*50)
        # print(index, subalpha)
        """
        以上面的代码为例
        index: 0, subalpha: 0.0~1.0
        index: 1, subalpha: 0.0~1.0
        index: 2, subalpha: 0.0~1.0
        index: 3, subalpha: 0.0~1.0
        """
        animation = self.animations[index]
        if animation is not self.active_animation:
            self.active_animation.finish()
            animation.begin()
            self.active_animation = animation
        animation.interpolate(subalpha)


"""
c = Circle().set_color(RED)
s = Square().set_color(BLUE)
t = Triangle().set_color(GREEN)
d = Dot().set_color(YELLOW)

animations = [c.animate.shift(DOWN*2),
                s.animate.shift(UP*2),
                t.animate.shift(RIGHT*2),
                d.animate.shift(LEFT*2)]   

self.play(LaggedStart(*animations, lag_ratio=0))
"""
class LaggedStart(AnimationGroup):
    '''可以统一控制 ``lag_ratio`` 的动画组'''
    def __init__(
        self,
        *animations,
        lag_ratio: float = DEFAULT_LAGGED_START_LAG_RATIO, # lag_ratio = 0时，所有动画同时开始
        **kwargs
    ):
        super().__init__(*animations, lag_ratio=lag_ratio, **kwargs)


"""
self.play(
        LaggedStart(*(
            dot.animate.set_radius(0.1).set_opacity(self.dot_fade_factor)
            for dot in dots
        ), **kw),
        LaggedStartMap(FadeOut, labels, **kw),
        LaggedStartMap(FadeOut, lines[:2], **kw),
)
"""
"""
self.play(
        LaggedStartMap(
            FadeIn, VGroup(*blocks[10:30]),
            lag_ratio=0.9,
        ),
        run_time=12,
)
"""
class LaggedStartMap(LaggedStart):
    '''统一控制 **动画类**、 ``mobjects``、 ``lag_ratio`` 的动画组'''
    def __init__(
        self,
        anim_func: Callable[[Mobject], Animation],
        group: Mobject,
        arg_creator: Callable[[Mobject], tuple] | None = None,
        run_time: float = 2.0,
        lag_ratio: float = DEFAULT_LAGGED_START_LAG_RATIO,
        **kwargs
    ):
        anim_kwargs = dict(kwargs)
        anim_kwargs.pop("lag_ratio", None)
        super().__init__(
            *(anim_func(submob, **anim_kwargs) for submob in group),
            run_time=run_time,
            lag_ratio=lag_ratio,
        )
