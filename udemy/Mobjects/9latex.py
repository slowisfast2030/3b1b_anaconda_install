from manimlib import *

class latex(Scene):
	def construct(self): 
		title = Text("Text, Latex")
		self.play(FadeIn(title))
		#self.wait(3)
		self.play(FadeOut(title))


		groceries = Text("Cheese, Tomatoes, Bread, Yeast").set_color(RED)
		self.add(groceries)
		#self.wait(1)
		self.remove(groceries)
		groceries2 = Text("""
			- Cheese
			- Lettuce
			- Tomatoes
			""")
		self.add(groceries2)
		#self.wait(1)
		self.remove(groceries2)


		equation = Tex(r"\begin{bmatrix} 1 & 2 & 3 \\ a & b & c \end{bmatrix}") 
		self.play(Write(equation))

		textintex = Tex(r"\text{This is Text in LaTeX}").shift(DOWN*3)
		self.add(textintex)






