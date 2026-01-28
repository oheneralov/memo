"""Simple mixin example combining reusable behavior with base classes."""

from datetime import datetime


class TimestampMixin:
	"""Adds created/updated timestamps when saving entities."""

	def __init__(self) -> None:
		self.created_at: datetime | None = None
		self.updated_at: datetime | None = None

	def touch(self) -> None:
		now = datetime.utcnow()
		if self.created_at is None:
			self.created_at = now
		self.updated_at = now


class SoftDeleteMixin:
	"""Provides soft-delete flag handling."""

	def __init__(self) -> None:
		self.deleted = False

	def delete(self) -> None:
		self.deleted = True


class CustomerRecord(TimestampMixin, SoftDeleteMixin):
	"""Concrete entity inheriting reusable mixin behavior."""

	def __init__(self, name: str) -> None:
		TimestampMixin.__init__(self)
		SoftDeleteMixin.__init__(self)
		self.name = name

	def save(self) -> None:
		self.touch()
		# Imagine persistence logic here.

	def __repr__(self) -> str:  # Helpful when printing demo output.
		return (
			f"CustomerRecord(name={self.name!r}, created_at={self.created_at}, "
			f"updated_at={self.updated_at}, deleted={self.deleted})"
		)


if __name__ == "__main__":
	customer = CustomerRecord("Alice")
	customer.save()
	print(customer)
	customer.delete()
	print(customer)
