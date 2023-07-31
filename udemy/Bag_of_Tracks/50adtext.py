from manimlib import *
import numpy as np
import random

class adtext(Scene):
	def construct(self): 
		text = Text("Advanced Text and Tex")
		self.play(FadeIn(text))
		#self.wait(3)
		self.play(FadeOut(text))

		title = Text("Advanced Text and Tex").shift(UP*3.5)#.scale(0.6)
		self.play(FadeIn(title))

		text = Text(
			"""
			Using t2c you can change color, using t2s you can change\n
			slant, using t2w you can change weight and you can even\n
			pick out which words!\n
			Using font you can change font but it changes every word.
			""",
			# t2c is a dict that you can choose color for different text
			t2c={"color": BLUE, "slant": BLUE, "weight": BLUE,"t2c":RED, "t2s":RED, "t2w":RED, "font":GREEN, },
			t2s={"slant": ITALIC},#ITALIC, NORMAL, OBLIQUE
			t2w={"weight": BOLD}, #BOLD, NORMAL
			font="Computer Modern", font_size=30,
		)
		self.play(FadeIn(text, UP))
		#self.wait(30)
		self.play(FadeOut(text, UP))

		
		y_tex = "\\textbf{y}"
		x_tex = r"\underline{x}"
		kw = {"color":WHITE}

		lines = Group(
			Tex(y_tex, "=", "m", x_tex, " + ", "b", **kw),
			Tex(y_tex, " - ", "b" "=", "m", x_tex, **kw),
			Tex("(", y_tex, " - ", "b", ")", "/", "m", "=", x_tex, **kw),
			Tex(x_tex, "=", "(", y_tex, " - ", "b", ")", "/", "m", **kw),
		)

		lines.arrange(DOWN, buff=0.7)
		for line in lines:
			tm = -line.get_part_by_tex("=").get_center()
			line.shift(tm[0] * RIGHT)
			line.set_color_by_tex_to_color_map({
				y_tex: BLUE,
				x_tex: RED,
				"m": GREEN,
			})
		self.play(FadeIn(lines[0], DOWN))
		self.play(TransformMatchingTex(lines[0], lines[1]))
		self.play(TransformMatchingTex(lines[1], lines[2]))
		self.play(TransformMatchingTex(lines[2], lines[3]))
		
		#self.wait(30)
		
		self.play(FadeOut(lines))
		




		
		source = Text("this is 1 line", height=1)
		target = Text("nice target line 2", height=1)
		kw = {"run_time": 3, "path_arc": PI / 2}

		self.play(Write(source))
		self.play(TransformMatchingShapes(source, target, **kw))
		self.wait(1)
		self.play(TransformMatchingShapes(target, source, **kw))
		




