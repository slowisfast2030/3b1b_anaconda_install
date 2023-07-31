from manimlib import *


class Friend(SVGMobject):
	CONFIG = {
		"color": BLUE_E,
		"stroke_width": 0,
		"stroke_color": BLACK,
		"fill_opacity": 1.0,
		"height": 3,
		"arm_angle": -PI/6,
	}

	def __init__(self, mode="freind", **kwargs):
		digest_config(self, kwargs)
		self.mode = mode
		self.parts_named = False
		svg_file = os.path.join(
				"/Users/syed-mohammadraza/ManimGLCourse/Tutorial3/svgs",
				f"{mode}.svg"
			)
		SVGMobject.__init__(self, file_name=svg_file, **kwargs)

	def name_parts(self):
		print(len(self.submobjects))
		self.parts_named = True

	def init_colors(self):
		SVGMobject.init_colors(self)
		number_of_parts = len(self.submobjects)
		colorsbro = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_parts)]
		for i in range(number_of_parts):
			self.submobjects[i].set_opacity(1).set_color(colorsbro[i])
		return self



class svgwarrior(Scene):
	def construct(self): 
		title = Text("SVG Freind")
		self.play(FadeIn(title))
		#self.wait(3)
		self.play(FadeOut(title))

		friendbro = Friend("friend")
		plainbro = Friend("shield")
		self.add(friendbro)
		self.wait(0.5)
		self.play(Transform(friendbro, plainbro))











