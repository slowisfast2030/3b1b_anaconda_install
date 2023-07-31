import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *

class updatering(Scene):
	def construct(self): 
		text = Text("Updating II: Updaters")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Updating II: Updaters").shift(UP*3.5).scale(0.6)
		self.play(FadeIn(title))

		obj1 = Text("This is text").shift(LEFT*4)
		obj2 = Square(fill_opacity=1).set_color(BLUE)
		obj3 = Circle(fill_opacity=1).set_color(YELLOW).shift(UP*2)
		obj4 = Rectangle(fill_opacity=1).set_color(GREEN).shift(DOWN*1)

		x = 0
		def moveSquare(mob):
			
			mob.become( Square(fill_opacity=1).set_color(BLUE).shift(LEFT*x) )
			# 如果是下面的代码，会发现不会出现obj2，一开始就是一个蓝色的圆，缓慢移动
			# 不是代码有bug，可以从updater的原理角度分析
			# 一开始确实是obj2，不过很快就被mob.become()覆盖了
			# 这里还可以进一步看到，整个updater的效果只模拟了位移的渐变，并没有模拟形状和颜色的渐变
			# 和transform类还是有本质差距
			# 如果想通过become模拟transform的效果，也不是不可以
			# 可以写多个become，每个become都是一个transform
			#mob.become( Circle(fill_opacity=1).set_color(BLUE).shift(LEFT*x) )
		
		# 一旦添加了updater，就相当于被包含进了while循环
		# 每间隔一个帧时间执行一次，直到整个代码结束
		obj2.add_updater(moveSquare)
		self.add(obj2)

		while x < 3:
			x += 0.01
			# wait就是保持上一个frame的状态0.001s
			self.wait(0.001)

		# 和tracker.py的代码对比起来，很有启发