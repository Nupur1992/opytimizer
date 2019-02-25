import numpy as np
from math import gamma, sin, pi


def generate_uniform_random_number(low=0.0, high=1.0, size=1):
    """Generates a random number or array based on an uniform distribution.

    Args:
        low (float): lower interval.
        high (float): higher interval.
        size (int): size of array.

    Returns:
        An uniform random number or array.

    """

    # Generates a random uniform number or array
    uniform_array = np.random.uniform(low, high, size)

    return uniform_array


def generate_gaussian_random_number(mean=0.0, variance=1.0, size=1):
    """Generates a random number or array based on a gaussian distribution.

    Args:
        mean (float): gaussian's mean value.
        variance (float): gaussian's variance value.
        size (int): size of array.

    Returns:
        A gaussian random number or array.

    """

    # Generates a random gaussian number or array
    gaussian_array = np.random.normal(mean, variance, size)

    return gaussian_array

def generate_levy_distribution(n_variables, beta):
    """
    It generates an n-dimensional array drawn from a Levy distribution
    The formulation used here is based on the paper "Multiobjective Cuckoo Search for Design Optimization", X.-S. Yang and S. Deb, Computers & Operations Research, 2013.

    Properties:
    n_variables (int): dimension of the output array
    beta (float): input parameter used in the formulation
    """

    if n_variables < 1:
        raise TypeError("Invalid input paramater @GenerateLevyDistribution.")

    num = gamma(1+beta)*sin(pi*beta/2)
    den = gamma((1+beta)/2)*beta*2**((beta-1)/2)
    sigma_u = (num/den)**(1/beta)
    u = np.random.normal(0, sigma_u**2, n_variables)
    v = np.random.normal(0, 1, n_variables)
    step = u / np.abs(v) ** (1 / beta)

    return step
