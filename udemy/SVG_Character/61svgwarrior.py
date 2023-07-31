from manimlib import *

#body #84D3DB
#head #A98E49
#else #8CD79F

class Warrior(SVGMobject):
	CONFIG = {
		"color": BLUE_E,
		"stroke_width": 0,
		"stroke_color": BLACK,
		"fill_opacity": 1.0,
		"height": 3,
		"arm_angle": -PI/6,
	}

	def __init__(self, mode="warrior", **kwargs):
		digest_config(self, kwargs)
		self.mode = mode
		self.parts_named = False
		svg_file = os.path.join(
				"/Users/syed-mohammadraza/ManimGLCourse/Tutorial3/svgs",
				f"{mode}.svg"
			)
		SVGMobject.__init__(self, file_name=svg_file, **kwargs)

	def name_parts(self):
		self.head = self.submobjects[0]
		self.body = self.submobjects[1]
		self.arm1 = self.submobjects[2]
		self.arm2 = self.submobjects[3]
		self.leg1 = self.submobjects[4]
		self.leg2 = self.submobjects[5]
		self.parts_named = True

	def init_colors(self):
		SVGMobject.init_colors(self)
		if not self.parts_named:
			self.name_parts()
		self.head.set_opacity(1).set_color(YELLOW)
		self.body.set_opacity(1).set_color(GREEN)
		self.arm1.set_opacity(1).set_color(ORANGE).rotate(self.arm_angle)
		self.arm2.set_opacity(1).set_color(PURPLE).rotate(PI/6)
		self.leg1.set_opacity(1).set_color(GREY).rotate(PI/2.2).shift(LEFT*0.5)
		self.leg2.set_opacity(1).set_color(WHITE).rotate(-PI/2.2).shift(RIGHT*0.5)
		return self



class svgwarrior(Scene):
	def construct(self): 
		title = Text("SVG Warrior")
		self.play(FadeIn(title))
		#self.wait(3)
		self.play(FadeOut(title))

		warbro = Warrior()
		plainbro = Warrior()
		self.add(warbro)
		self.wait(0.5)
		wave1bro = Warrior("wave1", arm_angle=-PI/6 + 1.5)
		wave2bro = Warrior("wave1", arm_angle=-PI/6 + 1.2)
		for i in range(4):
			self.play(Transform(warbro, wave1bro, run_time=0.1))
			self.play(Transform(warbro, wave2bro, run_time=0.1))
		self.play(Transform(warbro, plainbro))














