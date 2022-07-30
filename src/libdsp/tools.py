import numpy as np


def almost_equal(x, y, tol=0.0000001):
    return True if np.abs(x - y) < tol else False
