from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')
Point = tuple[T, T]


def cross_product(a: Point[T], b: Point[T]) -> T:
    return a[0] * b[1] - a[1] * b[0]


@dataclass
class Rect(Generic[T]):
    fr: Point[T]
    to: Point[T]

    def intersects(self, other: 'Rect[T]') -> bool:
        return self.fr[0] <= other.to[0] and \
               self.to[0] >= other.fr[0] and \
               self.fr[1] <= other.to[1] and \
               self.to[1] >= other.fr[1]


@dataclass
class Line(Generic[T]):
    fr: Point[T]
    to: Point[T]

    def get_bounding_box(self) -> Rect[T]:
        return Rect(
            (min(self.fr[0], self.to[0]),
             min(self.fr[1], self.to[1])),
            (max(self.fr[0], self.to[0]),
             max(self.fr[1], self.to[1]))
        )

    def get_cross_prod(self, point: Point[T]) -> T:
        trans_line = (self.to[0] - self.fr[0], self.to[1] - self.fr[1])
        trans_point = (point[0] - self.fr[0], point[1] - self.fr[1])

        return cross_product(trans_line, trans_point)

    def contains_point(self, point: Point[T]) -> bool:
        return self.get_cross_prod(point) == 0

    def is_point_to_the_right(self, point: Point[T]) -> bool:
        return self.get_cross_prod(point) < 0

    def touches_or_intersects_line(self, line: 'Line[T]') -> bool:
        return line.contains_point(self.fr) or \
               line.contains_point(self.to) or (
                   line.is_point_to_the_right(self.fr) ^
                   line.is_point_to_the_right(self.to)
               )

    def intersects(self, other: 'Line[T]') -> bool:
        box = self.get_bounding_box()
        other_box = other.get_bounding_box()

        return box.intersects(other_box) and \
               self.touches_or_intersects_line(other) and \
               other.touches_or_intersects_line(self)
