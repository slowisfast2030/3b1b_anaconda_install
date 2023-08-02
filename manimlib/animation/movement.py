from __future__ import annotations

from manimlib.animation.animation import Animation
from manimlib.utils.rate_functions import linear

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Sequence

    import numpy as np

    from manimlib.mobject.mobject import Mobject


"""
test_homotopy1 = lambda x, y, z, t: (
			x + interpolate(-3, 3, 2*t if t<=0.5 else 1), #First 5 Seconds
			y + interpolate(0, 3, 2*(t-0.5) if t>0.5 else 0), #Next 5 Seconds
			z)

test_homotopy2 = lambda x, y, z, t: (
			x + interpolate(-3, 3, 4*t if t<=0.25 else 1) 
				+ interpolate(3, -3, 4*(t-0.5) if (t>=0.5 and t<=0.75) else (0 if t<=0.5 else 1)), 
			y + interpolate(-3, 3, 4*(t-0.25) if (t>0.25 and t<0.5) else (0 if t<=0.25 else 1)) 
				+ interpolate(3, -3, 4*(t-0.75) if (t>0.75) else (0 if t<=0.75 else 1)), 
			z)

self.play(Homotopy(test_homotopy1, obj2, run_time=10, rate_func=linear))
"""
class Homotopy(Animation):
    apply_function_config: dict = dict()

    def __init__(
        self,
        homotopy: Callable[[float, float, float, float], Sequence[float]],
        mobject: Mobject,
        run_time: float = 3.0,
        **kwargs
    ):
        """
        Homotopy is a function from
        (x, y, z, t) to (x', y', z')
        """
        """
        homotopy 是一个从 (x, y, z, t) 到 (x', y', z') 的函数。
        t 的取值范围是 [0, 1]，
        让 mobject 根据 homotopy 计算的每个点坐标进行变换。
        例子中 t = 0 时 mob 是边长为 0 的正方形，
        t = 1 时是边长为 2 的正方形。
        与 Transform 类似，区别在于 Transform 锚点运动轨迹是直线，
        Homotopy 锚点运动轨迹是根据传入的 homotopy 计算的。
        """
        self.homotopy = homotopy
        super().__init__(mobject, run_time=run_time, **kwargs)

    def function_at_time_t(self, t: float) -> Callable[[np.ndarray], Sequence[float]]:
        def result(p):
            return self.homotopy(*p, t)
        return result

    def interpolate_submobject(
        self,
        submob: Mobject,
        start: Mobject,
        alpha: float
    ) -> None:
        submob.match_points(start)
        submob.apply_function(
            self.function_at_time_t(alpha),
            **self.apply_function_config
        )


class SmoothedVectorizedHomotopy(Homotopy):
    apply_function_config: dict = dict(make_smooth=True)


class ComplexHomotopy(Homotopy):
    def __init__(
        self,
        complex_homotopy: Callable[[complex, float], complex],
        mobject: Mobject,
        **kwargs
    ):
        """
        Given a function form (z, t) -> w, where z and w
        are complex numbers and t is time, this animates
        the state over time
        """
        def homotopy(x, y, z, t):
            c = complex_homotopy(complex(x, y), t)
            return (c.real, c.imag, z)

        super().__init__(homotopy, mobject, **kwargs)


class PhaseFlow(Animation):
    def __init__(
        self,
        function: Callable[[np.ndarray], np.ndarray],
        mobject: Mobject,
        virtual_time: float | None = None,
        suspend_mobject_updating: bool = False,
        rate_func: Callable[[float], float] = linear,
        run_time: float =3.0,
        **kwargs
    ):
        self.function = function
        self.virtual_time = virtual_time or run_time
        super().__init__(
            mobject,
            rate_func=rate_func,
            run_time=run_time,
            suspend_mobject_updating=suspend_mobject_updating,
            **kwargs
        )

    def interpolate_mobject(self, alpha: float) -> None:
        if hasattr(self, "last_alpha"):
            dt = self.virtual_time * (alpha - self.last_alpha)
            self.mobject.apply_function(
                lambda p: p + dt * self.function(p)
            )
        self.last_alpha = alpha


class MoveAlongPath(Animation):
    def __init__(
        self,
        mobject: Mobject,
        path: Mobject,
        suspend_mobject_updating: bool = False,
        **kwargs
    ):
        self.path = path
        super().__init__(mobject, suspend_mobject_updating=suspend_mobject_updating, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        point = self.path.point_from_proportion(alpha)
        self.mobject.move_to(point)
