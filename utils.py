import math


def are_floats_equal(f1, f2, prec=1e-4):
    return math.isclose(f1, f2, rel_tol=prec)
