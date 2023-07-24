from __future__ import annotations

from manimlib.constants import BLACK, GREY_E
from manimlib.constants import FRAME_HEIGHT
from manimlib.mobject.geometry import Rectangle

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from manimlib.typing import ManimColor


class ScreenRectangle(Rectangle):
    def __init__(
        self,
        aspect_ratio: float = 16.0 / 9.0,
        height: float = 4,
        **kwargs
    ):
        super().__init__(
            width=aspect_ratio * height,
            height=height,
            **kwargs
        )

"""
这里涉及到对frame的深入理解
首先存在一个绝对空间，里面的所有Mobject都有绝对的尺寸
frame是对这个绝对空间的一个裁剪
假设，一个长方形的绝对尺寸是(8*16/9, 8)
一个frame的绝对尺寸恰好也是是(8*16/9, 8)
那么这个长方形就可以完全显示在frame中
尽管显示器有大有小，但我们看到的都是长方形完全显示在frame中

如果，将frame的绝对尺寸改为2*(8*16/9, 8)
视觉效果就是，长方形变小了
其实是frame变大了
"""
class FullScreenRectangle(ScreenRectangle):
    def __init__(
        self,
        height: float = FRAME_HEIGHT,
        fill_color: ManimColor = GREY_E,
        fill_opacity: float = 1,
        stroke_width: float = 0,
        **kwargs,
    ):
        super().__init__(
            height=height,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            stroke_width=stroke_width,
        )


class FullScreenFadeRectangle(FullScreenRectangle):
    def __init__(
        self,
        stroke_width: float = 0.0,
        fill_color: ManimColor = BLACK,
        fill_opacity: float = 0.7,
        **kwargs,
    ):
        super().__init__(
            stroke_width=stroke_width,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
        )
