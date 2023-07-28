from audioop import reverse
from pickle import FRAME
from manimlib import *


def grid_interpolate(x00, x01, x10, x11, alphax, alphay):
    return x11*alphax*alphay + x10*(1-alphax)*alphay + x01*alphax*(1-alphay) + x00*(1-alphax)*(1-alphay)


class Abstract_Flow_Field(Mobject):
    """
    Abstract form of the `Fluid` type.

    Parameters
    ----------
    x_range : list
        The x range for the fluid box.
    y_range : list
        The y range for the fluid box.
    x_num : int
        The size of grid along x direction.
    y_num : int
        The size of grid along y direction.
    rho : int, float
        The density of fluid.
    nu : int, float
        The viscosity of the fluid.
    """
    # TODO finish the description
    CONFIG = {
        "rho": 1,   # density
        "nu": .4,   # viscosity
        "dt": .001,  # time gap for each calculation
    }

    def __init__(self, x_range, y_range, x_num=40, y_num=40, **kwargs):
        digest_config(self, kwargs)
        super().__init__(**kwargs)
        self.nx = x_num + 1
        self.ny = y_num + 1
        self.x_num = x_num
        self.y_num = y_num
        self.x_range = x_range
        self.y_range = y_range
        self.p_cal = 100
        self.frame_cal = 5
        self.dx = (x_range[1] - x_range[0]) / x_num
        self.dy = (y_range[1] - y_range[0]) / y_num
        self.x = np.linspace(0, 2, self.nx)
        self.y = np.linspace(0, 2, self.ny)
        self.X, self.Y = np.meshgrid(self.x, self.y)

        self.u = np.zeros((x_num, y_num))  # horizontal
        self.v = np.zeros((x_num, y_num))  # vertical
        self.p = np.zeros((x_num, y_num))  # pressure field
        self.count = 0
        self.bound_buff = np.array([(x_num-10)/x_num, (y_num-10)/y_num, 1])

    def pressure_poisson(self):
        """∂²p/∂x² + ∂²p/∂y² = b(x,y)"""
        for _ in range(self.p_cal):
            self.p[1:-1, 1:-1] = (  (self.p[1:-1, 2:] + self.p[1:-1, 0:-2]) * self.dy**2 
                                  + (self.p[2:, 1:-1] + self.p[0:-2, 1:-1]) * self.dx**2 
                                  - self.rho  / self.dt * (
                                        (self.u[1:-1, 2:] - self.u[1:-1, 0:-2]) / (2 * self.dx) 
                                      + (self.v[2:, 1:-1] - self.v[0:-2, 1:-1]) / (2 * self.dy)
                                      ) * self.dx**2 * self.dy**2
                                  ) / (2 * (self.dx**2 + self.dy**2)) 
            self.pressure_bounary_condition()

    def pressure_bounary_condition(self):

        self.p[:, -1] = 0   # dp/dx = 0 at x = max_x
        self.p[0, :] = self.p[1, :]  # dp/dy = 0 at y = min_y
        self.p[:, 0] = 0    # dp/dx = 0 at x = min_x
        self.p[-1, :] = self.p[-2, :]     # p = 0 at y = max_y
        self.p[int(self.nx/3)-16:int(self.nx/3)+17, int(self.ny/2) - 16:int(self.ny/2)+17] = self.p[int(self.nx/3)-17, int(self.ny/2)]

    def calculate_cavity_flow(self):

        for _ in range(self.frame_cal):
            self.pressure_poisson()

            self.u[1:-1, 1:-1] = self.u[1:-1, 1:-1] + self.dt * (
                - self.u[1:-1, 1:-1] / self.dx *
                (self.u[1:-1, 1:-1] - self.u[1:-1, 0:-2]) -
                self.v[1:-1, 1:-1] / self.dy *
                (self.u[1:-1, 1:-1] - self.u[0:-2, 1:-1]) -
                (self.p[1:-1, 2:] - self.p[1:-1, 0:-2]) / (2 * self.rho * self.dx) +
                self.nu * (
                    (self.u[1:-1, 2:] - 2 * self.u[1:-1, 1:-1] + self.u[1:-1, 0:-2]) / self.dx**2 +
                    (self.u[2:, 1:-1] - 2 * self.u[1:-1, 1:-1] + self.u[0:-2, 1:-1]) / self.dy**2)
            )

            self.v[1:-1, 1:-1] = self.v[1:-1, 1:-1] + self.dt * (
                - self.u[1:-1, 1:-1] / self.dx *
                (self.v[1:-1, 1:-1] - self.v[1:-1, 0:-2]) -
                self.v[1:-1, 1:-1] / self.dy *
                (self.v[1:-1, 1:-1] - self.v[0:-2, 1:-1]) -
                (self.p[2:, 1:-1] - self.p[0:-2, 1:-1]) / (2 * self.rho * self.dy) +
                self.nu * (
                    (self.v[1:-1, 2:] - 2 * self.v[1:-1, 1:-1] + self.v[1:-1, 0:-2]) / self.dx**2 +
                    (self.v[2:, 1:-1] - 2 * self.v[1:-1,
                                                   1:-1] + self.v[0:-2, 1:-1])/self.dy**2
                ))
            self.flow_boundary_condition()

    def flow_boundary_condition(self):
        self.u[:, 0] = 0   # left wall
        self.u[:, -1] = 2   # right wall
        self.u[0, :] = 0    # bottom wall
        self.u[-1, :] = 0   # top wall
        self.u[int(self.nx/3)-16:int(self.nx/3)+17,
               int(self.ny/2)-16:int(self.ny/2)+17] = 0

        self.v[:, 0] = 0    # left wall
        self.v[:, -1] = 0   # right wall
        self.v[0, :] = 0    # bottom wall
        self.v[-1, :] = 0   # top wall
        self.v[int(self.nx/3)-16:int(self.nx/3)+17,
               int(self.ny/2)-16:int(self.ny/2)+17] = 0

    def get_alpha(self, coord):
        x = inverse_interpolate(*self.x_range, coord[0])
        y = inverse_interpolate(*self.y_range, coord[1])
        return np.array([x, y])

    def get_coord_by_index(self, index):
        x, y = index
        return np.array([self.x_range[0] + x*self.dx, self.y_range[0] + y*self.dy, 0])

    def get_speed(self, coord):
        prepared = self.get_alpha(coord) * np.array([self.x_num, self.y_num])
        index = np.round(prepared).astype(int)
        alphas = prepared % 1
        u1, u2, u3, u4 = self.u[[index[0], index[0]+1, index[0],
                                 index[0]+1], [index[1], index[1], index[1]+1, index[1]+1]]
        v1, v2, v3, v4 = self.v[[index[0], index[0]+1, index[0],
                                 index[0]+1], [index[1], index[1], index[1]+1, index[1]+1]]
        return grid_interpolate(
            np.array([u1, v1, 0]),
            np.array([u2, v2, 0]),
            np.array([u3, v3, 0]),
            np.array([u4, v4, 0]),
            *alphas
        )

    def inside(self, coord):
        return self.x_range[0]*self.bound_buff[0] <= coord[0] <= self.x_range[1]*self.bound_buff[0] and self.y_range[0]*self.bound_buff[1] <= coord[1] <= self.y_range[1]*self.bound_buff[1]

    def shifts(self, m):
        self.calculate_cavity_flow()
        self.count += 1
        for i in m:
            if not self.inside(i.get_center()):
                i.move_to(np.array([random.uniform(
                    *self.x_range), random.uniform(*self.y_range), 0])*self.bound_buff)
                pass
            speed = self.get_speed(i.get_center())
            if get_norm(speed) < 0.005 and self.count > 10:
                i.move_to(np.array([random.uniform(
                    *self.x_range), random.uniform(*self.y_range), 0])*self.bound_buff)
            else:
                i.shift(speed*self.dt*10)


color = [BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_E, ]


def flow(x_range, y_range, num):

    return VGroup(*[Dot(np.array([random.uniform(*x_range), random.uniform(*y_range), 0])).set_color(color[random.randint(0, len(color)-1)]) for i in range(num)])


class Flow_A(Abstract_Flow_Field):

    def pressure_bounary_condition(self):
        self.p[:, -1] = 0
        self.p[0, :] = self.p[1, :]
        self.p[:, 0] = 0
        self.p[-1, :] = self.p[-2, :]
        self.p[int(self.nx/2):int(self.nx/2)+4, int(self.ny*0.3):int(self.ny*0.7)
               ] = self.p[int(self.nx/2)-1, int(self.ny*0.3):int(self.ny*0.7)]

    def flow_boundary_condition(self):
        self.u[:, 0] = 5   # left wall
        self.u[:, -1] = 0   # right wall
        self.u[0, :] = 0    # bottom wall
        self.u[-1, :] = 0   # top wall
        self.u[int(self.nx/2):int(self.nx/2)+4,
               int(self.ny*0.3):int(self.ny*0.7)] = 0

        self.v[:, 0] = 0    # left wall
        self.v[:, -1] = 0   # right wall
        self.v[0, :] = 0    # bottom wall
        self.v[-1, :] = 0   # top wall

    def shifts(self, m):
        self.calculate_cavity_flow()
        self.count += 1
        for i in m:
            if not self.inside(i.get_center()):
                i.move_to(np.array([random.uniform(
                    *self.x_range), random.uniform(*self.y_range), 0])*self.bound_buff)
                pass
            speed = self.get_speed(i.get_center())
            if i.get_center()[0] > 0.6*FRAME_WIDTH:
                m.remove(i)
            elif get_norm(speed) < 0.005 and self.count > 10:
                i.move_to(np.array([random.uniform(
                    *self.x_range), random.uniform(*self.y_range), 0])*self.bound_buff)
            else:
                i.shift(speed*self.dt*10)


class Waring_And_Fun(Scene):
    def construct(self):
        Text = TexText(
            "该片有大量公式，公式恐惧症者慎入。"
        ).scale(0.5)
        self.play(FadeIn(Text))
        self.wait(3)
        self.play(FadeOut(Text))
        self.wait()
        fluid_a = Flow_A(x_range=[-FRAME_WIDTH, FRAME_WIDTH],
                         y_range=[-FRAME_Y_RADIUS, FRAME_Y_RADIUS], x_num=640, y_num=180)
        fluid_v = VGroup(TexText("流"), TexText("体")).scale(
            3).arrange(DOWN, buff=2).move_to(FRAME_WIDTH*LEFT*0.7)
        self.add(fluid_v)

        def form_flow(m):
            m.add(*flow([-FRAME_WIDTH, -FRAME_WIDTH*0.7],
                  [-FRAME_Y_RADIUS, FRAME_Y_RADIUS], num=2))
            fluid_a.shifts(m)
        fluid_v.add_updater(form_flow)
        self.wait(30)

        def delete_flow(m):
            for i, j in enumerate(m):
                if i % 5 == 0:
                    m.remove(j)
                    self.remove(j)
            fluid_a.shifts(m)
        fluid_v.clear_updaters().add_updater(delete_flow)
        self.wait(2)


class NS_equation(Scene):
    def construct(self):



        NS = MTex(
            r"{\partial \boldsymbol v \over \partial t} + (\boldsymbol v\cdot\nabla)\boldsymbol v = -{1\over\rho}\nabla{p}+\nu\nabla^2 \boldsymbol v",
            tex_to_color_map={
                r"\boldsymbol v": TEAL,
                r"{p}": ORANGE,
                r"\nu": YELLOW,
                r"\rho": RED,
            },
        )

        NSu = MTex(
            r"{\partial {u} \over \partial t} + {u} {\partial {u} \over \partial x} + {v} {\partial {u} \over \partial y} = -{1 \over \rho} {\partial {p} \over \partial x}+\nu \left({\partial^2 {u} \over \partial x^2} + {\partial^2 {u} \over \partial y^2} \right)",
            tex_to_color_map={
                r"{u}": TEAL_B,
                r"{v}": TEAL,
                r"{p}": ORANGE,
                r"\nu": YELLOW,
                r"\rho": RED,
            },
        ).next_to(ORIGIN, UP)
        NSv = MTex(
            r"{\partial {v} \over \partial t} + {u} {\partial {v} \over \partial x} + {v} {\partial {v} \over \partial y} = -{1 \over \rho} {\partial {p} \over \partial y}+\nu \left({\partial^2 {v} \over \partial x^2} + {\partial^2 {v} \over \partial y^2} \right)",
            tex_to_color_map={
                r"{u}": TEAL_B,
                r"{v}": TEAL,
                r"{p}": ORANGE,
                r"\nu": YELLOW,
                r"\rho": RED,
            },
        ).next_to(ORIGIN, DOWN)
        # NSv
        self.play(Write(NS))
        self.wait(5)
        explain = VGroup(
            Tex(r"\boldsymbol v", "(x,y,t)").set_color_by_tex(
                r"\boldsymbol v", TEAL),
            TexText("速度矢量"),
            Tex(r"p", "(x,y,t)").set_color_by_tex("p", ORANGE),
            TexText("压强"),
            Tex(r"\nu", color=YELLOW),
            TexText("运动粘度"),
            Tex(r"\rho", color=RED),
            TexText("液体密度"),
        ).scale(.7).arrange_in_grid(n_cols=2, h_buff=0.5).shift(DOWN)
        explain[0][0].save_state().set_x(explain[4].get_x())
        explain[2][0].save_state().set_x(explain[4].get_x())
        self.play(NS.animate.shift(UP))
        self.wait()

        def Explain(tex):
            start = NS.get_parts_by_tex(tex)[0][0]
            if tex == r"\boldsymbol v":
                end = explain[0][0]
                side = explain[1]
            elif tex == "{p}":
                end = explain[2][0]
                side = explain[3]
            elif tex == r"\nu":
                end = explain[4][0]
                side = explain[5]
            elif tex == r"\rho":
                end = explain[6][0]
                side = explain[7]
            return AnimationGroup(ReplacementTransform(start.copy(), end), Write(side))

        self.play(Explain(r"\boldsymbol v"))
        self.wait(5)
        self.play(Explain("{p}"))
        self.wait(5)
        self.play(Explain(r"\nu"))
        self.wait(5)
        self.play(Explain(r"\rho"))
        self.wait(5)
        self.play(
            explain[0][0].animate.restore(),
            explain[2][0].animate.restore(),
            Write(explain[0][1]), Write(explain[2][1]),
        )
        self.wait(5)
        self.play(FadeOut(explain), NS.animate.center())
        self.wait(5)
        self.play(TransformMatchingMTex(NS.copy(), NSu, key_map={
                  r"\boldsymbol v": "{u}"}), TransformMatchingMTex(NS, NSv, key_map={r"\boldsymbol v": "{v}"}))
        self.wait()
        NSvg = VGroup(NSu, NSv)
        self.play(NSvg.animate.scale(.5).to_corner(UL))

class Discrete_equation(Scene):
    def construct(self):
        NSu = MTex(
            r"{\partial {u} \over \partial t} + {u} {\partial {u} \over \partial x} + {v} {\partial {u} \over \partial y} = -{1 \over \rho} {\partial {p} \over \partial x}+\nu \left({\partial^2 {u} \over \partial x^2} + {\partial^2 {u} \over \partial y^2} \right)",
            tex_to_color_map={
                r"{u}": TEAL_B,
                r"{v}": TEAL_D,
                r"{p}": ORANGE,
                r"\nu": YELLOW,
                r"\rho": RED,
            },
        ).next_to(ORIGIN, UP)
        NSv = MTex(
            r"{\partial {v} \over \partial t} + {u} {\partial {v} \over \partial x} + {v} {\partial {v} \over \partial y} = -{1 \over \rho} {\partial {p} \over \partial y}+\nu \left({\partial^2 {v} \over \partial x^2} + {\partial^2 {v} \over \partial y^2} \right)",
            tex_to_color_map={
                r"{u}": TEAL_B,
                r"{v}": TEAL_D,
                r"{p}": ORANGE,
                r"\nu": YELLOW,
                r"\rho": RED,
            },
        ).next_to(ORIGIN, DOWN)
        NSvg = VGroup(NSu, NSv)
        NSvg.scale(.5).to_corner(UL)
        self.add(NSvg)
        a = Axes(axis_config={"include_tip": False}, height=60,
                 width=60, x_range=[-30, 30, 1], y_range=[-30, 30, 1])
        a.add(a.add_coordinate_labels(np.arange(-30, 31), np.arange(-30, 31)))
        def graph_func(x): return np.sin(x)*.5-np.sin(x*2+0.2)*.6-x**3 * \
            0.001+np.cos(x**2*0.1)
        b = a.get_graph(graph_func, x_range=[-8, 8, 0.01]).set_color(YELLOW)
        self.play(FadeIn(a), ShowCreation(b, run_time=5))
        frame = self.camera.frame
        self.wait(5)
        deri = MTex(r"{\mathrm d f \over\mathrm d x} {=} \lim_{{h} \to 0} {f(x+{h})-f(x)\over {h}}",
                    tex_to_color_map={"f": YELLOW, "{h}": RED,"=":WHITE}, use_plain_tex=True).fix_in_frame()
        deri.move_to(np.array([4, 2, 0]))
        question_mark = VGroup(*[Tex("?").move_to(b.pfp(i))
                               for i in np.linspace(0, 1, 50)])
        self.play(FadeIn(question_mark, shift=DOWN *
                  0.2, lag_ratio=0.05, run_time=5))
        self.play(FadeOut(question_mark, shift=DOWN *
                  0.2, lag_ratio=0.05, run_time=5))
        self.wait(5)
        self.play(
            frame.animate.move_to(np.array([2.5,graph_func(2.5),0])).scale(.01), 
            Write(deri),b.animate.set_stroke(width=.1))
        x_start = Dot(np.array([2.495, graph_func(2.495), 0]),radius=0.002)
        x_end = Dot(np.array([2.505, graph_func(2.505), 0]),radius=0.002)
        line_start = Line(np.array([2.495, graph_func(2.495), 0]),np.array([2.495, 0, 0])).set_stroke(width=.1)
        line_end = Line(np.array([2.505, graph_func(2.505), 0]),np.array([2.505, 0, 0])).set_stroke(width=.1)
        h_line = Line(np.array([2.495,graph_func(2.505),0]),np.array([2.505,graph_func(2.505),0])).set_stroke(width=.1)
        self.wait(5)
        self.play(ShowCreation(x_start),ShowCreation(line_start))
        self.play(TransformFromCopy(x_start, x_end),TransformFromCopy(line_start, line_end),ShowCreation(h_line))
        df = DecimalNumber(graph_func(2.505)-graph_func(2.495), num_decimal_places=4).scale(0.01).next_to(np.array([2.495,(graph_func(2.505)+graph_func(2.495))/2,0]),LEFT,buff=0.001)
        dx = DecimalNumber(2.505-2.495, num_decimal_places=2).scale(0.01).next_to(np.array([2.5,graph_func(2.505),0]),DOWN,buff=0.005)
        deri2 = MTex(r"{\mathrm d f \over\mathrm d x}\approx {f(x+0.01)-f(x)\over 0.01}",
                    tex_to_color_map={"f": YELLOW, "0.01": RED,r"\approx":WHITE}, use_plain_tex=True).fix_in_frame().move_to(np.array([4, 2, 0]))
        self.wait(10)
        self.play(TransformMatchingMTex(deri, deri2, key_map={"{h}": "0.01","=": r"\approx"}))
        self.play(FadeIn(dx),FadeIn(df))
        deri3 = MTex(r"{\mathrm d f \over\mathrm d x}(2.5)\approx"+f"{np.round((graph_func(2.505)-graph_func(2.495))/0.01,4)}",
        tex_to_color_map={"f": YELLOW, r"\approx":WHITE,"(2.5)":WHITE}, use_plain_tex=True).fix_in_frame().move_to(np.array([4, 2, 0]))
        self.wait()
        self.play(TransformMatchingMTex(deri2, deri3))
        self.wait(5)
        self.play(frame.animate.center().scale(100),FadeOut(deri3),FadeOut(df),FadeOut(dx),FadeOut(h_line),FadeOut(line_start),FadeOut(line_end),FadeOut(x_start),FadeOut(x_end),b.animate.set_stroke(width=5))
        self.wait()
        self.play(FadeOut(a),FadeOut(b))
        two_ways = VGroup(
            MTex(r"{\mathrm d f \over\mathrm d x}\approx {f(x+\Delta x)-f(x)\over \Delta x}",tex_to_color_map={"f": YELLOW, "\Delta x": RED}),
            MTex(r"{\mathrm d f \over\mathrm d x}\approx {f(x+\Delta x)-f(x-\Delta x)\over 2\Delta x}",tex_to_color_map={"f": YELLOW, "\Delta x": RED})
        ).arrange(DOWN)
        self.play(Write(two_ways))
        self.wait(10)
        self.play(FadeOut(two_ways))
        self.play(NSvg.animate.center().scale(2))
        self.wait(5)
        grid = Square3D(side_length=0.5).get_grid(39,39,39/2+.1,buff=0.1)
        self.bring_to_back(grid)
        self.play(FadeIn(grid),NSvg.animate.scale(.5).to_corner(UL).fix_in_frame())
        self.wait()
        surface_func = lambda x,y: np.sin(x)*np.cos(y)+np.sin(x*0.5+0.2)+x**3*y*0.001
        self.add(grid,NSvg)
        frame.save_state()
        self.play(frame.animate.set_euler_angles(-10*DEGREES,20*DEGREES).move_to(np.array([0,0,surface_func(0,0)])).scale(.3),
        *[i.animate.shift(np.array([0,0,surface_func(i.get_center()[0],i.get_center()[1])])) for i in grid],
        NSvg.animate.set_opacity(1),
        run_time=5)
        self.wait(5)
        grid_notes = VGroup(
            MTex("u_{i,j}^n",tex_to_color_map={"u":TEAL_B}).scale(.25).move_to(np.array([0,0,surface_func(0,0)])),
            MTex("u_{i-1,j}^{n}",tex_to_color_map={"u":TEAL_B}).scale(.25).move_to(np.array([-.5,0,surface_func(-.5,0)])),
            MTex("u_{i,j-1}^{n}",tex_to_color_map={"u":TEAL_B}).scale(.25).move_to(np.array([0,-.5,surface_func(0,-.5)])),
            MTex("u_{i+1,j}^{n}",tex_to_color_map={"u":TEAL_B}).scale(.25).move_to(np.array([.5,0,surface_func(.5,0)])),
            MTex("u_{i,j+1}^{n}",tex_to_color_map={"u":TEAL_B}).scale(.25).move_to(np.array([0,.5,surface_func(0,.5)])),
        )
        u_grid = TexText("$u$","网格").set_color_by_tex("$u$",TEAL_B).to_edge(DOWN,buff=1).fix_in_frame()
        self.play(FadeIn(u_grid))
        self.play(Write(grid_notes[0]))
        self.wait(5)
        self.play(Write(grid_notes[1:]))
        par_deri_x = MTex(
            r"{\partial u\over\partial x}\approx {u^n_{i,j}-u^n_{i-1,j}\over \Delta x}\left(\approx {u_{i+1,j}^n-u_{i-1,j}^n\over 2 \Delta x}\right)",
            tex_to_color_map={"u": TEAL_B, r"\Delta x": MAROON_B,"\partial x":WHITE}
        ).add_background_rectangle(opacity=.2).fix_in_frame()
        par_deri_y = MTex(
            r"{\partial u\over\partial y}\approx {u^n_{i,j}-u^n_{i,j-1}\over \Delta y}\left(\approx {u_{i,j+1}^n-u_{i,j-1}^n\over 2 \Delta y}\right)",
            tex_to_color_map={"u": TEAL_B, r"\Delta y": MAROON_B,"\partial y":WHITE}
        ).add_background_rectangle(opacity=.2).fix_in_frame()
        self.wait(5)
        self.play(Write(par_deri_x))
        self.wait(5)
        self.play(FadeTransform(par_deri_x, par_deri_y, key_map={r"\Delta x": r"\Delta y", r"\partial x": r"\partial y"}))
        self.wait(5)
        second_degree_deri = MTex(
            r"{\partial^2 u\over \partial x^2}\approx{u_{i+1,j}^n-2u_{i,j}^n+u_{i-1,j}^n\over\Delta x^2}",
            tex_to_color_map={"u": TEAL_B, r"\Delta x": MAROON_B}
        ).add_background_rectangle(opacity=.2).fix_in_frame()
        self.play(FadeTransform(par_deri_y, second_degree_deri, key_map={r"\Delta x": r"\Delta x^2"}))
        self.wait(5)
        self.play(FadeOut(grid),FadeOut(second_degree_deri),frame.animate.restore(),FadeOut(u_grid),FadeOut(grid_notes))
        self.play(NSvg.animate.scale(2).center())
        self.wait(5)
class Discrete_equation2(Scene):
    def construct(self):
        NSu = MTex(
            r"{\partial {u} \over \partial t} + {u} {\partial {u} \over \partial x} + {v} {\partial {u} \over \partial y} = -{1 \over \rho} {\partial {p} \over \partial x}+\nu \left({\partial^2 {u} \over \partial x^2} + {\partial^2 {u} \over \partial y^2} \right)",
            tex_to_color_map={
                r"{u}": TEAL_B,
                r"{v}": TEAL_D,
                r"{p}": ORANGE,
                r"\nu": YELLOW,
                r"\rho": RED,
            },
        ).next_to(ORIGIN, UP)
        NSv = MTex(
            r"{\partial {v} \over \partial t} + {u} {\partial {v} \over \partial x} + {v} {\partial {v} \over \partial y} = -{1 \over \rho} {\partial {p} \over \partial y}+\nu \left({\partial^2 {v} \over \partial x^2} + {\partial^2 {v} \over \partial y^2} \right)",
            tex_to_color_map={
                r"{u}": TEAL_B,
                r"{v}": TEAL_D,
                r"{p}": ORANGE,
                r"\nu": YELLOW,
                r"\rho": RED,
            },
        ).next_to(ORIGIN, DOWN)
        NSvg = VGroup(NSu, NSv)
        self.add(NSvg)
        NSu_dis = MTex(
            r"{ {u}_{i,j}^{n+1}-{u}_{i,j}^{n} \over \Delta t}+{u}_{i,j}^{n}{ {u}_{i,j}^{n}-{u}_{i-1,j}^{n} \over \Delta x}+{v}_{i,j}^{n}{ {u}_{i,j}^{n}-{u}_{i,j-1}^{n} \over \Delta y} = -{1 \over \rho}{ {p}_{i+1,j}^{n}-{p}_{i-1,j}^{n} \over 2 \Delta x}+\nu\left({ {u}_{i+1,j}^{n}-2{u}_{i,j}^{n}+{u}_{i-1,j}^{n} \over \Delta x^2}+{ {u}_{i,j+1}^{n}-2{u}_{i,j}^{n}+{u}_{i,j-1}^{n} \over \Delta y^2}\right)",
            tex_to_color_map={"{u}": TEAL_B,"{v}":TEAL_D, "{p}": ORANGE, r"\nu": YELLOW,r"\rho": RED,"\Delta t":MAROON_B,"\Delta x":MAROON_B,"\Delta y":MAROON_B},
        ).scale(.5).next_to(ORIGIN,UP)
        NSv_dis = MTex(
            r"{ {v}_{i,j}^{n+1}-{v}_{i,j}^{n} \over \Delta t}+{u}_{i,j}^{n}{ {v}_{i,j}^{n}-{v}_{i-1,j}^{n} \over \Delta x}+{v}_{i,j}^{n}{ {v}_{i,j}^{n}-{v}_{i,j-1}^{n} \over \Delta y} = -{1 \over \rho}{ {p}_{i,j+1}^{n}-{p}_{i,j-1}^{n} \over 2 \Delta y}+\nu\left({ {v}_{i+1,j}^{n}-2{v}_{i,j}^{n}+{v}_{i-1,j}^{n} \over \Delta x^2}+{ {v}_{i,j+1}^{n}-2{v}_{i,j}^{n}+{v}_{i,j-1}^{n} \over \Delta y^2}\right)",
            tex_to_color_map={"{u}": TEAL_B,"{v}":TEAL_D, "{p}": ORANGE, r"\nu": YELLOW,r"\rho": RED,"\Delta t":MAROON_B,"\Delta x":MAROON_B,"\Delta y":MAROON_B},
        ).scale(.5).next_to(ORIGIN,DOWN)
        self.play(TransformMatchingMTex(NSu, NSu_dis),TransformMatchingMTex(NSv, NSv_dis))
        self.wait(5)
        NSu_sol = MTex(
            r"{u}_{i,j}^{n+1}={u}_{i,j}^{n}+\Delta t\left[-{u}_{i,j}^{n}{ {u}_{i,j}^{n}-{u}_{i-1,j}^{n} \over \Delta x}-{v}_{i,j}^{n}{ {u}_{i,j}^{n}-{u}_{i,j-1}^{n} \over \Delta y}-{1 \over \rho}{ {p}_{i+1,j}^{n}-{p}_{i-1,j}^{n} \over 2 \Delta x}+\nu\left({ {u}_{i+1,j}^{n}-2{u}_{i,j}^{n}+{u}_{i-1,j}^{n} \over \Delta x^2}+{ {u}_{i,j+1}^{n}-2{u}_{i,j}^{n}+{u}_{i,j-1}^{n} \over \Delta y^2}\right)\right]",
            tex_to_color_map={"{u}": TEAL_B,"{v}":TEAL_D, "{p}": ORANGE, r"\nu": YELLOW,r"\rho": RED,"\Delta t":MAROON_B,"\Delta x":MAROON_B,"\Delta y":MAROON_B},
        ).scale(.5).next_to(ORIGIN,UP)
        NSv_sol = MTex(
            r"{v}_{i,j}^{n+1}={v}_{i,j}^{n}+\Delta t\left[-{u}_{i,j}^{n}{ {v}_{i,j}^{n}-{v}_{i-1,j}^{n} \over \Delta x}-{v}_{i,j}^{n}{ {v}_{i,j}^{n}-{v}_{i,j-1}^{n} \over \Delta y}-{1 \over \rho}{ {p}_{i,j+1}^{n}-{p}_{i,j-1}^{n} \over 2 \Delta y}+\nu\left({ {v}_{i+1,j}^{n}-2{v}_{i,j}^{n}+{v}_{i-1,j}^{n} \over \Delta x^2}+{ {v}_{i,j+1}^{n}-2{v}_{i,j}^{n}+{v}_{i,j-1}^{n} \over \Delta y^2}\right)\right]",
            tex_to_color_map={"{u}": TEAL_B,"{v}":TEAL_D, "{p}": ORANGE, r"\nu": YELLOW,r"\rho": RED,"\Delta t":MAROON_B,"\Delta x":MAROON_B,"\Delta y":MAROON_B},
        ).scale(.5).next_to(ORIGIN,DOWN)
        self.play(TransformMatchingMTex(NSu_dis, NSu_sol),TransformMatchingMTex(NSv_dis, NSv_sol))
        NSvg = VGroup(NSu_sol,NSv_sol)
        self.play(NSvg.animate.scale(.5).arrange(DOWN).to_edge(UL))
        self.wait(5)
        p1 = MTex(r"\nabla \cdot \boldsymbol v = 0",tex_to_color_map={r"\boldsymbol v": TEAL},
        isolate=["=","-",r"\nabla"],use_plain_tex=True)
        p2 = MTex(r"{\Delta t\over\rho}\nabla^2 {p}=-\nabla\cdot \boldsymbol v",tex_to_color_map={r"\boldsymbol v": TEAL,r"\rho":RED,"{p}":ORANGE,"\Delta t":MAROON},
            isolate=["=","-",r"\nabla"],use_plain_tex=True)
        self.play(Write(p1))
        self.wait()
        self.play(TransformMatchingMTex(p1, p2))
        p3 = MTex(r"{ {p}_{i+1,j}^{n}-2{p}_{i,j}^{n}+{p}_{i-1,j}^{n}\over\Delta x^2}+{ {p}_{i,j+1}^{n}-2{p}_{i,j}^{n}+{p}_{i,j-1}^{n}\over\Delta y^2} = {\rho\over\Delta t}\left({ {u}_{i+1,j}^{n}-{u}_{i-1,j}^{n}\over2\Delta x}+{ {v}_{i,j+1}^{n}-{v}_{i,j-1}^{n}\over2\Delta y}\right)",
            tex_to_color_map={"{u}": TEAL_B,"{v}":TEAL_D, "{p}": ORANGE, r"\nu": YELLOW,r"\rho": RED,"\Delta t":MAROON_B,"\Delta x":MAROON_B,"\Delta y":MAROON_B},
        ).scale(.5)
        self.wait()
        self.play(TransformMatchingMTex(p2, p3))
        p4 = MTex(
            r"{p}_{i,j}^{n}={\left({p}_{i+1,j}^{n}+{p}_{i-1,j}^{n}\right)\Delta y^2+\left({p}_{i,j+1}^{n}+{p}_{i,j-1}^{n}\right)\Delta x^2-{\rho\over\Delta t}\left({ {u}_{i+1,j}^{n}-{u}_{i-1,j}^{n}\over2\Delta x}+{ {v}_{i,j+1}^{n}-{v}_{i,j-1}^{n}\over2\Delta y}\right)\Delta x^2\Delta y^2\over2(\Delta x^2+\Delta y^2)}",
            tex_to_color_map={"{u}": TEAL_B,"{v}":TEAL_D, "{p}": ORANGE, r"\nu": YELLOW,r"\rho": RED,"\Delta t":MAROON_B,"\Delta x":MAROON_B,"\Delta y":MAROON_B},
        ).scale(.5)
        self.wait()
        self.play(TransformMatchingMTex(p3, p4))
        self.wait()
        get_n = p4.get_parts_by_tex(r"^{n}")[:-4]
        self.play(LaggedStart(*[FlashAround(i) for i in get_n]))
        self.wait()
        NSvg.add(p4)        
        self.play(p4.animate.scale(.5).next_to(NSvg[1],DOWN).to_edge(LEFT))
        cover_rec = SurroundingRectangle(NSvg).set_fill(BLACK,0.5).set_stroke(width=0)
        self.play(FadeIn(cover_rec))
        grid_of_points = Square(1).get_grid(4,4,4,buff=0)
        labels = VGroup(*[Tex("a_{"+str(i%4)+","+str(i//4)+"}",isolate=["a"],tex_to_color_map={"a":BLUE}).scale(.5).move_to(grid_of_points[(3-i//4)*4+i%4]) for i in range(16)])
        self.wait()
        self.play(FadeIn(grid_of_points,shift=DOWN*.1,lag_ratio=.05),FadeIn(labels,shift=UP*.1,lag_ratio=.05))
        grid_and_labels = VGroup(grid_of_points,labels)
        self.wait()
        self.play(grid_and_labels.animate.shift(LEFT*3))
        already_known = VGroup(*[Integer(random.randint(0,2)).scale(.5).move_to(grid_of_points[i]) for i in [12,13,14,15,8,11,4,7,0,1,2,3,]])

        formula = MTex(r"a_{i,j}={1\over4}(a_{i-1,j}+a_{i+1,j}+a_{i,j-1}+a_{i,j+1})",tex_to_color_map={"a":BLUE},isolate=["+"],use_plain_tex=True).move_to(RIGHT*3).scale(.5)
        self.wait()
        self.play(Write(formula))
        anim_group = AnimationGroup(*[FadeTransform(labels[j],already_known[i]) for i,j in zip(range(12),[0,1,2,3,4,7,8,11,12,13,14,15])],)
        self.wait()
        self.play(anim_group)
        formulas = VGroup(
            MTex("a_{1,1}={1\over4}(a_{1,2}+a_{2,1}+1+2)",tex_to_color_map={"a":BLUE},isolate=["+"],use_plain_tex=True),
            MTex("a_{2,1}={1\over4}(a_{1,1}+a_{2,2}+1+1)",tex_to_color_map={"a":BLUE},isolate=["+"],use_plain_tex=True),
            MTex("a_{1,2}={1\over4}(a_{1,1}+a_{2,2}+0+1)",tex_to_color_map={"a":BLUE},isolate=["+"],use_plain_tex=True),
            MTex("a_{2,2}={1\over4}(a_{1,2}+a_{2,1}+1+2)",tex_to_color_map={"a":BLUE},isolate=["+"],use_plain_tex=True),
        ).scale(.5).arrange(DOWN).move_to(RIGHT*3)
        self.wait()
        self.remove(formula)
        self.play(LaggedStart(*[TransformMatchingMTex(formula.copy(),i) for i in formulas]))
        brace = Brace(formulas,LEFT)
        self.play(Write(brace))
        formulas.add(brace)
        self.wait()
        self.play(grid_and_labels.animate.set_opacity(0),FadeOut(already_known),formulas.animate.shift(LEFT*6))
        formulas_in_matrix = VGroup(
            IntegerMatrix([[-4,1,1,0],[1,-4,0,1],[1,0,-4,1],[0,1,1,-4]]),
            Matrix([
                ["a_{1,1}"],
                ["a_{2,1}"],
                ["a_{1,2}"],
                ["a_{2,2}"]
            ]),
            Tex("="),
            IntegerMatrix([[-3],[-1],[-2],[-3]]),
        ).scale(.5).arrange(RIGHT,buff=0.1).shift(RIGHT*3)
        for i in range(4):
            formulas_in_matrix[1].elements[i][0][0].set_color(BLUE)
        self.wait()
        self.play(Write(formulas_in_matrix))
        self.wait()
        answers = VGroup(
            MTex("a_{1,1}={5\over4}",tex_to_color_map={"a":BLUE}),
            MTex("a_{2,1}={7\over8}",tex_to_color_map={"a":BLUE}),
            MTex("a_{1,2}={9\over8}",tex_to_color_map={"a":BLUE}),
            MTex("a_{2,2}={5\over4}",tex_to_color_map={"a":BLUE}),
        ).scale(.5).arrange(DOWN).move_to(RIGHT*3)        
        self.play(FadeOut(formulas_in_matrix,shift=LEFT),FadeIn(answers,shift=LEFT))
        iteration_vg = VGroup(
            VGroup(Tex("a_{1,1}",tex_to_color_map={"a":BLUE}),Tex("="),DecimalNumber(0,num_decimal_places=4)).arrange(RIGHT,buff=0.2),
            VGroup(Tex("a_{2,1}",tex_to_color_map={"a":BLUE}),Tex("="),DecimalNumber(0,num_decimal_places=4)).arrange(RIGHT,buff=0.2),
            VGroup(Tex("a_{1,2}",tex_to_color_map={"a":BLUE}),Tex("="),DecimalNumber(0,num_decimal_places=4)).arrange(RIGHT,buff=0.2),
            VGroup(Tex("a_{2,2}",tex_to_color_map={"a":BLUE}),Tex("="),DecimalNumber(0,num_decimal_places=4)).arrange(RIGHT,buff=0.2),
        ).scale(.5).arrange(DOWN,buff=0.2).move_to(RIGHT*3)
        self.wait()
        self.play(answers.animate.scale(.5).arrange(RIGHT).to_corner(UR))
        self.wait()
        self.play(Write(iteration_vg))
        a11 = ValueTracker(0)
        a21 = ValueTracker(0)
        a12 = ValueTracker(0)
        a22 = ValueTracker(0)
        def update_interation(m):
            m[0][2].set_value(a11.get_value())#.next_to(m[0][1],RIGHT,buff=0.1)
            m[1][2].set_value(a21.get_value())#.next_to(m[1][1],RIGHT,buff=0.1)
            m[2][2].set_value(a12.get_value())#.next_to(m[2][1],RIGHT,buff=0.1)
            m[3][2].set_value(a22.get_value())#.next_to(m[3][1],RIGHT,buff=0.1)
        iteration_vg.add_updater(update_interation)
        put_in = VGroup(
            Line(iteration_vg[0][0].get_left(),formulas[1].get_parts_by_tex("a_{1,1}")[0].get_center()),
            Line(iteration_vg[0][0].get_left(),formulas[2].get_parts_by_tex("a_{1,1}")[0].get_center()),
            Line(iteration_vg[1][0].get_left(),formulas[0].get_parts_by_tex("a_{2,1}")[0].get_center()),
            Line(iteration_vg[1][0].get_left(),formulas[3].get_parts_by_tex("a_{2,1}")[0].get_center()),
            Line(iteration_vg[2][0].get_left(),formulas[0].get_parts_by_tex("a_{1,2}")[0].get_center()),
            Line(iteration_vg[2][0].get_left(),formulas[3].get_parts_by_tex("a_{1,2}")[0].get_center()),
            Line(iteration_vg[3][0].get_left(),formulas[1].get_parts_by_tex("a_{2,2}")[0].get_center()),
            Line(iteration_vg[3][0].get_left(),formulas[2].get_parts_by_tex("a_{2,2}")[0].get_center()),
        ).set_color(YELLOW)
        put_out = VGroup(
            Line(formulas[0].get_parts_by_tex("a_{1,1}")[0].get_center(),iteration_vg[0][0].get_left()),
            Line(formulas[1].get_parts_by_tex("a_{2,1}")[0].get_center(),iteration_vg[1][0].get_left()),
            Line(formulas[2].get_parts_by_tex("a_{1,2}")[0].get_center(),iteration_vg[2][0].get_left()),
            Line(formulas[3].get_parts_by_tex("a_{2,2}")[0].get_center(),iteration_vg[3][0].get_left()),
        ).set_color(YELLOW)
        self.wait()
        for i in range(15):   
            self.play(
                LaggedStart(*[ShowPassingFlash(i,time_width=.6) for i in put_in]),
            )
            self.play(
                LaggedStart(*[ShowPassingFlash(i,time_width=.6) for i in put_out]),
            )
            self.play(
                a11.animate.set_value((a21.get_value()+a12.get_value()+1+2)/4),
                a21.animate.set_value((a11.get_value()+a22.get_value()+0+1)/4),
                a12.animate.set_value((a11.get_value()+a22.get_value()+1+1)/4),
                a22.animate.set_value((a21.get_value()+a12.get_value()+1+2)/4),
            )
        
        self.wait()
        self.play(answers.animate.scale(2).arrange(DOWN).move_to(RIGHT*2))
        self.play(LaggedStart(*[FadeOut(i[0]) for i in iteration_vg]),LaggedStart(*[i[1:].animate.next_to(j,buff=0.1).set_y(j.get_part_by_tex("a").get_y()) for i,j in zip(iteration_vg,answers)]))
        self.wait()
        rec = FullScreenRectangle().set_fill(BLACK,1)
        self.add(rec,NSvg,cover_rec)
        self.play(FadeIn(rec))
        self.wait()
        self.play(FadeOut(cover_rec))
        self.play(p4.animate.scale(2).center())

class Discrete_equation3(Scene):
    def construct(self):
        NSu_sol = MTex(
            r"{u}_{i,j}^{n+1}={u}_{i,j}^{n}+\Delta t\left[-{u}_{i,j}^{n}{ {u}_{i,j}^{n}-{u}_{i-1,j}^{n} \over \Delta x}-{v}_{i,j}^{n}{ {u}_{i,j}^{n}-{u}_{i,j-1}^{n} \over \Delta y}-{1 \over \rho}{ {p}_{i+1,j}^{n}-{p}_{i-1,j}^{n} \over 2 \Delta x}+\nu\left({ {u}_{i+1,j}^{n}-2{u}_{i,j}^{n}+{u}_{i-1,j}^{n} \over \Delta x^2}+{ {u}_{i,j+1}^{n}-2{u}_{i,j}^{n}+{u}_{i,j-1}^{n} \over \Delta y^2}\right)\right]",
            tex_to_color_map={"{u}": TEAL_B,"{v}":TEAL_D, "{p}": ORANGE, r"\nu": YELLOW,r"\rho": RED,"\Delta t":MAROON_B,"\Delta x":MAROON_B,"\Delta y":MAROON_B},
        )
        NSv_sol = MTex(
            r"{v}_{i,j}^{n+1}={v}_{i,j}^{n}+\Delta t\left[-{u}_{i,j}^{n}{ {v}_{i,j}^{n}-{v}_{i-1,j}^{n} \over \Delta x}-{v}_{i,j}^{n}{ {v}_{i,j}^{n}-{v}_{i,j-1}^{n} \over \Delta y}-{1 \over \rho}{ {p}_{i,j+1}^{n}-{p}_{i,j-1}^{n} \over 2 \Delta y}+\nu\left({ {v}_{i+1,j}^{n}-2{v}_{i,j}^{n}+{v}_{i-1,j}^{n} \over \Delta x^2}+{ {v}_{i,j+1}^{n}-2{v}_{i,j}^{n}+{v}_{i,j-1}^{n} \over \Delta y^2}\right)\right]",
            tex_to_color_map={"{u}": TEAL_B,"{v}":TEAL_D, "{p}": ORANGE, r"\nu": YELLOW,r"\rho": RED,"\Delta t":MAROON_B,"\Delta x":MAROON_B,"\Delta y":MAROON_B},
        )
        NSvg = VGroup(NSu_sol,NSv_sol).scale(.25).arrange(DOWN).to_corner(UL)
        p = MTex(
            r"{p}_{i,j}^{n}={\left({p}_{i+1,j}^{n}+{p}_{i-1,j}^{n}\right)\Delta y^2+\left({p}_{i,j+1}^{n}+{p}_{i,j-1}^{n}\right)\Delta x^2-{\rho\over\Delta t}\left({ {u}_{i+1,j}^{n}-{u}_{i-1,j}^{n}\over2\Delta x}+{ {v}_{i,j+1}^{n}-{v}_{i,j-1}^{n}\over2\Delta y}\right)\Delta x^2\Delta y^2\over2(\Delta x^2+\Delta y^2)}",
            tex_to_color_map={"{u}": TEAL_B,"{v}":TEAL_D, "{p}": ORANGE, r"\nu": YELLOW,r"\rho": RED,"\Delta t":MAROON_B,"\Delta x":MAROON_B,"\Delta y":MAROON_B},
        ).scale(.5)
        self.add(NSvg,p)
        self.wait()

        loop_1 = TexText("循环100次：").scale(.5).next_to(p,UP,aligned_edge=LEFT).shift(LEFT)
        bound_1 = TexText("代入边界条件。").scale(.5).next_to(p,DOWN,aligned_edge=LEFT)
        loop_2 = TexText("循环：").scale(.5).next_to(loop_1,UP,aligned_edge=LEFT).shift(LEFT)
        self.play(Write(loop_1),Write(bound_1))
        self.wait()
        self.play(NSvg.animate.scale(2).arrange(DOWN).next_to(bound_1,DOWN,aligned_edge=LEFT).shift(LEFT))
        bound_2 = TexText("代入边界条件。").scale(.5).next_to(NSvg,DOWN,aligned_edge=LEFT)
        self.play(Write(bound_2))
        self.play(Write(loop_2))
        loop_1_bound = SurroundingRectangle(VGroup(loop_1,p,bound_1)).set_fill(WHITE,.3).set_stroke(WHITE,5)
        loop_2_bound = SurroundingRectangle(VGroup(loop_2,NSvg,bound_2)).set_fill(WHITE,.3).set_stroke(WHITE,5)
        
        vg=VGroup(loop_2_bound,loop_1_bound,loop_1,loop_2,bound_1,NSvg,p,bound_2)
        self.add(*vg)
        self.play(ShowCreation(loop_1_bound),ShowCreation(loop_2_bound))
        self.play(vg.animate.set_width(14).center())
        self.wait(5)
        self.play(FadeOut(vg))
        self.wait()

class Python_Code(Scene):
    def construct(self):
        grid = SGroup(
            *[SGroup(*[Square3D(side_length=8/9-.1) for i in range(16)]).arrange(RIGHT,buff=0.1) for i in range(9)]
        ).arrange(UP,buff=0.1)
        self.play(FadeIn(grid))
        sides = SGroup(
            grid[0],SGroup(*[grid[i][-1] for i in range(1,9)]),SGroup(*[grid[-1][-i] for i in range(2,16)]),SGroup(*[grid[-i][0] for i in range(1,10)])
        )
        centers = SGroup(
            *[grid[i][1:-1] for i in range(1,8)]
        )
        self.wait()
        self.play(LaggedStart(*[
            LaggedStart(*[
                Indicate(i,color=WHITE,scale_factor=1.1) for i in j
            ]) for j in centers
        ]))
        self.wait()
        self.play(LaggedStart(*[Indicate(i,color=WHITE,scale_factor=1.1) for j in sides for i in j]))
        code_for_p0 = Code("self.p[1:-1, 1:-1]")
        self.wait()
        self.play(*[i.animate.set_color(GREY_D) for j in centers for i in j])
        self.wait()
        self.play(FadeOut(grid))
        self.wait()
        self.play(Write(code_for_p0))
        p_text = """
self.p[1:-1, 1:-1] = ((self.p[1:-1, 2:] + self.p[1:-1, :-2]) * self.dy**2 
                  + (self.p[2:, 1:-1] + self.p[:-2, 1:-1]) * self.dx**2 
                  - self.rho  / self.dt * (
                                        (self.u[1:-1, 2:] - self.u[1:-1, :-2]) / (2 * self.dx) 
                                      + (self.v[2:, 1:-1] - self.v[:-2, 1:-1]) / (2 * self.dy)
                                  ) * self.dx**2 * self.dy**2
                  ) / (2 * (self.dx**2 + self.dy**2)) 
        """
        code_for_p = Code(p_text[1:])
        
        self.wait()
        self.play(TransformMatchingShapes(code_for_p0,code_for_p))
        p = MTex(
            r"{p}_{i,j}^{n}={\left({p}_{i+1,j}^{n}+{p}_{i-1,j}^{n}\right)\Delta y^2+\left({p}_{i,j+1}^{n}+{p}_{i,j-1}^{n}\right)\Delta x^2-{\rho\over\Delta t}\left({ {u}_{i+1,j}^{n}-{u}_{i-1,j}^{n}\over2\Delta x}+{ {v}_{i,j+1}^{n}-{v}_{i,j-1}^{n}\over2\Delta y}\right)\Delta x^2\Delta y^2\over2(\Delta x^2+\Delta y^2)}",
            tex_to_color_map={"{u}": TEAL_B,"{v}":TEAL_D, "{p}": ORANGE, r"\nu": YELLOW,r"\rho": RED,"\Delta t":MAROON_B,"\Delta x":MAROON_B,"\Delta y":MAROON_B},
        ).scale(.5).to_edge(DOWN)
        self.play(FadeIn(p))
        self.wait()
        p_text_2 = """
for _ in np.arange(100):
    self.p[1:-1, 1:-1] = ((self.p[1:-1, 2:] + self.p[1:-1, :-2]) * self.dy**2 
                      + (self.p[2:, 1:-1] + self.p[:-2, 1:-1]) * self.dx**2 
                      - self.rho  / self.dt * (
                                            (self.u[1:-1, 2:] - self.u[1:-1, :-2]) / (2 * self.dx) 
                                          + (self.v[2:, 1:-1] - self.v[:-2, 1:-1]) / (2 * self.dy)
                                      ) * self.dx**2 * self.dy**2
                      ) / (2 * (self.dx**2 + self.dy**2)) 
    self.pressure_bounary_condition()
        """
        code_for_p_2 = Code(p_text_2[1:])
        self.play(FadeTransform(code_for_p,code_for_p_2[29:-38-4]),Write(code_for_p_2[:29]),Write(code_for_p_2[-38-4:]))
        self.wait()
        code_for_p_3 = Code("self.pressure_poisson()")
        self.play(FadeTransform(code_for_p_2,code_for_p_3))
        self.play(FadeOut(p))
        uv_text_0 = """
self.pressure_poisson()

self.u[1:-1, 1:-1] = self.u[1:-1, 1:-1] + self.dt * (
    - self.u[1:-1, 1:-1] / self.dx *
    (self.u[1:-1, 1:-1] - self.u[1:-1, 0:-2]) -
    self.v[1:-1, 1:-1] / self.dy *
    (self.u[1:-1, 1:-1] - self.u[:-2, 1:-1]) -
    (self.p[1:-1, 2:] - self.p[1:-1, :-2]) / (2 * self.rho * self.dx) +
    self.nu * (
        (self.u[1:-1, 2:] - 2 * self.u[1:-1, 1:-1] + self.u[1:-1, :-2]) / self.dx**2 +
        (self.u[2:, 1:-1] - 2 * self.u[1:-1, 1:-1] + self.u[:-2, 1:-1]) / self.dy**2)
)
"""
        uv_text_1 = """
self.v[1:-1, 1:-1] = self.v[1:-1, 1:-1] + self.dt * (
    - self.u[1:-1, 1:-1] / self.dx *
    (self.v[1:-1, 1:-1] - self.v[1:-1, :-2]) -
    self.v[1:-1, 1:-1] / self.dy *
    (self.v[1:-1, 1:-1] - self.v[:-2, 1:-1]) -
    (self.p[2:, 1:-1] - self.p[0:-2, 1:-1]) / (2 * self.rho * self.dy) +
    self.nu * (
        (self.v[1:-1, 2:] - 2 * self.v[1:-1, 1:-1] + self.v[1:-1, :-2]) / self.dx**2 +
        (self.v[2:, 1:-1] - 2 * self.v[1:-1, 1:-1] + self.v[:-2, 1:-1])/self.dy**2
))

self.flow_boundary_condition()
"""         
        code_for_uv_0 = Code(uv_text_0[1:])
        self.play(FadeTransform(code_for_p_3,code_for_uv_0[:23]),Write(code_for_uv_0[23:]))
        code_for_uv_1 = Code(uv_text_1[1:]).next_to(code_for_uv_0,DOWN,0.5,LEFT)
        self.play(Write(code_for_uv_1),self.camera.frame.animate.move_to(code_for_uv_1))
        all_code = VGroup(*code_for_uv_0,*code_for_uv_1)
        self.wait()
        self.play(all_code.animate.set_height(7.9).center(),self.camera.frame.animate.center())
        self.wait()
class Final(Scene):
    def construct(self):
        uv_text_0 = """
self.pressure_poisson()

self.u[1:-1, 1:-1] = self.u[1:-1, 1:-1] + self.dt * (
    - self.u[1:-1, 1:-1] / self.dx *
    (self.u[1:-1, 1:-1] - self.u[1:-1, 0:-2]) -
    self.v[1:-1, 1:-1] / self.dy *
    (self.u[1:-1, 1:-1] - self.u[:-2, 1:-1]) -
    (self.p[1:-1, 2:] - self.p[1:-1, :-2]) / (2 * self.rho * self.dx) +
    self.nu * (
        (self.u[1:-1, 2:] - 2 * self.u[1:-1, 1:-1] + self.u[1:-1, :-2]) / self.dx**2 +
        (self.u[2:, 1:-1] - 2 * self.u[1:-1, 1:-1] + self.u[:-2, 1:-1]) / self.dy**2)
)
"""
        uv_text_1 = """
self.v[1:-1, 1:-1] = self.v[1:-1, 1:-1] + self.dt * (
    - self.u[1:-1, 1:-1] / self.dx *
    (self.v[1:-1, 1:-1] - self.v[1:-1, :-2]) -
    self.v[1:-1, 1:-1] / self.dy *
    (self.v[1:-1, 1:-1] - self.v[:-2, 1:-1]) -
    (self.p[2:, 1:-1] - self.p[0:-2, 1:-1]) / (2 * self.rho * self.dy) +
    self.nu * (
        (self.v[1:-1, 2:] - 2 * self.v[1:-1, 1:-1] + self.v[1:-1, :-2]) / self.dx**2 +
        (self.v[2:, 1:-1] - 2 * self.v[1:-1, 1:-1] + self.v[:-2, 1:-1])/self.dy**2
))

self.flow_boundary_condition()
"""         
        code_for_uv_0 = Code(uv_text_0[1:])
        code_for_uv_1 = Code(uv_text_1[1:]).next_to(code_for_uv_0,DOWN,0.5,LEFT)
        all_code = VGroup(*code_for_uv_0,*code_for_uv_1)
        all_code.set_height(7.9).center()
        fluid = Abstract_Flow_Field([-FRAME_X_RADIUS*1.1,FRAME_X_RADIUS*1.1],[-FRAME_Y_RADIUS*1.1,FRAME_Y_RADIUS*1.1],x_num=20*16,y_num=20*9)
        all_code.add_updater(fluid.shifts)
        self.add(all_code)
        self.wait(30)
class test_decimal(Scene):
    def construct(self):
        self.play(ShowPassingFlash(Line().set_stroke(color=YELLOW),run_time=5,time_width=.6))



class report_bug3(Scene):
    def construct(self):
        mtex = MTex(
            r"{\partial {u} \over \partial t} + {u} {\partial {u} \over \partial x} + {v} {\partial {u} \over \partial y} = -{1 \over \rho} {\partial {p} \over \partial x}+\nu \left({\partial^2 {u} \over \partial x^2} + {\partial^2 {u} \over \partial y^2} \right)",
            isolate=[r"\right)"]
        )
        self.add(mtex)
