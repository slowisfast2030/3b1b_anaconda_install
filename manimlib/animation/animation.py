from __future__ import annotations

from copy import deepcopy

from manimlib.mobject.mobject import _AnimationBuilder
from manimlib.mobject.mobject import Mobject
from manimlib.utils.rate_functions import smooth
from manimlib.utils.rate_functions import squish_rate_func
from manimlib.utils.simple_functions import clip

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable

    from manimlib.scene.scene import Scene


DEFAULT_ANIMATION_RUN_TIME = 1.0
DEFAULT_ANIMATION_LAG_RATIO = 0

from manimlib.logger import log

class Animation(object):
    def __init__(
        self,
        mobject: Mobject,
        run_time: float = DEFAULT_ANIMATION_RUN_TIME,
        # Tuple of times, between which the animation will run
        time_span: tuple[float, float] | None = None,
        # If 0, the animation is applied to all submobjects at the same time
        # If 1, it is applied to each successively.
        # If 0 < lag_ratio < 1, its applied to each with lagged start times
        # 以前一直误解了lag_ratio这个参数的含义
        # 需要建立animation和submobject的关系
        lag_ratio: float = DEFAULT_ANIMATION_LAG_RATIO, 
        rate_func: Callable[[float], float] = smooth,
        name: str = "",
        # Does this animation add or remove a mobject form the screen
        remover: bool = False,
        # What to enter into the update function upon completion
        final_alpha_value: float = 1.0,
        suspend_mobject_updating: bool = True,
    ):
        self.mobject = mobject
        self.run_time = run_time
        self.time_span = time_span
        self.rate_func = rate_func
        self.name = name or self.__class__.__name__ + str(self.mobject)
        self.remover = remover
        self.final_alpha_value = final_alpha_value
        self.lag_ratio = lag_ratio
        self.suspend_mobject_updating = suspend_mobject_updating

        self.count = 0

        assert(isinstance(mobject, Mobject))

    def __str__(self) -> str:
        return self.name

    def begin(self) -> None:
        # This is called right as an animation is being
        # played.  As much initialization as possible,
        # especially any mobject copying, should live in
        # this method
        #print('\n')
        #log.info(f"animation begin ===>")
        if self.time_span is not None:
            start, end = self.time_span
            self.run_time = max(end, self.run_time)
            self.rate_func = squish_rate_func(
                self.rate_func, start / self.run_time, end / self.run_time,
            )
        # 设置mob._is_animating = True
        self.mobject.set_animating_status(True)
        self.starting_mobject = self.create_starting_mobject()
        if self.suspend_mobject_updating:
            # All calls to self.mobject's internal updaters
            # during the animation, either from this Animation
            # or from the surrounding scene, should do nothing.
            # It is, however, okay and desirable to call
            # the internal updaters of self.starting_mobject,
            # or any others among self.get_all_mobjects()
            self.mobject.suspend_updating()
        self.families = list(self.get_all_families_zipped())
        self.interpolate(0)

    def finish(self) -> None:
        #print('\n')
        #log.info(f"animation finish ===>")
        self.interpolate(self.final_alpha_value)
        self.mobject.set_animating_status(False)
        if self.suspend_mobject_updating:
            self.mobject.resume_updating()

    def clean_up_from_scene(self, scene: Scene) -> None:
        if self.is_remover():
            scene.remove(self.mobject)

    def create_starting_mobject(self) -> Mobject:
        # Keep track of where the mobject starts
        return self.mobject.copy()

    def get_all_mobjects(self) -> tuple[Mobject, Mobject]:
        """
        Ordering must match the ording of arguments to interpolate_submobject
        """
        return self.mobject, self.starting_mobject

    def get_all_families_zipped(self) -> zip[tuple[Mobject]]:
        return zip(*[
            mob.get_family()
            for mob in self.get_all_mobjects()
        ])

    # 有一个深刻的问题值得思考：
    # 动画的插值和对象的更新的先后关系是什么？
    # 按道理来说，是先有插值，再有对象的更新
    def update_mobjects(self, dt: float) -> None:
        """
        更新 starting_mobject，以及 Transform 中的 target_mobject 的状态

        注意：通常情况下，处在动画进程中的 self.mobject 会停止更新（只处理动画），所以这个方法对它是没有用的

        Updates things like starting_mobject, and (for
        Transforms) target_mobject.  Note, since typically
        (always?) self.mobject will have its updating
        suspended during the animation, this will do
        nothing to self.mobject.
        """
        for mob in self.get_all_mobjects_to_update():
            mob.update(dt)

    def get_all_mobjects_to_update(self) -> list[Mobject]:
        # The surrounding scene typically handles
        # updating of self.mobject.  Besides, in
        # most cases its updating is suspended anyway
        return list(filter(
            lambda m: m is not self.mobject,
            self.get_all_mobjects()
        ))

    def copy(self):
        return deepcopy(self)

    def update_rate_info(
        self,
        run_time: float | None = None,
        rate_func: Callable[[float], float] | None = None,
        lag_ratio: float | None = None,
    ):
        self.run_time = run_time or self.run_time
        self.rate_func = rate_func or self.rate_func
        self.lag_ratio = lag_ratio or self.lag_ratio
        return self

    # Methods for interpolation, the mean of an Animation
    def interpolate(self, alpha: float) -> None:
        self.count += 1
        #log.info(f"animation interpolate {self.count}")
        self.interpolate_mobject(alpha)

    def update(self, alpha: float) -> None:
        """
        This method shouldn't exist, but it's here to
        keep many old scenes from breaking
        """
        self.interpolate(alpha)

    def interpolate_mobject(self, alpha: float) -> None:
        for i, mobs in enumerate(self.families):
            sub_alpha = self.get_sub_alpha(alpha, i, len(self.families))
            self.interpolate_submobject(*mobs, sub_alpha)

    def interpolate_submobject(
        self,
        submobject: Mobject,
        starting_submobject: Mobject,
        alpha: float
    ):
        # Typically ipmlemented by subclass
        pass

    def get_sub_alpha(
        self,
        alpha: float,
        index: int,
        num_submobjects: int
    ) -> float:
        # TODO, make this more understanable, and/or combine
        # its functionality with AnimationGroup's method
        # build_animations_with_timings
        lag_ratio = self.lag_ratio
        full_length = (num_submobjects - 1) * lag_ratio + 1
        value = alpha * full_length
        lower = index * lag_ratio
        raw_sub_alpha = clip((value - lower), 0, 1)
        return self.rate_func(raw_sub_alpha)

    # Getters and setters
    def set_run_time(self, run_time: float):
        self.run_time = run_time
        return self

    def get_run_time(self) -> float:
        if self.time_span:
            return max(self.run_time, self.time_span[1])
        return self.run_time

    def set_rate_func(self, rate_func: Callable[[float], float]):
        self.rate_func = rate_func
        return self

    def get_rate_func(self) -> Callable[[float], float]:
        return self.rate_func

    def set_name(self, name: str):
        self.name = name
        return self

    def is_remover(self) -> bool:
        return self.remover


def prepare_animation(anim: Animation | _AnimationBuilder):
    if isinstance(anim, _AnimationBuilder):
        return anim.build()

    if isinstance(anim, Animation):
        return anim

    raise TypeError(f"Object {anim} cannot be converted to an animation")
