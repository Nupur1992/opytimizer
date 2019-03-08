import numpy as np
from opytimizer import Opytimizer
from opytimizer.core.function import Function
from opytimizer.optimizers.ba import BA
from opytimizer.spaces.search import SearchSpace


def sphere(x):
    # Declaring Sphere's function
    y = x ** 2

    return np.sum(y)


# Creating Function's object
f = Function(pointer=sphere)

# Number of agents
n_agents = 2

# Number of decision variables
n_variables = 2

# Number of running iterations
n_iterations = 10

# Lower and upper bounds (has to be the same size as n_variables)
lower_bound = [-10, -10]
upper_bound = [10, 10]

# Creating the SearchSpace class
s = SearchSpace(n_agents=n_agents, n_iterations=n_iterations,
                n_variables=n_variables, lower_bound=lower_bound,
                upper_bound=upper_bound)

# Hyperparameters for the optimizer
hyperparams = {
    'f_min': 0,
    'f_max': 2,
    'A': 0.5,
    'r': 0.5
}

# Creating PSO's optimizer
p = BA(hyperparams=hyperparams)

# Finally, we can create an Opytimizer class
o = Opytimizer(space=s, optimizer=p, function=f)

# Running the optimization task
history = o.start()

# Now, there is a History object holding vital historical information from the optimization task
# history.show()
