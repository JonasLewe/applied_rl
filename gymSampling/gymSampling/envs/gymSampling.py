"""
Cart pole swing-up: modified version of:
https://github.com/hardmaru/estool/blob/master/custom_envs/cartpole_swingup.py
"""
"""
Cartpole sampling: modified version of Cart pole swing-up:
https://github.com/angelolovatto/gym-cartpole-swingup
"""
from dataclasses import dataclass, field
from collections import namedtuple

import numpy as np
import gym
from gym import spaces
from gym.utils import seeding


@dataclass(frozen=True)
class CartParams:
    """Parameters defining the Cart."""

    width: float = 1 / 3
    height: float = 1 / 6
    mass: float = 0.5


@dataclass(frozen=True)
class PoleParams:
    """Parameters defining the Pole."""

    width: float = 0.05
    length: float = 0.6
    mass: float = 0.5


@dataclass
class CartPoleSwingUpParams:  # pylint: disable=no-member,too-many-instance-attributes
    """Parameters for physics simulation."""

    gravity: float = 9.82
    forcemag: float = 10.0
    deltat: float = 0.01
    friction: float = 0.1
    x_threshold: float = 2.4
    cart: CartParams = field(default_factory=CartParams)
    pole: PoleParams = field(default_factory=PoleParams)
    masstotal: float = field(init=False)
    mpl: float = field(init=False)

    def __post_init__(self):
        self.masstotal = self.cart.mass + self.pole.mass
        self.mpl = self.pole.mass * self.pole.length


State = namedtuple("State", "x_pos x_dot theta theta_dot")


class GymSampling(gym.Env):
    """
    Description:
       A pole is attached by an un-actuated joint to a cart, which moves along a track.
       Unlike CartPoleEnv, friction is taken into account in the physics calculations.
       The pendulum starts (pointing down) upside down, and the goal is to swing it up
       and keep it upright by increasing and reducing the cart's velocity.
    """

    metadata = {"render.modes": ["human", "rgb_array"], "video.frames_per_second": 50}

    def __init__(self):
        high = np.array([1.0], dtype=np.float32)
        self.action_space = spaces.Box(low=-high, high=high)
        high = np.array([np.finfo(np.float32).max] * 5, dtype=np.float32)
        self.observation_space = spaces.Box(low=-high, high=high)
        self.params = CartPoleSwingUpParams()

        self.seed()
        self.viewer = None
        self.state = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        state = self.state
        # Valid action
        action = np.clip(action, self.action_space.low, self.action_space.high)
        self.state = next_state = self._transition_fn(self.state, action)
        next_obs = self._get_obs(next_state)
        reward = self._reward_fn(state, action, next_state)
        done = self._terminal(next_state)

        return next_obs, reward, done, {}

    def reset(self):
        self.state = State(
            *self.np_random.uniform(low = np.array([-1, -1, 0, -1]), high=np.array([1, 1, 2*np.pi, 1]),).astype(np.float32)
        )
        return self._get_obs(self.state)

    @staticmethod
    def _reward_fn(state, action, next_state):
        return np.cos(next_state.theta, dtype=np.float32)

    def _terminal(self, state):
        return bool(abs(state.x_pos) > self.params.x_threshold)

    def _transition_fn(self, state, action):
        # pylint: disable=no-member
        action = action[0] * self.params.forcemag

        sin_theta = np.sin(state.theta)
        cos_theta = np.cos(state.theta)

        xdot_update = (
            -2 * self.params.mpl * (state.theta_dot ** 2) * sin_theta
            + 3 * self.params.pole.mass * self.params.gravity * sin_theta * cos_theta
            + 4 * action
            - 4 * self.params.friction * state.x_dot
        ) / (4 * self.params.masstotal - 3 * self.params.pole.mass * cos_theta ** 2)
        thetadot_update = (
            -3 * self.params.mpl * (state.theta_dot ** 2) * sin_theta * cos_theta
            + 6 * self.params.masstotal * self.params.gravity * sin_theta
            + 6 * (action - self.params.friction * state.x_dot) * cos_theta
        ) / (
            4 * self.params.pole.length * self.params.masstotal
            - 3 * self.params.mpl * cos_theta ** 2
        )

        delta_t = self.params.deltat
        return State(
            x_pos=state.x_pos + state.x_dot * delta_t,
            theta=state.theta + state.theta_dot * delta_t,
            x_dot=state.x_dot + xdot_update * delta_t,
            theta_dot=state.theta_dot + thetadot_update * delta_t,
        )

    @staticmethod
    def _get_obs(state):
        x_pos, x_dot, theta, theta_dot = state
        return np.array(
            [x_pos, x_dot, np.cos(theta), np.sin(theta), theta_dot], dtype=np.float32
        )

    def render(self, mode="human"):
        if self.viewer is None:
            self.viewer = CartPoleSwingUpViewer(
                self.params.cart, self.params.pole, world_width=5
            )

        if self.state is None:
            return None

        self.viewer.update(self.state, self.params.pole)
        return self.viewer.render(return_rgb_array=mode == "rgb_array")

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None

