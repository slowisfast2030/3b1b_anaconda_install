from manimlib import *

class cube(Scene):
    def construct(self):
        c = Cube(color=BLUE)
        self.add(c)
        self.wait(1)

        frame = self.camera.frame
        frame.generate_target()
        frame.target.set_euler_angles(
			theta = -10*DEGREES,
			phi = 50 *DEGREES
		)
        self.play(MoveToTarget(frame))
        def rotCam(s):
            s.increment_theta(-0.005)
        frame.add_updater(rotCam)

        self.wait(5)
