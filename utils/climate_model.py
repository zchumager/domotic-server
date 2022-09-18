from functools import reduce
from operator import add, mul


def basic(temperatures, weights):
    """
    :param temperatures: list of temperatures
    :param weights: list of weights related to each temperature
    :return: the calculated temperature with the model
    """

    print("Using climate model")

    dividend = reduce(add, map(mul, temperatures, weights))
    divisor = sum(weights)

    return dividend // divisor


"""
Add more models to be used for calculating temperature
"""