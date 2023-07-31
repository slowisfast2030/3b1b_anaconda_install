from manimlib import *

class thenums(Scene):
	def construct(self): 
		title = Text("Numbers and Number Line")
		self.play(FadeIn(title))
		#self.wait(3)
		self.play(FadeOut(title))
		
		"""
		firstnum = DecimalNumber(3.3)
		self.play(FadeIn(firstnum))
		self.wait(2)
		firstnum.set_value(4.5)
		self.wait(2)
		firstnum.increment_value()
		self.wait(2)
		firstnum.increment_value(0.05)
		self.wait(2)
		

		secondnum = Integer(4).shift(DOWN*1)
		self.play(FadeIn(secondnum))
		self.wait(2)
		secondnum.set_value(1)
		self.wait(2)
		secondnum.increment_value()
		self.wait(2)
		secondnum.increment_value(0.4)
		secondnum.set_color(BLUE)
		self.wait(2)
		secondnum.increment_value(0.4)
		secondnum.set_color(RED)
		self.wait(2)
		secondnum.increment_value(0.4)
		secondnum.set_color(BLUE)
		self.wait(2)
		secondnum.increment_value(0.8)
		secondnum.set_color(BLUE)
		self.wait(2)
		secondnum.increment_value(0.8)
		secondnum.set_color(RED)
		self.wait(2)
		secondnum.increment_value(0.8)
		secondnum.set_color(BLUE)
		self.wait(2)
		"""

		nline = NumberLine().shift(UP*1).scale(0.6)
		self.play(FadeIn(nline))

		dot1 = Dot([1, 0, 0])
		self.play(FadeIn(dot1))

		posx = -3
		dot2 = Dot(nline.n2p(posx)).set_color(GREEN_SCREEN)
		self.play(FadeIn(dot2))

		"""
		#Rudimentary Animation (No Updaters or Generate Targets)
		for i in range(200):
			posx += 1/50
			self.remove(dot2)
			dot2 = Dot(nline.n2p(posx)).set_color(GREEN_SCREEN)
			self.add(dot2)
			self.wait(0.001)
		"""
		
		def addLabels(numberlinemobj, x_values=None, excluding=[]):
			if (x_values == None):
				x_values = numberlinemobj.get_tick_range()
			nlabels = []
			for i in x_values:
				if i not in excluding:
					nlabels.append(  Text(str(i)).shift(numberlinemobj.n2p(i)).shift(DOWN*0.3).scale(0.5)  )
			return Group(numberlinemobj, *nlabels)
		nline = addLabels(nline, [-5, -4, -3, -2, -1, 0, 1, 2, 3], [-2])
		self.play(FadeIn(nline))







