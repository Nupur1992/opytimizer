"""Butterfly Optimization Algorithm.
"""

import numpy as np

import opytimizer.math.random as r
import opytimizer.utils.exception as e
import opytimizer.utils.logging as l
from opytimizer.core import Optimizer

logger = l.get_logger(__name__)


class BOA(Optimizer):
    """A BOA class, inherited from Optimizer.

    This is the designed class to define BOA-related
    variables and methods.

    References:
        S. Arora and S. Singh. Butterfly optimization algorithm: a novel approach for global optimization.
        Soft Computing (2019).

    """

    def __init__(self, params=None):
        """Initialization method.

        Args:
            params (dict): Contains key-value parameters to the meta-heuristics.

        """

        logger.info('Overriding class: Optimizer -> BOA.')

        # Overrides its parent class with the receiving params
        super(BOA, self).__init__()

        # Sensor modality
        self.c = 0.01

        # Power exponent
        self.a = 0.1

        # Switch probability
        self.p = 0.8

        # Builds the class
        self.build(params)

        logger.info('Class overrided.')

    @property
    def c(self):
        """float: Sensor modality.

        """

        return self._c

    @c.setter
    def c(self, c):
        if not isinstance(c, (float, int)):
            raise e.TypeError('`c` should be a float or integer')
        if c < 0:
            raise e.ValueError('`c` should be >= 0')

        self._c = c

    @property
    def a(self):
        """float: Power exponent.

        """

        return self._a

    @a.setter
    def a(self, a):
        if not isinstance(a, (float, int)):
            raise e.TypeError('`a` should be a float or integer')
        if a < 0:
            raise e.ValueError('`a` should be >= 0')

        self._a = a

    @property
    def p(self):
        """float: Switch probability.

        """

        return self._p

    @p.setter
    def p(self, p):
        if not isinstance(p, (float, int)):
            raise e.TypeError('`p` should be a float or integer')
        if p < 0 or p > 1:
            raise e.ValueError('`p` should be between 0 and 1')

        self._p = p

    @property
    def fragrance(self):
        """np.array: Array of fragrances.

        """

        return self._fragrance

    @fragrance.setter
    def fragrance(self, fragrance):
        if not isinstance(fragrance, np.ndarray):
            raise e.TypeError('`fragrance` should be a numpy array')

        self._fragrance = fragrance

    def compile(self, space):
        """Compiles additional information that is used by this optimizer.

        Args:
            space (Space): A Space object containing meta-information.

        """

        # Arrays of fragances
        self.fragrance = np.zeros(space.n_agents)

    def _best_movement(self, agent_position, best_position, fragrance, random):
        """Updates the agent's position towards the best butterfly (eq. 2).

        Args:
            agent_position (np.array): Agent's current position.
            best_position (np.array): Best agent's current position.
            fragrance (np.array): Agent's current fragrance value.
            random (float): A random number between 0 and 1.

        Returns:
            A new position based on best movement.

        """

        # Calculates the new position based on best movement
        new_position = agent_position + (random ** 2 * best_position - agent_position) * fragrance

        return new_position

    def _local_movement(self, agent_position, j_position, k_position, fragrance, random):
        """Updates the agent's position using a local movement (eq. 3).

        Args:
            agent_position (np.array): Agent's current position.
            j_position (np.array): Agent `j` current position.
            k_position (np.array): Agent `k` current position.
            fragrance (np.array): Agent's current fragrance value.
            random (float): A random number between 0 and 1.

        Returns:
            A new position based on local movement.

        """

        # Calculates the new position based on local movement
        new_position = agent_position + (random ** 2 * j_position - k_position) * fragrance

        return new_position

    def update(self, space):
        """Wraps Butterfly Optimization Algorithm over all agents and variables.

        Args:
            space (Space): Space containing agents and update-related information.

        """

        # Iterates through all agents
        for i, agent in enumerate(space.agents):
            # Calculates fragrance for current agent (eq. 1)
            self.fragrance[i] = self.c * agent.fit ** self.a

        # Iterates through all agents
        for i, agent in enumerate(space.agents):
            # Generates a uniform random number
            r1 = r.generate_uniform_random_number()

            # If random number is smaller than switch probability
            if r1 < self.p:
                # Moves current agent towards the best one (eq. 2)
                agent.position = self._best_movement(agent.position, space.best_agent.position,
                                                     self.fragrance[i], r1)

            # If random number is bigger than switch probability
            else:
                # Generates `j` and `k` indexes
                j = r.generate_integer_random_number(0, len(space.agents))
                k = r.generate_integer_random_number(0, len(space.agents), exclude_value=j)

                # Moves current agent using a local movement (eq. 3)
                agent.position = self._local_movement(agent.position, space.agents[j].position,
                                                      space.agents[k].position, self.fragrance[i],
                                                      r1)
