import sys
sys.path.append('/Users/linus/Desktop/less-is-more/3b1b_anaconda_install/manim/3b1b-videos-master')

from manim_imports_ext import *
import scipy.spatial

# 库的版本更新后，一些可视化效果有变化

# Helpers
def project_to_xy_plane(p1, p2):
    """
    Draw a line from source to p1 to p2.  Where does it
    intersect the xy plane?
    """
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    if z2 < z1:
        z2 = z1 + 1e-2  # TODO, bad hack
    vect = p2 - p1
    return p1 - (z2 / vect[2]) * vect


def flat_project(point):
    # return [*point[:2], 0]
    return [*point[:2], 0.05 * point[2]]  # TODO


def get_pre_shadow(mobject, opacity):
    result = mobject.deepcopy()
    if isinstance(result, Group) and all((isinstance(sm, VMobject) for sm in mobject)):
        result = VGroup(*result)
    result.clear_updaters()

    for sm in result.family_members_with_points():
        color = interpolate_color(sm.get_color(), BLACK, opacity)
        sm.set_color(color)
        sm.set_opacity(opacity)
        if isinstance(sm, VMobject):
            sm.set_stroke(
                interpolate_color(sm.get_stroke_color(), BLACK, opacity)
            )
        sm.set_gloss(sm.get_gloss() * 0.5)
        sm.set_shadow(0)
        sm.set_reflectiveness(0)
    return result


def update_shadow(shadow, mobject, light_source):
    lp = light_source.get_center() if light_source is not None else None

    def project(point):
        if lp is None:
            return flat_project(point)
        else:
            return project_to_xy_plane(lp, point)

    for sm, mm in zip(shadow.family_members_with_points(), mobject.family_members_with_points()):
        sm.set_points(np.apply_along_axis(project, 1, mm.get_points()))
        if isinstance(sm, VMobject) and sm.get_unit_normal()[2] < 0:
            sm.reverse_points()
        if isinstance(sm, VMobject):
            sm.set_fill(opacity=mm.get_fill_opacity())
        else:
            sm.set_opacity(mm.get_opacity())


def get_shadow(mobject, light_source=None, opacity=0.7):
    shadow = get_pre_shadow(mobject, opacity)
    shadow.add_updater(lambda s: update_shadow(s, mobject, light_source))
    return shadow


def get_area(shadow):
    return 0.5 * sum(
        get_norm(sm.get_area_vector())
        for sm in shadow.get_family()
    )


def get_convex_hull(mobject):
    points = mobject.get_all_points()
    hull = scipy.spatial.ConvexHull(points[:, :2])
    return points[hull.vertices]


def sort_to_camera(mobject, camera_frame):
    cl = camera_frame.get_implied_camera_location()
    mobject.sort(lambda p: -get_norm(p - cl))
    return mobject


def cube_sdf(point, cube):
    c = cube.get_center()
    vect = point - c
    face_vects = [face.get_center() - c for face in cube]
    return max(*(
        abs(np.dot(fv, vect) / np.dot(fv, fv))
        for fv in face_vects
    )) - 1


def is_in_cube(point, cube):
    return cube_sdf(point, cube) < 0


def get_overline(mob):
    overline = Underline(mob).next_to(mob, UP, buff=0.05)
    overline.set_stroke(WHITE, 2)
    return overline


def get_key_result(solid_name, color=BLUE):
    eq = OldTex(
        "\\text{Area}\\big(\\text{Shadow}(\\text{" + solid_name + "})\\big)",
        "=",
        "\\frac{1}{2}", "{c}", "\\cdot",
        "(\\text{Surface area})",
        tex_to_color_map={
            "\\text{Shadow}": GREY_B,
            f"\\text{{{solid_name}}}": color,
            "\\text{Solid}": BLUE,
            "{c}": RED,
        }
    )
    eq.add_to_back(get_overline(eq[:5]))
    return eq


def get_surface_area(solid):
    return sum(get_norm(f.get_area_vector()) for f in solid)


# Scenes

class ShadowScene(ThreeDScene):
    object_center = [0, 0, 3]
    frame_center = [0, 0, 2]
    area_label_center = [0, -1.5, 0]
    surface_area = 6.0
    num_reorientations = 10
    plane_dims = (20, 20)
    plane_style = {
        "stroke_width": 0,
        "fill_color": GREY_A,
        "fill_opacity": 0.5,
        #"gloss": 0.5,
        #"shadow": 0.2,
    }
    limited_plane_extension = 0
    object_style = {
        "stroke_color": WHITE,
        "stroke_width": 0.5,
        "fill_color": BLUE_E,
        "fill_opacity": 0.7,
        #"reflectiveness": 0.3,
        #"gloss": 0.1,
        #"shadow": 0.5,
    }
    inf_light = False
    glow_radius = 10
    glow_factor = 10
    area_label_center = [-2, -1, 0]
    unit_size = 2

    def setup(self):
        self.camera.frame.reorient(-30, 75)
        self.camera.frame.move_to(self.frame_center)
        self.add_plane()
        self.add_solid()
        self.add_shadow()
        self.setup_light_source()

    def add_plane(self):
        width, height = self.plane_dims

        grid = NumberPlane(
            x_range=(-width // 2, width // 2, 2),
            y_range=(-height // 2, height // 2, 2),
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
            },
            faded_line_ratio=4,
        )
        grid.shift(-grid.get_origin())
        grid.set_width(width)
        grid.axes.match_style(grid.background_lines)
        grid.set_flat_stroke(True)
        grid.insert_n_curves(3)

        plane = Rectangle()
        plane.replace(grid, stretch=True)
        # 这一行会报错，可能版本更新了
        plane.set_style(**self.plane_style)
        plane.set_stroke(width=0)
        if self.limited_plane_extension > 0:
            plane.set_height(height // 2 + self.limited_plane_extension, about_edge=UP, stretch=True)
        self.plane = plane

        # plane.add(grid)
        # self.add(plane)
        self.add(grid)

    def add_solid(self):
        self.solid = self.get_solid()
        self.solid.move_to(self.object_center)
        self.add(self.solid)

    def get_solid(self):
        cube = VCube()
        cube.deactivate_depth_test()
        cube.set_height(2)
        # 又报错
        cube.set_style(**self.object_style)
        # Wrap in group so that strokes and fills
        # are rendered in separate passes
        cube = self.cube = Group(*cube)
        cube.add_updater(lambda m: self.sort_to_camera(m))
        return cube

    def add_shadow(self):
        light_source = None if self.inf_light else self.camera.light_source
        shadow = get_shadow(self.solid, light_source)

        self.add(shadow, self.solid)
        self.shadow = shadow

    def setup_light_source(self):
        self.light = self.camera.light_source
        if self.inf_light:
            self.light.move_to(100 * OUT)
        else:
            glow = self.glow = TrueDot(
                radius=self.glow_radius,
                glow_factor=self.glow_factor,
            )
            glow.set_color(interpolate_color(YELLOW, WHITE, 0.5))
            glow.add_updater(lambda m: m.move_to(self.light))
            self.add(glow)

    def sort_to_camera(self, mobject):
        return sort_to_camera(mobject, self.camera.frame)

    def get_shadow_area_label(self):
        text = OldTexText("Shadow area: ")
        decimal = DecimalNumber(100)

        label = VGroup(text, decimal)
        label.arrange(RIGHT)
        label.move_to(self.area_label_center - decimal.get_center())
        label.fix_in_frame()
        label.set_backstroke()
        decimal.add_updater(lambda d: d.set_value(
            get_area(self.shadow) / (self.unit_size**2)
        ).set_backstroke())
        return label

    def begin_ambient_rotation(self, mobject, speed=0.2, about_point=None, initial_axis=[1, 1, 1]):
        mobject.rot_axis = np.array(initial_axis)

        def update_mob(mob, dt):
            mob.rotate(speed * dt, mob.rot_axis, about_point=about_point)
            mob.rot_axis = rotate_vector(mob.rot_axis, speed * dt, OUT)
            return mob
        mobject.add_updater(update_mob)
        return mobject

    def get_shadow_outline(self, stroke_width=1):
        outline = VMobject()
        outline.set_stroke(WHITE, stroke_width)
        outline.add_updater(lambda m: m.set_points_as_corners(get_convex_hull(self.shadow)).close_path())
        return outline

    def get_light_lines(self, outline=None, n_lines=100, only_vertices=False):
        if outline is None:
            outline = self.get_shadow_outline()

        def update_lines(lines):
            lp = self.light.get_center()
            if only_vertices:
                points = outline.get_vertices()
            else:
                points = [outline.pfp(a) for a in np.linspace(0, 1, n_lines)]
            for line, point in zip(lines, points):
                if self.inf_light:
                    line.set_points_as_corners([point + 10 * OUT, point])
                else:
                    line.set_points_as_corners([lp, point])

        line = Line(IN, OUT)
        light_lines = line.replicate(n_lines)
        light_lines.set_stroke(YELLOW, 0.5, 0.1)
        light_lines.add_updater(update_lines)
        return light_lines

    def random_toss(self, mobject=None, angle=TAU, about_point=None, meta_speed=5, **kwargs):
        if mobject is None:
            mobject = self.solid

        mobject.rot_axis = normalize(np.random.random(3))
        mobject.rot_time = 0

        def update(mob, time):
            dt = time - mob.rot_time
            mob.rot_time = time
            mob.rot_axis = rotate_vector(mob.rot_axis, meta_speed * dt, normalize(np.random.random(3)))
            mob.rotate(angle * dt, mob.rot_axis, about_point=about_point)

        self.play(
            UpdateFromAlphaFunc(mobject, update),
            **kwargs
        )

    def randomly_reorient(self, solid=None, about_point=None):
        solid = self.solid if solid is None else solid
        solid.rotate(
            random.uniform(0, TAU),
            axis=normalize(np.random.uniform(-1, 1, 3)),
            about_point=about_point,
        )
        return solid

    def init_frame_rotation(self, factor=0.0025, max_speed=0.01):
        frame = self.camera.frame
        frame.d_theta = 0

        def update_frame(frame, dt):
            frame.d_theta += -factor * frame.get_theta()
            frame.increment_theta(clip(
                factor * frame.d_theta,
                -max_speed * dt,
                max_speed * dt
            ))

        frame.add_updater(update_frame)
        return frame


class SimpleWriting(Scene):
    text = ""
    font = "Better Grade"
    color = WHITE
    font_size = 48

    def construct(self):
        words = Text(self.text, font=self.font, font_size=self.font_size)
        words.set_color(self.color)
        self.play(Write(words))
        self.wait()


class AliceName(SimpleWriting):
    text = "Alice"
    font_size = 72


class BobName(SimpleWriting):
    text = "Bob"
    font = "Kalam"


class BobWords(SimpleWriting):
    font = "Kalam"
    font_size = 24
    words1 = "Embraces calculations"
    words2 = "Loves specifics"

    def construct(self):
        words = VGroup(*(
            Text(text, font=self.font, font_size=self.font_size)
            for text in (self.words1, self.words2)
        ))
        words.arrange(DOWN)

        for word in words:
            self.play(Write(word))
            self.wait()


class AliceWords(BobWords):
    font = "Better Grade"
    words1 = "Procrastinates calculations"
    words2 = "Seeks generality"
    font_size = 48


class AskAboutConditions(SimpleWriting):
    text = "Which properties matter?"


class IntroduceShadow(ShadowScene):
    area_label_center = [-2.5, -2, 0]
    plane_dims = (28, 20)

    def construct(self):
        # Setup
        light = self.light
        light.move_to([0, 0, 20])
        self.add(light)
        cube = self.solid
        cube.scale(0.945)  # Hack to make the appropriate area 1
        shadow = self.shadow
        outline = self.get_shadow_outline()
        frame = self.camera.frame
        frame.add_updater(lambda f, dt: f.increment_theta(0.01 * dt))  # Ambient rotation
        area_label = self.get_shadow_area_label()
        light_lines = self.get_light_lines(outline)

        # Question
        question = OldTexText(
            "Puzzle: Find the average\\\\area of a cube's shadow",
            font_size=48,
        )
        question.to_corner(UL)
        question.fix_in_frame()
        subquestion = Text("(Averaged over all orientations)")
        subquestion.match_width(question)
        subquestion.next_to(question, DOWN, MED_LARGE_BUFF)
        subquestion.set_fill(BLUE_D)
        subquestion.fix_in_frame()
        subquestion.set_backstroke()

        # Introductory animations
        self.shadow.update()
        self.play(
            FadeIn(question, UP),
            *(
                LaggedStartMap(DrawBorderThenFill, mob, lag_ratio=0.1, run_time=3)
                for mob in (cube, shadow)
            )
        )
        self.random_toss(run_time=3, angle=TAU)

        # Change size and orientation
        outline.update()
        area_label.update()
        self.play(
            FadeIn(area_label),
            ShowCreation(outline),
        )
        self.play(
            cube.animate.scale(0.5),
            run_time=2,
            rate_func=there_and_back,
        )
        self.random_toss(run_time=2, angle=PI)
        self.wait()
        self.begin_ambient_rotation(cube)
        self.play(FadeIn(subquestion, 0.5 * DOWN))
        self.wait(7)

        # Where is the light?
        light_comment = Text("Where is the light?")
        light_comment.set_color(YELLOW)
        light_comment.to_corner(UR)
        light_comment.set_backstroke()
        light_comment.fix_in_frame()

        cube.clear_updaters()
        cube.add_updater(lambda m: self.sort_to_camera(cube))
        self.play(
            FadeIn(light_comment, 0.5 * UP),
            light.animate.next_to(cube, OUT, buff=1.5),
            run_time=2,
        )
        light_lines.update()
        self.play(
            ShowCreation(light_lines, lag_ratio=0.01, run_time=3),
        )
        self.play(
            light.animate.shift(1.0 * IN),
            rate_func=there_and_back,
            run_time=3
        )
        self.play(
            light.animate.shift(4 * RIGHT),
            run_time=5
        )
        self.play(
            Rotate(light, PI, about_point=light.get_z() * OUT),
            run_time=8,
        )
        self.play(light.animate.shift(4 * RIGHT), run_time=5)
        self.wait()

        # Light straight above
        # self.play(
        #     frame.animate.set_height(12).set_z(4),
        #     light.animate.set_z(10),
        #     run_time=3,
        # )
        # self.wait()
        # self.play(light.animate.move_to(75 * OUT), run_time=3)
        # self.wait()
        # self.play(
        #     frame.animate.set_height(8).set_z(2),
        #     LaggedStart(*map(FadeOut, (question, subquestion, light_comment))),
        #     run_time=2
        # )

        # Flat projection
        # verts = np.array([*cube[0].get_vertices(), *cube[5].get_vertices()])
        # vert_dots = DotCloud(verts)
        # vert_dots.set_glow_factor(0.5)
        # vert_dots.set_color(WHITE)
        # proj_dots = vert_dots.copy()
        # proj_dots.apply_function(flat_project)
        # proj_dots.set_color(GREY_B)
        # vert_proj_lines = VGroup(*(
        #     DashedLine(*pair)
        #     for pair in zip(verts, proj_dots.get_points())
        # ))
        # vert_proj_lines.set_stroke(WHITE, 1, 0.5)

        # point = verts[np.argmax(verts[:, 0])]
        # xyz_label = OldTex("(x, y, z)")
        # xy0_label = OldTex("(x, y, 0)")
        # for label in xyz_label, xy0_label:
        #     label.rotate(PI / 2, RIGHT)
        #     label.set_backstroke()
        # xyz_label.next_to(point, RIGHT)
        # xy0_label.next_to(flat_project(point), RIGHT)

        # vert_dots.save_state()
        # vert_dots.set_glow_factor(5)
        # vert_dots.set_radius(0.5)
        # vert_dots.set_opacity(0)
        # self.play(
        #     Restore(vert_dots),
        #     Write(xyz_label),
        # )
        # self.wait()