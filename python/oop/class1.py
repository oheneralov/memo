class MathUtils:
	"""Utility math helpers that do not depend on instance state."""

	@staticmethod
	def __square(value: float) -> float:
		"""Private helper to keep the hypotenuse formula readable."""
		return value * value

	@staticmethod
	def hypotenuse(a: float, b: float) -> float:
		"""Return the Pythagorean hypotenuse for sides a and b."""
		return (MathUtils.__square(a) + MathUtils.__square(b)) ** 0.5


class Triangle:
	"""Right triangle described by the lengths of the two legs."""

	def __init__(self, leg_a: float, leg_b: float) -> None:
		self.leg_a = leg_a
		self.leg_b = leg_b

	def _legs(self) -> tuple[float, float]:
		"""Protected helper that exposes legs for subclasses."""
		# Subclasses can inspect legs without touching private state.
		return self.leg_a, self.leg_b

	def __sum_of_squares(self) -> float:
		"""Private instance helper that uses object state."""
		return self.leg_a * self.leg_a + self.leg_b * self.leg_b

	def hypotenuse(self) -> float:
		"""Compute hypotenuse using the object's stored legs."""
		return self.__sum_of_squares() ** 0.5


class TriangleReporter(Triangle):
	"""Simple subclass that consumes the protected helper."""

	def describe(self) -> str:
		leg_a, leg_b = self._legs()
		return (
			f"Triangle with legs {leg_a} and {leg_b} has hypotenuse {self.hypotenuse():.2f}"
		)


if __name__ == "__main__":
	c = MathUtils.hypotenuse(3, 4)
	print(f"Static helper hypotenuse: {c}")

	triangle = Triangle(5, 12)
	print(f"Instance helper hypotenuse: {triangle.hypotenuse()}")

	reporter = TriangleReporter(7, 24)
	print(reporter.describe())
