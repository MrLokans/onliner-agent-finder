from coordinates import Point


def test_points_with_same_coordinates_are_considered_equal():
    p1 = Point(2.0, 3.0)
    p2 = Point(2.0, 3.0)

    assert p1 == p2


def test_points_with_different_coordinates_are_considered_not_equal():
    p1 = Point(2.0, 3.0)
    p2 = Point(2.0, 4.0)

    assert p1 != p2

    p1 = Point(2.0, 3.0)
    p2 = Point(3.0, 3.0)

    assert p1 != p2

    p1 = Point(4.0, 3.0)
    p2 = Point(3.0, 4.0)

    assert p1 != p2


def test_points_with_close_coordinates_are_considered_equal():
    p1 = Point(2.0003, 3.0003)
    p2 = Point(2.0004, 3.0004)

    assert p1 == p2
