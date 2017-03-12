from . import utils
from . import methods
from collections import namedtuple, deque


class Body:
    """
    Represents a celestial body.
    Distances must be given in AU
        1 AU = 149,597,870.700 m
    Time is measured in years
        1 yr = 31,557,600 s
    Mass is measured in solar masses, Ms
        1 Ms = 4π2 AU^3/yr^3/G ≈ 1.99e30 kg
    Force is measured in F (arbitrary unit)
        1 F = G Ms^2 / AU^2 ≈ 2.989e23 N

    Parameters
    ----------
    pos0 : Vector2
        Initial position (in AU)
    vel0 : Vector2
        Initial velocity (in AU/yr)
    mass : float
        Mass (in solar masses)

    Attributes
    ----------
    pos : Vector2
    vel : Vector2
    mass : float
    inv_mass : float
    forces : Vector2
        The forces applied to the Body.
    """
    class State:

        def __init__(self, pos, vel, forces):
            self.pos = pos
            self.vel = vel
            self.forces = forces

    def __init__(self, name, pos, vel, mass):
        self.name = name
        self.states = deque(maxlen=3)  # remember a few past states
        pos = utils.Vector2.from_pair(pos)
        vel = utils.Vector2.from_pair(vel)
        self.states.appendleft(Body.State(pos, vel, utils.Vector2()))
        self.mass = mass
        self.inv_mass = 1 / mass

    @property
    def pos(self):
        return self.states[-1].pos

    @pos.setter
    def pos(self, new_pos):
        new_pos = utils.Vector2.from_pair(new_pos)
        self.states[-1].pos = new_pos

    @property
    def prev_pos(self):
        return self.states[-2].pos

    @property
    def vel(self):
        return self.states[-1].vel

    @vel.setter
    def vel(self, new_vel):
        new_vel = utils.Vector2.from_pair(new_vel)
        self.states[-1].vel = new_vel

    @property
    def prev_vel(self):
        return self.states[-2].vel

    @property
    def forces(self):
        return self.states[-1].forces

    @forces.setter
    def forces(self, new_forces):
        new_forces = utils.Vector2.from_pair(new_forces)
        self.states[-1].forces = new_forces

    @property
    def prev_forces(self):
        return self.states[-2].forces

    def new_state(self):
        self.states.appendleft(Body.State(self.pos, self.vel, utils.Vector2()))

    def apply_gravity_of(self, body):
        """Applies another body's gravitational force to this body."""
        r = body.pos - self.pos
        r3 = abs(r)**3
        self.forces += -(self.mass * body.mass / r3) * r

    def integrate(self, dt, method=methods.euler):
        self.vel, self.pos = method(self, dt)

    def __eq__(self, other):
        try:
            if self.name != other.name:
                return False
            if self.mass != other.mass:
                return False
            if self.pos != other.pos:
                return False
            if self.vel != other.vel:
                return False
            return True
        except AttributeError:
            return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Planet(Body):
    pass


class Star(Body):
    pass
