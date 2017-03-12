from . import utils
from . import methods
from collections import namedtuple

State = namedtuple('State', ['pos', 'vel'])


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

    def __init__(self, name, pos, vel, mass):
        self.name = name
        self.pos = utils.Vector2.from_pair(pos)
        self.vel = utils.Vector2.from_pair(vel)
        self.mass = mass
        self.inv_mass = 1 / mass
        self.forces = utils.Vector2()

    def reset_forces(self):
        self.forces = utils.Vector2()

    def apply_force(self, body):
        """Applies another body's gravitational force to this body."""
        r = body.pos - self.pos
        r3 = abs(r)**3
        gravity = -(body.mass / r3) * r
        self.forces += -(self.mass * body.mass / r3) * r

    def integrate(self, dt, method=methods.euler):
        """
        m dv/dt = F
        """
        at = self.forces * self.inv_mass
        vt = self.vel
        xt = self.pos
        new_vel, new_pos = method(at, vt, xt, dt)
        self.vel = new_vel
        self.pos = new_pos

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Planet(Body):
    pass


class Star(Body):
    pass