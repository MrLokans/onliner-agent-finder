from coordinates import CoordinateRectangle, Point


class TestRectangleEquality(object):

    def test_rectangles_with_same_coords_are_considered_equal(self):
        p1 = Point(2.0, 3.0)
        p2 = Point(10.0, 30.0)

        rect1 = CoordinateRectangle(p1, p2)
        rect2 = CoordinateRectangle(p1, p2)

        assert rect1 == rect2


    def test_rectangles_with_different_coords_are_not_considered_equal(self):
        p1 = Point(2.0, 3.0)
        p2 = Point(10.0, 30.0)
        p3 = Point(11.0, 31.0)

        rect1 = CoordinateRectangle(p1, p2)
        rect2 = CoordinateRectangle(p1, p3)

        assert rect1 != rect2


class TestRectangleSplitting(object):
    def test_splitting_rectangle_into_1_to_1_returns_same_rectangle(self):
        p1 = Point(2.0, 3.0)
        p2 = Point(10.0, 30.0)
        rect1 = CoordinateRectangle(p1, p2)

        results = rect1.get_rectangles(1, 1)
        assert results == [rect1]

    def test_splitting_rectangle_into_2_to_2_returns_4_same_squared_rectangles(self):
        sample_rect = CoordinateRectangle(Point(1.0, 3.0), Point(9.0, 13.0))

        expected_rectangles = [
            CoordinateRectangle(Point(1.0, 4.0), Point(5.0, 13.0)),
            CoordinateRectangle(Point(5.0, 8.0), Point(9.0, 13.0)),
            CoordinateRectangle(Point(1.0, 3.0), Point(5.0, 8.0)),
            CoordinateRectangle(Point(5.0, 3.0), Point(9.0, 8.0)),
        ]

        assert sample_rect.get_rectangles(2, 2) == expected_rectangles
