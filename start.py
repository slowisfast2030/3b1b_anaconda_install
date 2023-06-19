from manimlib import *

"""
python -m manimlib start.py SquareToCircle -o --hd
or
manimgl start.py SquareToCircle -o --hd
or
python start.py (需要将下面的类实例化，并调用run方法)

客观评价下，manimgl没有manimce库细节做的好
"""
class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=1)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()

        self.play(ShowCreation(square))
        self.wait()
        self.play(ReplacementTransform(square, circle))
        self.wait()

# ins = SquareToCircle()
# ins.run()
# print('over')
"""
安装了两个manimgl环境
manimgl：初始化conda环境后，下载了manimgl的源码，执行python -m pip install -e .
manimgl_3b1b：初始化conda环境后，执行python -m pip install manimgl

manimgl环境下执行manim start.py SquareToCircle不会报错
manimgl_3b1b环境下执行manim start.py SquareToCircle会报错

vscode选中manimgl环境，变量不能跳转
vscode选中manimgl_3b1b环境，变量可以跳转

头疼。。。不能双全。。。

cd /opt/anaconda3/envs/manimgl/lib/python3.9/site-packages
可以发现没有manimlib文件夹，但是manimlib_3b1b环境下有这个文件夹
这可能就是两种安装方式的区别

====
终于找到了原因：
根源在于python -m pip install -e .
-e的意思是editable，即可编辑的，这种安装方式会在site-packages目录下创建一个egg-link文件，指向源码目录

下载的源码路径：/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim
"""