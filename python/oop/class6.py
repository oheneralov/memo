import code
from dataclasses import dataclass


class MethodTypesDemo:
	"""Showcases how @staticmethod and @classmethod behave differently."""

	default_discount = 0.1

	@staticmethod
	def compute_total(price, quantity):
		"""Pure function: depends only on provided args."""
		return price * quantity

	@classmethod
	def discounted_total(cls, price, quantity):
		"""Uses cls to access and modify shared class state."""
		subtotal = cls.compute_total(price, quantity)
		return subtotal * (1 - cls.default_discount)

	@classmethod
	def set_discount(cls, value):
		"""Update the shared class-level discount."""
		cls.default_discount = value


@dataclass
class Product:
	"""Compact data container using @dataclass for boilerplate reduction."""
	name: str
	price: float
	quantity: int = 1

	def total(self):
		"""Instance method that leverages generated __init__ and __repr__."""
		return self.price * self.quantity


if __name__ == "__main__":
	subtotal = MethodTypesDemo.compute_total(25, 4)
	print(f"Static subtotal: {subtotal}")

	MethodTypesDemo.set_discount(0.2)
	discounted = MethodTypesDemo.discounted_total(25, 4)
	print(f"Class-method discounted total: {discounted}")

	product = Product(name="Notebook", price=3.5, quantity=6)
	print(product)
	print(f"Dataclass total: {product.total()}")


MyClass = type(
    "MyClass",
    (object,),
    {"x": 10}
)

print(MyClass.x)  # 10
# This is equivalent to:
class MyClass:
    x = 10
