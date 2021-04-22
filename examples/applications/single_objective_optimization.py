import numpy as np
from opytimark.markers.n_dimensional import Sphere

from opytimizer import Opytimizer
from opytimizer.core.function import Function
from opytimizer.optimizers.swarm.fa import FA
from opytimizer.spaces.search import SearchSpace

# Random seed for experimental consistency
np.random.seed(0)

# Number of agents, decision variables and iterations
n_agents = 20
n_variables = 2
n_iterations = 1000

# Lower and upper bounds (has to be the same size as n_variables)
lower_bound = (-10, -10)
upper_bound = (10, 10)

# Creating the SearchSpace class
s = SearchSpace(n_agents=n_agents, n_iterations=n_iterations,
                n_variables=n_variables, lower_bound=lower_bound,
                upper_bound=upper_bound)

# Hyperparameters for the optimizer
hyperparams = {
    'w': 0.7,
    'c1': 1.7,
    'c2': 1.7
}

# Creating PSO's optimizer
p = FA(hyperparams=hyperparams)

# Creating Function's object
f = Function(pointer=Sphere())

# Finally, we can create an Opytimizer class
o = Opytimizer(space=s, optimizer=p, function=f)

# Running the optimization task
history = o.start(n_iterations=100)
