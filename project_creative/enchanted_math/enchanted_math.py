from manimlib import *
bpm = 95
note_time = 10/bpm

class Color_Change(Animation):
    CONFIG = {
        "suspend_mobject_updating": False,
        "int_func": np.round,
    }

    def __init__(self, group, color1, color2, **kwargs):
        self.all_submobjects = list(group.submobjects)
        self.color1 = color1
        self.color2 = color2
        super().__init__(group, **kwargs)

    def interpolate_mobject(self, alpha):
        n_submobs = len(self.all_submobjects)
        index = int(self.int_func(alpha * n_submobs))
        self.update_submobject_list(index)

    def update_submobject_list(self, index):
        self.mobject.set_submobjects(self.all_submobjects[:index])
        self.mobject.set_color(self.color1)
        for i in np.arange(np.maximum(-5,-len(self.mobject.submobjects)),0):
            self.mobject.submobjects[i].set_color(interpolate_color(self.color1, self.color2, (i+6)/5))

class Stretch(Transform):
    CONFIG = {
        "lag_ratio": DEFAULT_FADE_LAG_RATIO,
    }

    def __init__(self, mobject, **kwargs):
        super().__init__(mobject, **kwargs)
    
    def create_target(self):
        return self.mobject

    def create_starting_mobject(self):
        start = super().create_starting_mobject()
        start.stretch(0,0)
        return start

def lagrange_interpolation(points):
    n = len(points)
    def lagrange_basis(i, x):
        result = 1
        for j in range(n):
            if j == i:
                continue
            result *= (x - points[j][0]) / (points[i][0] - points[j][0])
        return result
    def lagrange_polynomial(x):
        result = 0
        for i in range(n):
            result += points[i][1] * lagrange_basis(i, x)
        return result
    return lagrange_polynomial

    

class Countable_infinity(Scene):
    def construct(self):
        self.add_sound("enchanted_love")

        def shaking_path(x): return np.array(
            [np.cos(10*x), np.sin(9*x), 0])
        frame = self.camera.frame
        frame.scale(2)
        #frame.add_updater(lambda obj:obj.move_to(shaking_path(self.time)))
        # self.add(frame)
        numlist = VGroup(*[Tex(str(i)).move_to(RIGHT*(i+1)*1.5)
                         for i in np.arange(30)])
        numlist2 = VGroup(*[Tex(str(i)).move_to(DOWN*(i+1)*1.5)
                          for i in np.arange(30)])
        numlist3 = VGroup(*[Tex(str(i)).set_opacity((i+1) %
                          2).move_to(np.array([i+1, -1, 0])*1.5) for i in np.arange(30)])
        numlist4_pre = VGroup(*[Tex(str(i)).set_opacity((i+1) %
                              2).move_to(np.array([i+1, -1, 0])*1.5) for i in np.arange(60)])
        numlist4 = VGroup(
            *[Tex(str(i*2)).move_to(np.array([i+1, -1, 0])*1.5) for i in np.arange(30)])
        for i in [*numlist, *numlist2]:
            i.save_state()
        numlist.save_state()
        numlist2.save_state()

        self.add(frame)
        frame.add_updater(lambda obj: obj.move_to(VGroup(*self.mobjects[1:])))
        self.wait(note_time)
        for i in range(4):
            self.add(numlist[i*5])
            self.wait(note_time)
            self.play(ShowIncreasingSubsets(
                numlist[i*5+1:(i+1)*5]), run_time=note_time*4)
            self.wait(note_time*6.05)
            if i == 2:
                frame.clear_updaters()
        self.add(numlist[20:])
        for j in range(4):
            self.play(frame.animate.shift(DOWN*1.25), run_time=note_time*5)
            if j == 3:
                self.play(frame.animate.shift(DOWN*1.25), run_time=note_time*5)
                self.wait(note_time*3)
            else:
                self.wait(note_time*7)

        self.play(TransformFromCopy(numlist, numlist3), run_time=note_time*5)
        self.wait(note_time*6)
        self.remove(numlist3)
        self.add(numlist4_pre)
        self.play(TransformMatchingShapes(numlist4_pre[::2], numlist4))
        frame.save_state()
        self.wait(note_time*5.45)
        relationship1 = VGroup(
            *[Arrow(i.get_center(), j.get_center()) for i, j in zip(numlist, numlist4)]).set_color(YELLOW_B)

        # self.wait(note_time*2)
        for i in range(4):
            self.add(relationship1[i*5])
            self.wait(note_time)
            self.play(ShowIncreasingSubsets(
                relationship1[i*5+1:(i+1)*5]), run_time=note_time*4)
            self.wait(note_time*6.1)

        self.wait(note_time*22)
        big_notation = Tex("\mathrm{card}~", "\mathds{N}", "=",
                           "\mathrm{card}~", "2\mathds{N}").move_to(frame).scale(4)

        # self.wait(note_time*5)

        self.play(ShowIncreasingSubsets(big_notation), run_time=5*note_time)
        self.remove(big_notation, relationship1, numlist4)
        back = Rectangle(width=200, height=200, color=WHITE, fill_opacity=1)
        self.add(back, numlist)
        numlist.set_color(BLACK)
        numlist2.set_color(BLACK)
        self.play(ReplacementTransform(numlist.copy(), numlist2,
                  path_arc=-PI/2), run_time=5*note_time)
        self.add(numlist2)
        self.wait(note_time*5)

        grid_of_fractions = VGroup(*[VGroup(*[Tex("{", str(j), "\\over ", str(i-j), "}").move_to(np.array(
            [numlist[j].get_x(), numlist2[i-j].get_y(), 0])).set_color(BLACK) for j in range(i+1)]) for i in range(30)])

        def form_grid(i):
            start = VGroup(*[VGroup(numlist[m], numlist2[i-m])
                           for m in range(i+1)])
            end = grid_of_fractions[i]
            if i != 29:
                return AnimationGroup(*[TransformMatchingShapes(k.copy(), j, path_arc=PI/2) for k, j in zip(start, end)], run_time=note_time*5)
            else:
                return AnimationGroup(*[TransformMatchingShapes(k, j, path_arc=PI/2) for k, j in zip(start, end)], run_time=note_time*5)

        for i in range(6):
            self.play(form_grid(i), rate_func=exponential_decay)
            self.wait(note_time*6.5)
        self.wait(note_time*13)
        self.play(LaggedStart(*[form_grid(i) for i in range(6,30)],lag_ratio=0.1),run_time=note_time*85)
        #self.wait(note_time*85)
        #self.add(grid_of_fractions[6:])
        self.remove(numlist, numlist2)
        frame.shift(-grid_of_fractions[0].get_center())
        frame_center = np.array([12.06236942, -6.25, 0.])-grid_of_fractions[0].get_center()
        grid_of_fractions.shift(-grid_of_fractions[0].get_center())

        def update(obj, alpha):
            obj.move_to(frame_center+0.2*np.array(
                [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]))
        self.play(*[i.animate.shift(random.uniform(0, 5)*OUT) for k in grid_of_fractions for i in k],
                  rate_func=bezier([0, 0, 0, 1, 1, 1, 1, 1, 0]), run_time=11*note_time)
        self.play(UpdateFromAlphaFunc(frame, update), run_time=note_time)
        frame.move_to(frame_center)
        centers = []
        for i,f in enumerate(grid_of_fractions):
            if i%2 == 0:
                centers+=[m.get_center() for m in f]
            else:
                centers+=reversed([m.get_center() for m in f])


        UR_arrows = VGroup(*[VGroup(*[Arrow(p.get_center(), q.get_center()).set_color(YELLOW)
                           for p, q in zip(i[:-1], i[1:])]) for i in grid_of_fractions[1::2]])
        DL_arrows = VGroup(*[VGroup(*[Arrow(p.get_center(), q.get_center()).set_color(YELLOW)
                           for q, p in zip(i[:-1], i[1:])]) for i in grid_of_fractions[2::2]])
        D_arrows = VGroup(*[Arrow(p[0].get_center(), q[0].get_center()).set_color(YELLOW)
                          for p, q in zip(grid_of_fractions[::2], grid_of_fractions[1::2])])
        R_arrows = VGroup(*[Arrow(p[-1].get_center(), q[-1].get_center()).set_color(YELLOW)
                          for p, q in zip(grid_of_fractions[1::2], grid_of_fractions[2::2])])
        around_circ1 = Circle().flip().next_to(frame_center, buff=0)
        around_circ2 = Circle().next_to(frame_center, LEFT, buff=0)
        self.play(*[GrowArrow(i) for k in UR_arrows for i in k],
                  frame.animate.shift(UR*2), run_time=5*note_time)
        self.play(frame.animate.move_to(frame_center),
                  UR_arrows.animate.set_color("#03C497"), run_time=5*note_time)
        self.play(*[GrowArrow(i) for k in DL_arrows for i in k],
                  frame.animate.shift(DL*2), run_time=5*note_time)
        self.play(frame.animate.move_to(frame_center),
                  DL_arrows.animate.set_color("#03C497"), run_time=5*note_time)
        self.wait(6*note_time)
        self.play(MoveAlongPath(frame, around_circ1), run_time=6*note_time)
        self.wait(6*note_time)
        self.play(*[GrowArrow(i) for i in D_arrows],
                  frame.animate.shift(DOWN*2), run_time=3*note_time)
        self.play(frame.animate.move_to(frame_center),
                  D_arrows.animate.set_color("#03C497"), run_time=3*note_time)
        self.wait(6*note_time)
        self.play(MoveAlongPath(frame, around_circ2), run_time=6*note_time)
        self.wait(6*note_time)
        self.play(*[GrowArrow(i) for i in R_arrows],
                  frame.animate.shift(RIGHT*2), run_time=3*note_time)
        self.play(frame.animate.move_to(frame_center),
                  R_arrows.animate.set_color("#03C497"), run_time=3*note_time)

        swing_path = Arc(-150*DEGREES,120*DEGREES).next_to(frame_center,UP,buff=0)
        def swing(obj,alpha):
            obj.move_to(swing_path.pfp(np.sin(3*PI*alpha)*0.5+0.5)-OUT*np.sin(3*PI*alpha)**2)

        self.play(UpdateFromAlphaFunc(frame,swing),run_time=30*note_time)

        def get_frac(i, j):
            return (j, i-j)

        def modified_Cross(mobject):
            a = Circle().set_fill(TEAL_A,1).set_stroke("#03C497")
            return a.move_to(mobject)

        Crosses = VGroup()
        slope_list = []
        index_list = []
        for i in np.arange(0, 30):
            for j in np.arange(i+1):
                x, y = get_frac(i, j)
                f = np.gcd(x, y)
                if (x, y) == (0, 0):
                    Crosses.add(modified_Cross(grid_of_fractions[i][j]).scale(.6))
                    slope_list.append((1, 1))
                    index_list.append((i, j))
                elif y == 0:
                    Crosses.add(modified_Cross(grid_of_fractions[i][j]).scale(.6))
                    slope_list.append((x/f, y/f))
                    index_list.append((i, j))
                elif x == 0 and y > 1:
                    Crosses.add(modified_Cross(grid_of_fractions[i][j]).scale(.6))
                    slope_list.append((x/f, y/f))
                    index_list.append((i, j))
                elif np.gcd(x, y) > 1:
                    Crosses.add(modified_Cross(grid_of_fractions[i][j]).scale(.6))
                    slope_list.append((x/f, y/f))
                    index_list.append((i, j))
        


        lines = VGroup(*[Line(5*np.array([-i,j,0])/(i*i+j*j)**.5,60*np.array([-i,j,0])/(i*i+j*j)**.5) for i, j in slope_list]).set_color("#00A795")
        lines_tag = VGroup(*[Line(-30*np.array([-i,j,0])/(i*i+j*j)**.5,ORIGIN) for i, j in slope_list]).set_color("#00A795")

        self.play(frame.animate.move_to(-frame_center),run_time=12*note_time)
        self.play(
            ApplyMethod(frame.move_to,frame_center+shaking_path(self.time),run_time=12*note_time,rate_func=lambda t:1-exponential_decay(1-t))
        )
        shaking_path_factor = ValueTracker(0.5)
        frame.add_updater(lambda m: m.move_to(frame_center+shaking_path(self.time)*shaking_path_factor.get_value()))
        self.play(
            LaggedStart(*[Transform(i,j) for i,j in zip(lines,lines_tag)],lag_ratio=.01,run_time=54*note_time)
        )
        self.play(shaking_path_factor.animate.set_value(0.2),run_time=18*note_time)
        self.play(
            LaggedStart(*[ReplacementTransform(i,j) for i,j in zip(lines,Crosses)],lag_ratio=.01,run_time=30*note_time))
        labeled_num = VGroup()
        back_recs = VGroup()
        fracs = VGroup()
        k=0

        def back_rec(mob):
            return Rectangle(mob.get_width()+0.1,mob.get_height()+0.1).move_to(mob)

        for i in np.arange(0, 30):
            if i%2==1:
                for j in np.arange(i+1):
                    if not( (i,j) in index_list):
                        labeled_num.add(Integer(k).set_color(YELLOW_B).next_to(grid_of_fractions[i][j],UR,buff=0))
                        back_recs.add(back_rec((VGroup(grid_of_fractions[i][j],labeled_num[k]))).set_fill(RED,0.5).set_stroke(RED,5))
                        fracs.add(grid_of_fractions[i][j])
                        k+=1
            elif i%2==0:
                for j in np.arange(i,-1,-1):
                    if not( (i,j) in index_list):
                        labeled_num.add(Integer(k).set_color(YELLOW_B).next_to(grid_of_fractions[i][j],UR,buff=0))
                        back_recs.add(back_rec((VGroup(grid_of_fractions[i][j],labeled_num[k]))).set_fill(RED,0.5).set_stroke(RED,5))
                        fracs.add(grid_of_fractions[i][j])
                        k+=1
        #self.play(frame.animate.move_to(ORIGIN).scale(0.5),run_time=3*note_time)
        self.play(ShowIncreasingSubsets(back_recs),Color_Change(labeled_num,YELLOW_B,BLACK),run_time=54*note_time,rate_func=linear)
        formula2 = Tex("\mathrm{card}~\mathds{N}", "=","\mathrm{card}~\mathds{Q}").move_to(frame).scale(4).set_color(BLACK)
        self.wait(2*note_time)
        formula2.add_updater(lambda m: m.move_to(frame)).set_opacity(0)
        self.add(formula2)
        for i in range(3):
            formula2[i].set_opacity(1)
            self.wait(2*note_time)
        self.wait(4*note_time)
        self.remove(*self.get_mobjects())
        self.add(frame)
        realindex = VGroup(*[Tex(str(i)).move_to(DOWN*i)
                          for i in np.arange(30)])
        def rand_str():
            rand="0."
            for i in range(100):
                rand+=str(random.randint(0,9))
            return rand
        rand_str_list = [rand_str() for i in range(100)]
        final_per_str = "0."
        for i in range(100):
            final_per_str += rand_str_list[i][i+2]
        final_str = "0."
        for k in final_per_str[2:]:
            if int(k)<9:
                final_str += str(int(k)+1)
            else:
                final_str += "0"
        
        reallist = VGroup(*[Tex(*list(rand_str_list[i])).next_to(DOWN*i,RIGHT,buff=1) for i in range(100)])
        self.add(realindex[0])
        self.wait(note_time*6)
        self.play(ShowIncreasingSubsets(realindex[1:10]),run_time=9*note_time)
        self.play(Write(realindex[10:],run_time=30*note_time),Write(reallist[:14],lag_ratio=1,run_time=24*note_time))
        self.add(reallist[14:])
        digit_circle = VGroup(*[Circle(arc_center=reallist[i][2+i].get_center(),radius=0.3).set_fill(YELLOW_B,0.5).set_stroke(YELLOW_B,6) for i in range(100)])
        
        frame_path = bezier([
            frame_center,
            digit_circle[0].get_center(),
            digit_circle[0].get_center(),
            digit_circle[1].get_center(),
            digit_circle[-6].get_center(),
            digit_circle[-5].get_center(),
            digit_circle[-5].get_center(),
            frame_center])
        scale_fractor = bezier([1,0.2,0.2,0.2,0.2,0.2,0.2,0.2,1])
        frame.save_state()
        def round_trip(obj,alpha):
            obj.restore()
            obj.scale(scale_fractor(alpha)).move_to(frame_path(alpha))
        self.play(ShowCreation(digit_circle[:14]),shaking_path_factor.animate.set_value(0),run_time=28*note_time,rate_func=linear)
        self.add(digit_circle[14:])
        frame.clear_updaters()
        final_per_tex = Tex(*list(final_per_str)).next_to(UP,RIGHT,buff=1)
        final_tex = Tex(*list(final_str)).next_to(UP*2,RIGHT,buff=1)
        relationship2 = VGroup(*[Arrow(reallist[i][i+2].get_center(),final_per_tex[i+2].get_center(),buff=0.3) for i in range(100)]).set_color(YELLOW_B)
        self.play(UpdateFromAlphaFunc(frame,round_trip),LaggedStart(*[ReplacementTransform(reallist[i][i+2].copy(),final_per_tex[i+2]) for i in range(100)]),
            LaggedStart(*[GrowArrow(relationship2[i]) for i in range(100)]),
            Write(final_per_tex[:2]),run_time=80*note_time)
        #self.play(FadeIn(final_tex[2:],shift=DOWN,lag_ratio=.05),FadeOut(final_per_tex[2:],shift=DOWN,lag_ratio=.05),run_time=10*note_time)
        relationship3 = VGroup(*[Arrow(final_per_tex[i+2].get_center(),final_tex[i+2].get_center()) for i in range(100)]).set_color(YELLOW_B)
        
        Crosses2 = VGroup(*[VGroup(Line(UR,DL),Line(UL,DR)).set_stroke(width=5).scale(0.1).move_to(i) for i in relationship3]).set_color(RED)
        frame.add_updater(lambda m: m.move_to(frame_center+shaking_path(self.time)*shaking_path_factor.get_value()))
        self.play(shaking_path_factor.animate.set_value(0.1),run_time=6*note_time)
        self.play(
            LaggedStart(*[ReplacementTransform(i.copy(),j) for i,j in zip(final_per_tex,final_tex)],lag_ratio=.1),
            LaggedStart(*[GrowArrow(relationship3[i]) for i in range(100)],lag_ratio=.1),
            LaggedStart(*[ShowCreation(c) for c in Crosses2],lag_ratio=.1),
            FadeOut(relationship2,lag_ratio=0.1),
            run_time=40*note_time
        )
        relationship4 = VGroup(*[Arrow(final_tex[i+2].get_center(),reallist[i][i+2].get_center(),buff=0.3) for i in range(100)]).set_color(YELLOW_B)
        self.wait(6*note_time)
        Crosses3 = VGroup(*[VGroup(Line(UR,DL),Line(UL,DR)).set_stroke(width=5).scale(0.1).move_to(i) for i in relationship4]).set_color(RED)

        self.play(
            LaggedStart(*[ReplacementTransform(i,j,path_arc=-PI) for i,j in zip(relationship3,relationship4)]),
            LaggedStart(*[ReplacementTransform(i,j,path_arc=-PI) for i,j in zip(Crosses2,Crosses3)]),
            run_time=40*note_time
        )
        self.wait(6*note_time)
        self.play(FadeOut(final_per_tex),run_time=6*note_time)
        full_rec = back_rec(reallist).set_stroke(RED,5).set_fill(RED,0.5)
        full_arrow = Arrow(final_tex.get_bottom(),full_rec.get_top(),buff=0.1).set_color(YELLOW_B)
        full_cross = VGroup(Line(UR,DL),Line(UL,DR)).set_stroke(RED,width=5).scale(0.1).move_to(full_arrow)
        self.bring_to_back(full_rec)
        self.play(
            FadeIn(full_rec),
            FadeOut(digit_circle),
            *[ReplacementTransform(i,full_arrow) for i in relationship4],
            *[ReplacementTransform(i,full_cross) for i in Crosses3],
            run_time=40*note_time
        )
        self.wait(6*note_time)
        formula3 = Tex("\mathrm{card}~","\mathds{N}","<","\mathrm{card}","~\mathds{R}").scale(2).fix_in_frame()
        self.play(Write(formula3),run_time=12*note_time)

        back.set_color(BLACK)
        self.add(back,formula3)
        self.play(FadeIn(back),formula3.animate.set_opacity(1),run_time=6*note_time)
        frame.clear_updaters().move_to(ORIGIN).scale(0.5)
        
        n = 50

        stair_corners = [np.array([20,-8,0]),np.array([20,-3,0])]
        jumping_corners = [np.array([4,-3,0])+i*np.array([-2,1,0]) for i in np.arange(int(n/2))]

        for i in range(n):
            if i == 0:
                stair_corners.append(np.array([5,-3,0]))
            elif i % 2 == 1:
                stair_corners.append(stair_corners[i+1]+LEFT*2)
            else:
                stair_corners.append(stair_corners[i+1]+UP)
        stair_corners.append(stair_corners[-1]+LEFT*50)
        jumping_corners += [jumping_corners[-1]+LEFT*i for i in np.arange(2,9,2)]
        
        def jumping_path(alpha):
            if alpha == 1:
                return jumping_corners[-1][1]
            else:
                path_index = int(np.floor(alpha*(len(jumping_corners)-1)))
                path_x = jumping_corners[0][0]*(1-alpha)+jumping_corners[-1][0]*alpha
                path_polynomial = lagrange_interpolation([jumping_corners[path_index],jumping_corners[path_index+1],jumping_corners[path_index+1]+UR])

                return np.array([path_x,path_polynomial(path_x)+0.3,0])
        
        def window():
            return VGroup(*[Square(side_length=1.9).set_fill(YELLOW_B,1).set_stroke(width=0) for _ in range(4)]).arrange_in_grid(2,2,buff=0.2)
        windows = VGroup()
        for i in np.arange(int(n/2)):
            if i% 20 == 9:
                windows.add(window().next_to(jumping_corners[i],UP,buff=3))

        def light():
            return Polygon(LEFT*2,RIGHT*2,RIGHT*4+DOWN*20,LEFT*4+DOWN*20).set_stroke(width=0).set_fill(YELLOW_B,.5)

        windows_light = VGroup(*[light().next_to(i.get_top(),DOWN,buff=0) for i in windows])
        self.add(windows_light,windows)
        
        stair = Polygon(*stair_corners,np.array([stair_corners[-1][0],stair_corners[0][1],0])).set_stroke(width=5).set_fill(BLACK,.9)
        
        final_square1 = Square(1.5).set_fill(BLACK,1).set_stroke(WHITE).move_to(jumping_corners[-1]+np.array([-2,0.75,0]))
        final_square2 = Square(1.5).set_fill(BLACK,1).set_stroke(WHITE).move_to(jumping_corners[-1]+np.array([-2,2.25,0]))
        final_square3 = Square(1.5).set_fill(BLACK,1).set_stroke(WHITE).move_to(jumping_corners[-1]+np.array([-2,2.25,0]))
        final_light = VGroup(
            Rectangle(width=3,height=30).set_stroke(width=0).set_fill("#00A795",1),
            Rectangle(width=3,height=30).set_stroke(width=0).set_fill("#05668D",1),
            Rectangle(width=2,height=30).set_stroke(width=0).set_fill("#00A795",1)
        ).next_to(final_square1.get_bottom(),UP,buff=0)

        R = Tex("\mathds{R}").move_to(jumping_corners[0]+0.3*UP)
        N = Tex("\mathds{N}").move_to(final_square1)

        def interpolate_between(p1,p2,num):
            return [p1*(1-alpha)+p2*alpha for alpha in np.linspace(0,1,num)]

        frame_path = Elbow().set_points_as_corners([*interpolate_between(ORIGIN,jumping_corners[len(jumping_corners)-6]+UP*3,6),final_square3.get_center()+UP*.75])
        self.add(final_square1,final_square2,N)
        self.play(
            FadeOut(formula3[0:4]),
            ReplacementTransform(formula3[4],R[0]),
            FadeIn(stair),
            run_time=6*note_time)
        self.play(
            UpdateFromAlphaFunc(R,lambda m,alpha: m.move_to(jumping_path(alpha))),
            MoveAlongPath(self.camera.frame,frame_path),
            run_time=20,rate_func=linear)
        R.move_to(jumping_corners[-1]+0.3*UP)
        final_jump = lagrange_interpolation([jumping_corners[-1]+UP*0.3,jumping_corners[-1]+np.array([-1,2.25,0]),jumping_corners[-1]+np.array([-2,2.25,0])])
        final_path = FunctionGraph(final_jump,x_range=[jumping_corners[-1][0]-2,jumping_corners[-1][0],0.001]).reverse_points()
        self.add(final_light,*final_light,stair,final_square1,final_square2,final_square3,N,R)
        self.play(
            Stretch(final_light,lag_ratio=0.1),
            MoveAlongPath(R,final_path,rate_func=linear),
            run_time=6*note_time)
        
        R.move_to(final_square3)
        self.wait(6*note_time)
        ques_mark = Tex("?").move_to(final_square2)
        self.add(final_square2,ques_mark,final_square3,R)
        self.play(final_square3.animate.shift(UP*1.5),R.animate.shift(UP*1.5),Write(ques_mark),run_time=6*note_time)





class Thumbnail_enchanted(Scene):
    def construct(self):

        
        ground = Line(np.array([-3,-3,0]),np.array([3,-3,0]))
        final_light = VGroup(
            Rectangle(width=4,height=30).set_stroke(width=0).set_fill("#05668D",1),
            Rectangle(width=3,height=30).set_stroke(width=0).set_fill("#00A795",1)
        ).next_to(ground,UP,buff=0)
        box = Square(side_length=1.4).set_fill(BLACK,1).set_stroke(WHITE).move_to(np.array([0,0.75,0]))
        boxes = VGroup(*[box.copy() for i in range(2)])
        boxes[0].rotate(20*DEGREES)
        boxes[1].rotate(-20*DEGREES)
        boxes.arrange(UP,buff=0).next_to(ground,UP,buff=0)
        N = Tex("\mathds{N}").scale(2).move_to(boxes[0]).rotate(20*DEGREES)
        R = Tex("\mathds{R}").scale(2).move_to(boxes[1]).rotate(-20*DEGREES)
        flash1 = VGroup(*[Line(ORIGIN,DOWN*.5,buff=0.05).rotate(PI/2*i,about_point=ORIGIN).set_stroke(width=8) for i in range(4)])
        flash1.move_to(np.array([-1.25,1.5,0]))
        flash2 = VGroup(*[Line(ORIGIN,DOWN*.5,buff=.08).rotate(PI/2*i,about_point=ORIGIN).set_stroke(width=8) for i in range(4)])
        flash2.move_to(np.array([1.35,2.5,0]))

        self.add(final_light,ground,boxes,N,R,flash1,flash2)






