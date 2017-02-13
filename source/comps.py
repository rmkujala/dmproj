import math


def angle(x, y):
    """
    Compute the angle between sets x and y.

    Parameters
    ----------
    x : set
        describes the temrs in a tweet
    y : set
        describes the terms in a tweet

    Returns
    -------
    angle : float
        the angle between the two vectors in radians.
    """
    tx_ty = len(x) * len(y)
    if tx_ty == 0:
        return math.pi / 2
    else:
        intersection_size = len(x & y)
        return math.acos(intersection_size / math.sqrt(tx_ty))


def get_lower_bound(x, y):
    """
    Obtain a lower bound for the angle.

    Parameters
    ----------
    x : size of the query tweet
    y : max number of common neighbors

    Returns
    -------
    low_bound : str
    """
    return math.acos(y / math.sqrt(x * y))
