from colour import hex2rgb
from manimlib import*


def length_func(norm): return 0.55 * sigmoid(norm/2.2)


def shorten(vec):
    return normalize(vec)*abs(length_func(get_norm(vec)))


def get_array(DL, UR, ranges):
    l2r = np.linspace(DL[0], UR[0], ranges[0])
    b2t = np.linspace(DL[1], UR[1], ranges[1])
    grid = np.array([[[x, y, 0] for y in b2t] for x in l2r])
    return grid


def inside(polygon, point, return_intersection=False):
    points = polygon.get_vertices()
    points = np.append(points, [points[0]], axis=0)
    intersection = 0
    side = np.where(points[0, 1] <= point[1], -1, 1)
    for i in range(len(points)):
        if ((points[i, 1] <= point[1]) and (side == 1)) or ((points[i, 1] > point[1]) and (side == -1)):
            side = -side
            if match_interpolate(points[i-1, 0], points[i, 0], points[i-1, 1], points[i, 1], point[1]) < point[0]:
                intersection += 1
    if not return_intersection:
        return not (intersection % 2 == 0)
    else:
        return intersection


def dis(array1, array2):
    return np.sum((array1-array2)**2)**0.5


def nearest(polygon, point, closed_curve=True):
    points = polygon.get_vertices()
    if closed_curve:
        distance = np.array([dis(get_closest_point_on_line(
            points[i-1], points[i], point), point) for i in np.arange(len(points))])
    else:
        distance = np.array([dis(get_closest_point_on_line(
            points[i-1], points[i], point), point) for i in np.arange(1, len(points))])
    index = np.where(distance == np.min(distance))[0][0]
    return (points[index-1], points[index])


def nearest2(polygon, point, closed_curve=True):
    points = polygon.get_vertices()
    if closed_curve:
        distance = np.array([dis(get_closest_point_on_line(
            points[i-1], points[i], point), point) for i in np.arange(len(points))])
    else:
        distance = np.array([dis(get_closest_point_on_line(
            points[i-1], points[i], point), point) for i in np.arange(1, len(points))])
    index = np.where(distance == np.min(distance))[0][0]
    return get_closest_point_on_line(points[index-1], points[index], point)


class ArrayMass:

    def __init__(self, width, height, *boxes, res_per_unit=2):
        self.grid = get_array(np.array([-width/2, -height/2, 0]), np.array(
            [width/2, height/2, 0]), [int(width*res_per_unit), int(height*res_per_unit)])
        self.shape = self.grid.shape
        self.v = np.zeros_like(self.grid)
        self.k = 40
        self.mass = 0.01
        self.dx = width/int(width*res_per_unit-1)
        self.dy = height/int(height*res_per_unit-1)
        self.boxes = boxes
        self.dt = 1/600
        self.g = 9.8

    def get_neighours(self, index):
        i, j = index
        i = i % self.shape[0]
        j = j % self.shape[1]
        x = np.array([i-1, i+1])
        x = np.delete(x, np.where((x < 0) | (x >= self.shape[0])))
        y = np.array([j-1, j+1])
        y = np.delete(y, np.where((y < 0) | (y >= self.shape[1])))
        near_x = np.array([self.grid[X, j] for X in x])
        near_y = np.array([self.grid[i, Y] for Y in y])
        far = np.array([self.grid[X, Y] for X in x for Y in y])
        return (near_x, near_y, far)

    def get_pure_neighours(self, index):
        a, b, c = self.get_neighours(index)
        return np.array([*a, *b, *c])

    def get_neighour_indexs(self, index):
        i, j = index
        i = i % self.shape[0]
        j = j % self.shape[1]
        x = np.array([i-1, i+1])
        x = np.delete(x, np.where(x < 0))
        y = np.array([j-1, j+1])
        y = np.delete(y, np.where(y < 0))
        near_x = np.array([(X, j) for X in x])
        near_y = np.array([(i, Y) for Y in y])
        far = np.array([(X, Y) for X in x for Y in y])
        return (near_x, near_y, far)

    def get_border(self):
        return np.append(self.grid[0, :-1], [*self.grid[:-1, -1], *np.flip(self.grid[-1, 1:], 0), *np.flip(self.grid[1:, 0], 0)], 0)

    def get_spring_force(self, index):
        i, j = index
        near_x, near_y, far = self.get_neighours((i, j))
        center = self.grid[i, j]
        near_x += -center
        near_y += -center
        far += -center
        x_force = np.sum(
            np.array([normalize(x)*(get_norm(x)-self.dx)*self.k for x in near_x]), 0)
        y_force = np.sum(
            np.array([normalize(x)*(get_norm(x)-self.dy)*self.k for x in near_y]), 0)
        far_force = np.sum(np.array([normalize(
            x)*(get_norm(x)-get_norm(np.array([self.dx, self.dy])))*self.k for x in far]), 0)

        return (x_force + y_force + far_force)/self.mass

    def get_spring_force_sep(self, index):
        i, j = index
        near_x, near_y, far = self.get_neighours((i, j))
        center = self.grid[i, j]
        near_x += -center
        near_y += -center
        far += -center
        x_force = np.array(
            [normalize(x)*(get_norm(x)-self.dx)*self.k for x in near_x])
        y_force = np.array(
            [normalize(x)*(get_norm(x)-self.dy)*self.k for x in near_y])
        far_force = np.array([normalize(
            x)*(get_norm(x)-get_norm(np.array([self.dx, self.dy])))*self.k for x in far])
        return np.array([*x_force, *y_force, *far_force])

    def move_by_force(self):
        a = np.array([[self.get_spring_force((i, j))+np.array([0, -self.g, 0])
                     for j in np.arange(self.shape[1])] for i in np.arange(self.shape[0])])

        self.v += a*self.dt
        #self.v *= 0.99
        self.grid += self.v*self.dt + 0.5*self.dt**2*a

    def bounce(self):
        for i in np.arange(self.shape[0]):
            for j in np.arange(self.shape[1]):
                for poly in self.boxes:
                    # print(poly)
                    if inside(poly, self.grid[i, j]):
                        a, b = nearest(poly, self.grid[i, j])
                        self.grid[i, j] = get_closest_point_on_line(
                            a, b, self.grid[i, j])
                        self.v[i, j] = flip_about_a_line(0, b-a, self.v[i, j])
        return self


class SoftBody(Polygon):

    CONFIG = {
        "note_grid": False,
        "note_relationship": False,
        "note_force": False,
        "note_seperate_force": False,
        "note_speed": False,
        "res_per_unit": 2
    }

    def __init__(self, width, height, *boxes, **kwargs):
        digest_config(self, kwargs)
        self.array = ArrayMass(width, height, *boxes,
                               res_per_unit=self.res_per_unit)
        self.kwargs = kwargs
        border = self.array.get_border()
        super().__init__(*border, **kwargs)
        self.set_stroke(width=0).set_fill(color=BLUE, opacity=1)

    def up(self):

        def move(obj):
            for i in range(5):
                obj.array.move_by_force()
                obj.array.bounce()
            obj.become(Polygon(*obj.array.get_border()
                               ).set_stroke(width=0).set_fill(color=BLUE, opacity=1))

        self.add_updater(move)

    def step(self, steps):
        for i in range(steps):
            self.array.move_by_force()
            # self.array.bounce()
        self.become(Polygon(*self.array.get_border()
                            ).set_stroke(width=0).set_fill(color=BLUE, opacity=1))

    def bounce(self):
        self.array.bounce()
        self.become(Polygon(*self.array.get_border()
                            ).set_stroke(width=0).set_fill(color=BLUE, opacity=1))
        return self

    def shift(self, vector):
        self.array.grid += vector
        return super().shift(vector)

    def get_note_grid(self):
        return VGroup(*[Dot(i) for j in self.array.grid for i in j])

    def get_note_relationship(self):
        return VGroup(*[VGroup(*[Line(self.array.grid[i, j], nei, stroke_width=1).set_color(GREY) for nei in self.array.get_pure_neighours((i, j))])
                        for i in np.arange(self.array.shape[0]) for j in np.arange(self.array.shape[1])])

    def get_note_force(self):
        return VGroup(*[Vector(shorten(self.array.get_spring_force((i, j))/self.array.mass)).shift(self.array.grid[i, j]).set_color(YELLOW)
                        for i in np.arange(self.array.shape[0]) for j in np.arange(self.array.shape[1])])

    def get_seperate_note_force(self):
        return VGroup(*[VGroup(*[Vector(shorten(f)).shift(self.array.grid[i, j]).set_color(YELLOW) for f in self.array.get_spring_force_sep((i, j))]).set_color(YELLOW)
                        for i in np.arange(self.array.shape[0]) for j in np.arange(self.array.shape[1])])

    def get_note_speed(self):
        return VGroup(*[Vector(shorten(self.array.v[i, j])).set_color(RED).shift(self.array.grid[i, j])
                        for i in np.arange(self.array.shape[0]) for j in np.arange(self.array.shape[1])])

    def get_rec(self):
        return Polygon(*self.array.get_border()).set_fill(BLUE, 1).set_stroke(width=0)

class introduce(Scene):
    def construct(self):
        grid = NumberPlane([-15, 15], [-12, 4]).set_color(GREY_E)
        self.add(grid)
        ground = Rectangle(FRAME_WIDTH, 4).next_to(DOWN*7, DOWN).set_opacity(1).set_color_by_code(
            "color.rgb = mix(vec3(0.7,0.2,0.8),vec3(0.4,0.1,0.8),-(point.y+1.)/4.);")
        soft = SoftBody(4, 2, ground, color=BLUE)
        ruan = TexText("软").move_to(
            (soft.array.grid[2, 2]+soft.array.grid[2, 1])/2).scale(3)
        ti = TexText("体").move_to(
            (soft.array.grid[5, 2]+soft.array.grid[5, 1])/2).scale(3)
        ruan.save_state()
        ti.save_state()
        frame = self.camera.frame
        frame.add_updater(lambda obj: obj.move_to(soft))

        def tape_on_soft(index1, index2):
            i1, j1 = index1
            i2, j2 = index2

            def update(obj):
                obj.restore()
                obj.move_to(
                    (soft.array.grid[i1, j1]+soft.array.grid[i2, j2])/2)
                obj.rotate(np.arctan2(
                    soft.array.grid[i1, j1, 1]-soft.array.grid[i2, j2, 1],
                    soft.array.grid[i1, j1, 0]-soft.array.grid[i2, j2, 0]
                )-PI/2
                )
            return update
        # self.add(ground,soft,ruan,ti)
        self.play(ShowCreation(VGroup(soft)), ShowCreation(ground))
        self.add(soft)
        self.play(DrawBorderThenFill(ruan), DrawBorderThenFill(ti))
        self.add(frame)
        ruan.add_updater(tape_on_soft((2, 2), (2, 1)))
        ti.add_updater(tape_on_soft((5, 2), (5, 1)))
        soft.up()
        self.wait(8)
        framerec = FullScreenRectangle(fill_opacity=1).set_color(
            BLACK).add_updater(lambda obj: obj.move_to(frame))
        self.play(FadeIn(framerec))
        # soft.clear_updaters()
        # self.add(grid)
        # self.play(FadeIn(grid))
        #soft.add_updater(lambda obj:obj.move_to(self.mouse_drag_point))


class setup_function(Scene):
    def construct(self):
        self.index = 0
        subtitle = [
            r"在$\mathrm{manim}$里，有一个内置函数$\mathtt{get\_closest\_point\_on\_line}$",
            "它可以告诉我们一个线段上到某个点距离最短的点",
            "由此，我们可以写出一个函数让它返回一个多边形上到某点距离最短的点",
            "实际上，我们接下来还需要用到这条边，那我们顺手也写一下吧",
            "我们还需要一个函数，来判断一个点是否在一个多边形之内",
            "实现方式也很简单，我们可以使用祖传的交点法",
            "当交点个数为奇数时，点在形内；交点个数为偶数时，点在形外"
        ]
        subti = VGroup(*[TexText(i).scale(0.7).to_edge(DOWN)
                       for i in subtitle])

        def sub():
            if self.index != 0:
                self.play(Write(subti[self.index]),
                          FadeOut(subti[self.index-1]))
            else:
                self.play(Write(subti[self.index]))

            self.index += 1

        title = TexText(r"$\mathrm{Chapter~0}$",
                        "准备工作", font_size=100).arrange(DOWN)
        grid = NumberPlane([-20, 20], [-10, 10]).set_color(GREY_E)
        title.set_color_by_code(
            f"color.rgb = mix(vec3({hex2rgb(WHITE)}),vec3(0.),abs(point.x*point.y/2.));")
        self.play(DrawBorderThenFill(title))
        self.wait(2)
        self.play(FadeOut(title))
        self.play(FadeIn(grid))
        self.wait()

        sub()
        roundaround = Circle(radius=3)
        input_dot = Dot(roundaround.pfp(0.1))
        input_line = Line(LEFT*2, RIGHT*2).rotate(10*DEGREES)
        output_dot = Dot(get_closest_point_on_line(input_line.get_start(), input_line.get_end(), input_dot.get_center())).add_updater(
            lambda obj: obj.move_to(get_closest_point_on_line(input_line.get_start(), input_line.get_end(), input_dot.get_center())))
        output_line = Line(input_dot.get_center(), output_dot.get_center(), color=GREY).add_updater(lambda obj: obj.put_start_and_end_on(
            input_dot.get_center(), get_closest_point_on_line(input_line.get_start(), input_line.get_end(), input_dot.get_center())))
        self.play(ShowCreation(input_line), FadeIn(input_dot))
        self.wait()
        self.add(output_line, output_dot, input_dot)
        self.play(FadeIn(output_dot), FadeIn(output_line))
        self.wait()
        input_dot.add_updater(
            lambda obj: obj.rotate(.2*DEGREES, about_point=ORIGIN))
        self.wait()
        sub()
        tex_to_color_map = {
            "{a}": RED,
            "{b}": YELLOW,
            "{p}": TEAL
        }
        input_note = Tex("{p}").set_color_by_tex_to_color_map(tex_to_color_map).scale(
            0.7).add_updater(lambda obj: obj.next_to(input_dot.get_center()))
        startpoint_note = Tex("{a}").set_color_by_tex_to_color_map(
            tex_to_color_map).scale(0.7).next_to(input_line.get_start(), LEFT)
        endpoint_note = Tex("{b}").set_color_by_tex_to_color_map(
            tex_to_color_map).scale(0.7).next_to(input_line.get_end())
        output_note = Tex(r"\mathtt{get\_closest\_point\_on\_line(}", "{a}", ",", "{b}", ",", "{p}", "\mathtt{)}").scale(
            0.7).set_color_by_tex_to_color_map(tex_to_color_map).add_updater(lambda obj: obj.next_to(output_dot, DOWN))
        # self.add(input_note,startpoint_note,endpoint_note,output_note)
        self.play(
            *[Write(i) for i in [input_note, startpoint_note, endpoint_note, output_note]])
        self.wait(6)
        random_poly = Polygon(*np.array([[-1, 3, 0], [-4, 0, 0], [-2, -1, 0], [-1, -3, 0], [
                              3, -2, 0], [1, 0, 0], [3, 2, 0]])).set_color(BLUE).set_fill(opacity=0.5)
        self.play(*[FadeOut(i) for i in [input_note,
                  startpoint_note, endpoint_note, output_note]])
        input_dot.clear_updaters()
        input_note.clear_updaters()
        startpoint_note.clear_updaters()
        endpoint_note.clear_updaters()
        output_note.clear_updaters()
        self.play(input_line.animate.set_color(BLUE).put_start_and_end_on(np.array(
            [-1, 3, 0]), np.array([-4, 0, 0])), input_dot.animate.move_to(np.array([-2.5, 1.5, 0])))
        # self.add(random_poly,output_line,input_dot,output_dot)
        self.play(ShowCreation(VGroup(random_poly)))
        self.add(output_line, input_dot, output_dot)

        self.remove(input_line)
        sub()
        self.wait()
        output_dot.clear_updaters().add_updater(lambda obj: obj.move_to(
            nearest2(random_poly, input_dot.get_center())))
        output_line.clear_updaters().add_updater(lambda obj: obj.put_start_and_end_on(
            input_dot.get_center(), nearest2(random_poly, input_dot.get_center())))
        input_dot.add_updater(
            lambda obj: obj.rotate(.2*DEGREES, about_point=ORIGIN))
        self.wait(6)
        sub()
        input_line.set_color(YELLOW).add_updater(lambda obj: obj.put_start_and_end_on(
            *nearest(random_poly, input_dot.get_center())))
        self.play(FadeIn(input_line))
        self.add(output_line, input_dot, output_dot)
        self.wait(6)
        self.play(*[FadeOut(i) for i in [input_line, output_dot, output_line]])
        self.wait()

        sub()
        input_dot.add_updater(lambda obj: obj.set_color(interpolate_color(
            GREY, WHITE, inside(random_poly, input_dot.get_center()))))
        self.wait(6)
        sub()
        random_line = Line().add_updater(lambda obj: obj.set_color(interpolate_color(GREY, WHITE, inside(random_poly,
                                                                                                         input_dot.get_center()))).put_start_and_end_on(input_dot.get_center(), np.array([-10, input_dot.get_y(), 0])))
        internum = Integer(2).scale(0.7).add_updater(lambda obj: obj.set_value(inside(random_poly, input_dot.get_center(
        ), True)).set_color(interpolate_color(GREY, WHITE, inside(random_poly, input_dot.get_center()))).next_to(input_dot))

        self.add(random_line, internum)
        self.play(FadeIn(random_line), FadeIn(internum))
        self.wait(6)
        sub()
        self.wait(6)
        frame = FullScreenRectangle().set_color(BLACK).set_opacity(1)
        self.play(FadeIn(frame))


class Abstract(Scene):
    def construct(self):
        self.index = 0
        subtitle = [
            "我们的软体架构大致如上:",
            "接着我们使用欧拉法对$\\mathtt{self.grid}$更新",
            "而我们的$\\mathtt{self.spring}$又与$\\mathtt{self.grid},\\mathtt{self.k},\\mathtt{self.dx},\\mathtt{self.dy}$有关",
            "这个计算的实现不难，只需用到胡克定理：$F=k\Delta x$",
            "让我们对这个弹簧网格的一部分进行详细研究",
            "当我们的网格发生形变时，弹簧长度发生变化，产生弹力",
            "我们再把这些弹力加起来，就求出了这一质点受到的弹力",
            "同样的，我们对一个软体中所有的质点都这样做，就求出了$\\mathtt{self.spring}$"
        ]
        subti = VGroup(*[TexText(i).scale(0.7).to_edge(DOWN)
                       for i in subtitle])

        def sub():
            if self.index != 0:
                self.play(Write(subti[self.index]),
                          FadeOut(subti[self.index-1]))
            else:
                self.play(Write(subti[self.index]))

            self.index += 1
        grid = NumberPlane([-20, 20], [-10, 10]).set_color(GREY_E)
        title = TexText("$\mathrm{Chapter~1}$", "弹簧格点", font_size=100).arrange(DOWN).set_color_by_code(
            f"color.rgb = mix(vec3({hex2rgb(WHITE)}),vec3(0.),abs(point.x*point.y/2.));")
        title[1].insert_n_curves(30)
        self.play(DrawBorderThenFill(title))
        self.wait(2)
        self.play(FadeOut(title))
        self.play(FadeIn(grid))
        self.wait()

        # sub()
        rec = Rectangle(FRAME_WIDTH, 2).next_to(DOWN*2, DOWN).rotate(5*DEGREES)
        soft = SoftBody(2, 4, rec, color=BLUE).shift(LEFT*3)
        self.play(FadeIn(soft))
        soft.up()
        self.wait(1.5)
        soft.clear_updaters()
        sub()

        grid = soft.get_note_grid()
        self.play(LaggedStart(*[GrowFromCenter(i) for i in grid]))
        grid_note = Tex(r"\mathtt{self}", r"\mathtt{.grid}", r"\text{\#储存格点坐标}").scale(
            0.7).set_color_by_tex_to_color_map({"self": ORANGE, "#": GREY})
        acc_note = Tex(r"\mathtt{self}", r"\mathtt{.spring}", r"\text{\#储存格点受到弹力}").scale(
            0.7).set_color_by_tex_to_color_map({"self": ORANGE, "#": GREY})
        v_note = Tex(r"\mathtt{self}", r"\mathtt{.velo}", r"\text{\#储存格点速度}").scale(
            0.7).set_color_by_tex_to_color_map({"self": ORANGE, "#": GREY})
        mass_note = Tex(r"\mathtt{self}", r"\mathtt{.mass}", r"\text{\#储存格点质量}").scale(
            0.7).set_color_by_tex_to_color_map({"self": ORANGE, "#": GREY})
        k_note = Tex(r"\mathtt{self}", r"\mathtt{.k}", r"\text{\#弹簧劲度系数}").scale(
            0.7).set_color_by_tex_to_color_map({"self": ORANGE, "#": GREY})
        dt_note = Tex(r"\mathtt{self}", r"\mathtt{.dt}", r"\text{\#渲染步长}").scale(
            0.7).set_color_by_tex_to_color_map({"self": ORANGE, "#": GREY})
        dx_note = Tex(r"\mathtt{self}", r"\mathtt{.dx}", r"\text{\#横向弹簧原长}").scale(
            0.7).set_color_by_tex_to_color_map({"self": ORANGE, "#": GREY})
        dy_note = Tex(r"\mathtt{self}", r"\mathtt{.dy}", r"\text{\#纵向弹簧原长}").scale(
            0.7).set_color_by_tex_to_color_map({"self": ORANGE, "#": GREY})
        g_note = Tex(r"\mathtt{self}", r"\mathtt{.g}", r"\text{\#重力加速度}").scale(
            0.7).set_color_by_tex_to_color_map({"self": ORANGE, "#": GREY})
        boxes_note = Tex(r"\mathtt{self}", r"\mathtt{.boxes}", r"\text{\#地面}").scale(
            0.7).set_color_by_tex_to_color_map({"self": ORANGE, "#": GREY})

        mass_note[2].insert_n_curves(30)
        lists = [[i[:2], i[2]] for i in [grid_note, acc_note, v_note,
                                         mass_note, k_note, dt_note, dx_note, dy_note, g_note, boxes_note]]
        notes = VGroup(*[j for i in lists for j in i]
                       ).arrange_in_grid(n_cols=2).move_to(np.array([3, 1, 0]))
        self.play(Write(grid_note))
        self.wait()

        relationship = soft.get_note_relationship()
        self.add(relationship, grid)
        self.play(LaggedStart(*[ShowCreation(i) for i in relationship]))

        tips = TexText("这些连接质点的线段即为弹簧").scale(
            0.4).set_color(GREY).next_to(subti, UP)
        self.wait()
        self.play(Write(tips))
        self.wait()
        self.play(LaggedStart(*[Uncreate(i)
                  for i in relationship]), FadeOut(tips))
        self.wait()

        seperate_force = soft.get_seperate_note_force()
        self.play(LaggedStart(*[GrowArrow(a)
                  for i in seperate_force for a in i], lag_ratio=0.01))
        self.wait()

        force = soft.get_note_force()
        self.play(ReplacementTransform(seperate_force, force))
        self.wait()
        self.play(Write(acc_note))
        self.wait()
        self.play(LaggedStart(
            *[i.animate.scale(0, about_point=i.get_start()) for i in force]))
        self.wait()

        velo = soft.get_note_speed()
        self.play(LaggedStart(*[GrowArrow(i) for i in velo]))
        self.wait()
        self.play(Write(v_note))
        self.wait()
        self.play(LaggedStart(
            *[i.animate.scale(0, about_point=i.get_start()) for i in velo]))
        self.wait()

        self.play(Write(notes[6:]), run_time=6)
        self.wait(2)
        self.play(FadeOut(soft), FadeOut(grid))
        self.wait()
        sub()
        euler = TexText("$\\mathtt{self}$", "$\\mathtt{.velo+=}$", "$\\mathtt{self}$", "$\\mathtt{.dt*(}$", "$\\mathtt{self}$", "$\\mathtt{.spring/}$",
                        "$\\mathtt{self}$", "$\\mathtt{.mass+np.array([0,-}$", "$\\mathtt{self}$", "$\\mathtt{.g,0]))}$\\\\",
                        "$\\mathtt{self}$", "$\\mathtt{.grid+=}$", "$\\mathtt{self}$", "$\\mathtt{.velo*}$", "$\\mathtt{self}$", "$\\mathtt{.dt}$").set_color_by_tex_to_color_map({"self": ORANGE})
        euler.set_width(7).move_to(np.array([-3.5, 0, 0]))
        self.play(Write(euler))
        self.wait(3)
        self.play(FadeOut(euler))
        self.wait()
        sub()
        self.wait(2)
        sub()
        self.wait()
        self.play(FadeOut(notes))

        def put_on_line(obj, line, value):
            obj.restore()
            obj.next_to(line.get_center(), UP, buff=0.05).set_value(value)
            obj.rotate(np.arctan((line.get_start()[1]-line.get_end()[1])/(line.get_start()[0]-line.get_end()[0])),
                       about_point=line.get_center())

        def get_force(line, length):
            vec = normalize(line.get_vector())
            delta_x = line.get_length() - length
            return Vector(vec*delta_x*4).set_color(YELLOW).set_opacity(0.7)

        neibours = VGroup(
            Dot(np.array([-2, -2, 0])),
            Dot(np.array([-2, 0, 0])),
            Dot(np.array([-2, 2, 0])),
            Dot(np.array([0, 2, 0])),
            Dot(np.array([2, 2, 0])),
            Dot(np.array([2, 0, 0])),
            Dot(np.array([2, -2, 0])),
            Dot(np.array([0, -2, 0])),
        )
        lengths = np.array([2**0.5, 1, 2**0.5, 1, 2**0.5, 1, 2**0.5, 1])*2
        center = Dot(ORIGIN)
        relation = VGroup(
            *[Line(center.get_center(), j.get_center()).set_color(GREY) for j in neibours])

        def update_relation(obj):
            for i in range(8):
                obj[i].put_start_and_end_on(
                    center.get_center(), neibours[i].get_center())

        numbers = VGroup(
            *[DecimalNumber(include_sign=True).scale(0.4) for i in range(8)])
        for decimal, line in zip(numbers, relation):
            decimal.save_state()
            put_on_line(decimal, line, 0)

        def update_numbers(obj):
            for decimal, line, length in zip(obj, relation, lengths):
                put_on_line(decimal, line, line.get_length()-length)

        forces = VGroup(*[get_force(line, length)
                        for line, length in zip(relation, lengths)])

        def update_forces(obj):
            obj.become(VGroup(*[get_force(line, length)
                       for line, length in zip(relation, lengths)]))

        sub()
        self.wait()
        self.play(Write(center))
        self.play(FadeIn(neibours))
        self.wait()
        self.play(ShowCreation(relation))
        self.play(Write(numbers))
        self.add(forces)
        self.wait()
        relation.add_updater(update_relation)
        numbers.add_updater(update_numbers)
        forces.add_updater(update_forces)
        sub()
        self.play(*[mob.animate.shift(np.array([random.uniform(-0.5, 0.5),
                  random.uniform(-0.5, 0.5), 0])) for mob in neibours], run_time=3)
        self.wait(2)

        added_force = Vector(np.sum(
            np.array([vec.get_vector() for vec in forces]), axis=0)).set_color(YELLOW)
        forces.clear_updaters()
        sub()
        self.play(*[Transform(i, added_force.copy()) for i in forces])
        self.remove(forces)
        self.add(added_force)
        soft.move_to(ORIGIN)
        grid = soft.get_note_grid()
        grid_forces = soft.get_note_force()
        numbers.clear_updaters()
        self.play(FadeOut(added_force), FadeOut(numbers))
        self.add(soft, grid, neibours, center, relation)
        # self.play(,)
        self.play(
            FadeIn(soft), FadeIn(grid),
            *[neibours[d].animate.move_to(grid[g]) for d, g in [(
                0, 0), (1, 1), (2, 2), (3, 10), (4, 18), (5, 17), (6, 16), (7, 8)]],
            center.animate.move_to(grid[9])
        )

        def update_through(obj, alpha):
            index = int(alpha*len(grid))
            index = np.minimum(len(grid)-1, index)
            obj.move_to(grid[index])
            neibours.become(
                VGroup(*[Dot(i) for i in soft.array.get_pure_neighours((index //
                       soft.array.shape[1], index % soft.array.shape[1]))])
            )
            self.add(grid_forces[index])
        self.wait()
        sub()
        self.wait()
        # self.add(show_forces)
        self.play(UpdateFromAlphaFunc(center, update_through), run_time=4)
        self.wait(2)
        relation.clear_updaters()
        self.play(FadeOut(relation), FadeOut(center),
                  FadeOut(neibours), FadeOut(subti[7]))
        grid.add_updater(lambda obj: obj.become(soft.get_note_grid()))
        grid_forces.add_updater(lambda obj: obj.become(soft.get_note_force()))
        self.add(grid, grid_forces)
        soft.up()
        self.wait(7)
        frame = FullScreenRectangle().set_color(BLACK).set_opacity(1)
        self.play(FadeIn(frame))


class colision(Scene):
    def construct(self):
        self.index = 0
        subtitle = [
            "在我们的模拟中，物体之间的碰撞也是不可或缺的一部分",
            "那么让我们来看看如何实现物体碰撞的拟真吧",
            "现在，这个软体有一部分已经进入了多边形内，我们要把它推出来",
            "我们先用之前写过的函数判断质点是否在多边形内",
            "然后我们将顶点推至多边形上，并将速度矢量沿边翻折"
        ]
        subti = VGroup(*[TexText(i).scale(0.7).to_edge(DOWN)
                       for i in subtitle]).fix_in_frame()

        def sub():
            if self.index != 0:
                self.play(Write(subti[self.index]),
                          FadeOut(subti[self.index-1]))
            else:
                self.play(Write(subti[self.index]))

            self.index += 1
        grid = NumberPlane([-20, 20], [-10, 10]).set_color(GREY_E)
        title = TexText("$\mathrm{Chapter~2}$", "碰撞", font_size=100).arrange(DOWN).set_color_by_code(
            f"color.rgb = mix(vec3({hex2rgb(WHITE)}),vec3(0.),abs(point.x*point.y/2.));")

        title[1].insert_n_curves(30)
        self.play(DrawBorderThenFill(title))
        self.wait(2)
        self.play(FadeOut(title))
        self.play(FadeIn(grid))
        self.wait()

        poly = Polygon(np.array([-1, -2, 0]), np.array([8, 1, 0]), np.array(
            [8, -4, 0]), np.array([-8, -4, 0]), np.array([-8, 12, 0]))
        poly.set_color_by_rgb_func(lambda p: interpolate(
            hex_to_rgb(BLUE), hex_to_rgb(PURPLE), sigmoid(p[0]/5)))
        self.play(FadeIn(poly))
        soft = SoftBody(2, 2, poly).shift(UP*3)

        gridpoints = soft.get_note_grid()
        velo = soft.get_note_speed()
        self.wait()
        self.play(FadeIn(soft), FadeIn(gridpoints), FadeIn(velo))

        gridpoints.add_updater(lambda m: m.become(soft.get_note_grid()))
        velo.add_updater(lambda m: m.become(soft.get_note_speed()))
        self.wait()
        sub()
        self.wait(2)
        soft.up()

        sub()
        # self.wait(0.1)
        # soft.clear_updaters()
        soft.array.boxes = []
        self.wait(0.05)
        soft.clear_updaters()

        gridpoints.clear_updaters()
        velo.clear_updaters()
        self.wait()
        frame = self.camera.frame
        frame.save_state()
        self.play(frame.animate.scale(0.5).move_to(
            soft.array.grid[0, 2]), run_time=4)
        self.wait()
        sub()

        self.play(soft.animate.set_opacity(0.5))
        self.wait()
        sub()
        self.play(*[d.animate.set_color(interpolate_color(GREEN, RED,
                  inside(poly, d.get_center()))) for d in gridpoints])
        self.wait()

        def side_vector(polygon, point):
            a, b = nearest(polygon, point)
            return a-b

        move_grid_points = AnimationGroup(*[dot.animate.move_to(nearest2(poly, dot.get_center(
        ))).set_color(GREEN) for dot in gridpoints if inside(poly, dot.get_center())])
        move_velo_arrows = AnimationGroup(*[arrow.animate.shift(nearest2(poly, arrow.get_start())-arrow.get_start()).rotate(PI, axis=side_vector(
            poly, arrow.get_start()), about_point=nearest2(poly, arrow.get_start())) for arrow in velo if inside(poly, arrow.get_start())])

        polyside = soft.get_vertices()
        polyside_after = []
        for i in polyside:
            if inside(poly, i):
                polyside_after.append(nearest2(poly, i))
            else:
                polyside_after.append(i)

        sub()
        self.play(soft.animate.become(Polygon(*polyside_after).set_stroke(
            width=0).set_fill(BLUE, 0.5)), move_grid_points, move_velo_arrows)
        self.wait()
        self.play(soft.animate.set_fill(opacity=1), gridpoints.animate.set_color(
            WHITE), velo.animate.set_opacity(1))

        soft.array.boxes = [poly]
        soft.up()
        gridpoints.add_updater(lambda m: m.become(soft.get_note_grid()))
        velo.add_updater(lambda m: m.become(soft.get_note_speed()))
        self.play(frame.animate.restore(), run_time=2)
        self.wait(5)
        framerect = FullScreenRectangle().set_fill(BLACK, 1).set_stroke(width=0)
        self.play(FadeIn(framerect))


class simulation1(Scene):
    def construct(self):

        grid = NumberPlane([-20, 20], [-10, 10]).set_color(GREY_E)
        title = TexText("$\mathrm{Chapter~3}$", "模拟", font_size=100).arrange(DOWN).set_color_by_code(
            f"color.rgb = mix(vec3({hex2rgb(WHITE)}),vec3(0.),abs(point.x*point.y/2.));")

        title[1].insert_n_curves(30)
        self.play(DrawBorderThenFill(title))
        self.wait(2)
        self.play(FadeOut(title))
        self.play(FadeIn(grid))
        self.wait()

        Left = FRAME_X_RADIUS*LEFT
        Up = FRAME_Y_RADIUS*UP
        poly1 = Polygon(Left, Left+UP, UP/2, ORIGIN).set_fill(WHITE,
                                                              1).set_stroke(BLACK, 5).shift(UP)
        poly2 = poly1.copy().shift(-Left)
        poly3 = poly1.copy().shift(-Up)
        poly4 = poly1.copy().shift(-Left-Up)
        self.play(FadeIn(poly1), FadeIn(poly2), FadeIn(poly3), FadeIn(poly4))

        soft1 = SoftBody(1.5, 1.5, poly1).next_to(poly1, UP)
        soft2 = SoftBody(1.5, 1.5, poly2).next_to(poly2, UP)
        soft3 = SoftBody(1.5, 1.5, poly3).next_to(poly3, UP)
        soft4 = SoftBody(1.5, 1.5, poly4).next_to(poly4, UP)

        soft1.array.k = 10
        soft2.array.k = 20
        soft3.array.k = 40
        soft4.array.k = 80

        texs = VGroup(
            Tex("k=10").scale(.5).next_to(poly1, DOWN),
            Tex("k=20").scale(.5).next_to(poly2, DOWN),
            Tex("k=40").scale(.5).next_to(poly3, DOWN),
            Tex("k=80").scale(.5).next_to(poly4, DOWN),
        )
        self.play(FadeIn(soft1), FadeIn(soft2), FadeIn(soft3), FadeIn(soft4))
        self.play(FadeIn(texs))
        self.wait()

        soft1.up()
        soft2.up()
        soft3.up()
        soft4.up()
        self.wait(10)
        self.play(FadeOut(texs))


class simulation2(Scene):
    def construct(self):
        grid = NumberPlane([-20, 20], [-10, 10]).set_color(GREY_E)

        Left = FRAME_X_RADIUS*LEFT
        Up = FRAME_Y_RADIUS*UP
        poly1 = Polygon(Left, Left+UP, UP/2, ORIGIN).set_fill(WHITE,
                                                              1).set_stroke(BLACK, 5).shift(UP)
        poly2 = poly1.copy().shift(-Left)
        poly3 = poly1.copy().shift(-Up)
        poly4 = poly1.copy().shift(-Left-Up)
        self.add(grid, poly1, poly2, poly3, poly4)

        soft1 = SoftBody(1.5, 1.5, poly1).next_to(poly1, UP)
        soft2 = SoftBody(1.5, 1.5, poly2).next_to(poly2, UP)
        soft3 = SoftBody(1.5, 1.5, poly3).next_to(poly3, UP)
        soft4 = SoftBody(1.5, 1.5, poly4).next_to(poly4, UP)

        soft1.array.mass = .01
        soft2.array.mass = .02
        soft3.array.mass = .04
        soft4.array.mass = .08

        texs = VGroup(
            Tex("m=0.01").scale(.5).next_to(poly1, DOWN),
            Tex("m=0.02").scale(.5).next_to(poly2, DOWN),
            Tex("m=0.04").scale(.5).next_to(poly3, DOWN),
            Tex("m=0.08").scale(.5).next_to(poly4, DOWN),
        )
        self.play(FadeIn(soft1), FadeIn(soft2), FadeIn(soft3), FadeIn(soft4))
        self.play(FadeIn(texs))
        self.wait()

        soft1.up()
        soft2.up()
        soft3.up()
        soft4.up()
        self.wait(10)
        self.play(FadeOut(texs))


class simulation3(Scene):
    def construct(self):
        grid = NumberPlane([-20, 20], [-10, 10]).set_color(GREY_E)

        Left = FRAME_X_RADIUS*LEFT
        Up = FRAME_Y_RADIUS*UP
        poly1 = Polygon(Left, Left+UP, UP/2, ORIGIN).set_fill(WHITE,
                                                              1).set_stroke(BLACK, 5).shift(UP)
        poly2 = poly1.copy().shift(-Left)
        poly3 = poly1.copy().shift(-Up)
        poly4 = poly1.copy().shift(-Left-Up)
        self.add(grid, poly1, poly2, poly3, poly4)

        soft1 = SoftBody(1.5, 1.5, poly1, res_per_unit=2).next_to(poly1, UP)
        soft2 = SoftBody(1.5, 1.5, poly2, res_per_unit=3).next_to(poly2, UP)
        soft3 = SoftBody(1.5, 1.5, poly3, res_per_unit=4).next_to(poly3, UP)
        soft4 = SoftBody(1.5, 1.5, poly4, res_per_unit=5).next_to(poly4, UP)

        texs = VGroup(
            Tex("dx=dy=1").scale(.5).next_to(poly1, DOWN),
            Tex("dx=dy=\\frac12").scale(.5).next_to(poly2, DOWN),
            Tex("dx=dy=\\frac13").scale(.5).next_to(poly3, DOWN),
            Tex("dx=dy=\\frac14").scale(.5).next_to(poly4, DOWN),
        )
        self.play(FadeIn(soft1), FadeIn(soft2), FadeIn(soft3), FadeIn(soft4))
        self.play(FadeIn(texs))
        self.wait()

        soft1.up()
        soft2.up()
        soft3.up()
        soft4.up()
        self.wait(10)
        self.play(FadeOut(texs))
        self.play(FadeOut(VGroup(poly1, poly2, poly3, poly4)))
        self.play(FadeOut(grid))

class Thumbnail(Scene):
    def construct(self):
        wall = RegularPolygon(50).move_to(DOWN*2+RIGHT*2).set_color(RED).scale(1.5)
        wall2 = RegularPolygon(50).move_to(DOWN*2+LEFT*1).set_color(RED)

        self.add(wall,wall2)
        soft = SoftBody(2,2,wall,wall2,res_per_unit=3).move_to(np.array([4,5,0]))
        a = VGroup()
        self.count = 0
        def update(obj,dt):
            if self.count %20 == 0:
                obj.add(soft.get_rec().set_opacity(0.5))
            self.count+=1
        trace = TracedPath(soft.get_center).set_stroke(width=5)
        self.add(a,soft,trace)
        soft.array.v += LEFT*3
        a.add_updater(update)

        soft.up()
        self.wait(3)
        #text1 = Text("fuiyou~",font='Consolas').next_to(soft,UP)
        #self.add(text1)
        soft.clear_updaters()
        ruanti = TexText("软\\\\体").scale(5).to_edge(LEFT,buff=1).insert_n_curves(100)

        ruanti.apply_function(lambda p:p+np.array([np.cos(p[1]*5)/20,np.sin(p[0]*5)/20,0]))
        self.add(ruanti)
        back = FullScreenRectangle().set_fill("#333333",1)
        self.bring_to_back(back)
        self.wait(1)