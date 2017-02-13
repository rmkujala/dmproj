import numpy as np
import comps


def test_angle():
    a = {"a", "b", "c"}

    b = {"b", "c", "d"}

    ang_should_be = 0.84106867056793033
    assert_angle_comp(a, b, ang_should_be)

    assert_angle_comp({}, {}, np.pi / 2)
    assert_angle_comp({1}, {}, np.pi / 2)
    assert_angle_comp({1}, {1}, 0)


def assert_angle_comp(x, y, ang_should_be):
    ang = comps.angle(x, y)
    np.testing.assert_approx_equal(ang, ang_should_be)
