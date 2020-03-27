from manimlib.imports import *

class Pendulum(VGroup):
    CONFIG = {
        "length": 3,                # Default
        "gravity": 9.8,             # Default
        "weight_diameter": 0.5,     # Default
        "initial_theta": PI/4,
        "omega": -2,
        "damping": 0,
        "top_point": 2 * UP,        # Default
        "rod_style": {"stroke_color": GOLD},
        "weight_style": {"fill_color": BLUE},
        "dashed_line_config": {},
        "n_steps_per_frame": 10000
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_fixed_point()
        self.create_rod()
        self.create_weight()
        self.rotating_group = VGroup(self.rod, self.weight)
        self.create_dashed_line()
        self.set_theta(self.initial_theta)
        self.update()

    def create_fixed_point(self):
        self.fixed_point_tracker = VectorizedPoint(self.top_point)
        self.add(self.fixed_point_tracker)
        return self

    def create_rod(self):
        rod = self.rod = Line(UP, DOWN)
        rod.set_height(self.length)
        rod.set_style(**self.rod_style)
        rod.move_to(self.get_fixed_point(), UP)
        self.add(rod)

    def create_weight(self):
        weight = self.weight = Dot()
        weight.set_style(**self.weight_style)
        weight.move_to(self.rod.get_end())
        self.add(weight)

    def create_dashed_line(self):
        line = self.dashed_line = DashedLine(self.get_fixed_point(),self.get_fixed_point() + self.length * DOWN,**self.dashed_line_config
        )
        line.add_updater(
            lambda l: l.move_to(self.get_fixed_point(), UP)
        )
        self.add_to_back(line)

    def get_theta(self):
        theta = self.rod.get_angle() - self.dashed_line.get_angle()
        theta = (theta + PI) % TAU - PI
        return theta

    def set_theta(self, theta):
        self.rotating_group.rotate(theta-self.get_theta())
        self.rotating_group.shift(self.get_fixed_point()-self.rod.get_start())
        return self

    def get_omega(self):
        return self.omega

    def set_omega(self, omega):
        self.omega = omega
        return self

    def get_fixed_point(self):
        return self.fixed_point_tracker.get_location()

    def start_swinging(self):
        self.add_updater(Pendulum.update_by_gravity)

    def end_swinging(self):
        self.remove_updater(Pendulum.update_by_gravity)

    def update_by_gravity(self, dt):
        theta = self.get_theta()
        omega = self.get_omega()
        framerate = self.n_steps_per_frame
        for x in range(framerate):
            time = dt/framerate
            dtheta = omega*time
            domega = op.add(-self.damping * omega,-(self.gravity / self.length)*np.sin(theta))*time
            theta += dtheta
            omega += domega
        self.set_theta(theta)
        self.set_omega(omega)
        return self

class SimplePendulum(MovingCameraScene):
    CONFIG = {
        "pendulum_config": {
            "length": 3,
            "top_point": 4 * RIGHT,
            "weight_diameter": 0.35,
            "gravity": 9.8,
        }
    }

    def setup(self):
        MovingCameraScene.setup(self)

    def construct(self):
        self.add_pendulum()

    def add_pendulum(self):
        pendulum = self.pendulum = Pendulum(**self.pendulum_config)
        pendulum.start_swinging()
        frame = self.camera_frame
        frame.save_state()
        frame.scale(1)
        frame.move_to(pendulum.top_point)
            # Or:
            #frame.scale(1)
            #frame.move_to(pendulum.top_point)
        self.add(pendulum, frame)
        self.wait(20)
