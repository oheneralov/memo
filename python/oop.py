"""Demo covering isinstance plus the lifecycle differences of __new__ vs __init__."""

from __future__ import annotations


class Device:
	"""Base device with a name and generic status reporting."""

	def __init__(self, name: str) -> None:
		self.name = name

	def status(self) -> str:
		return f"{self.name} is operational"


class Gadget(Device):
	"""Specialized device that tracks a feature."""

	def __init__(self, name: str, feature: str) -> None:
		super().__init__(name)
		self.feature = feature

	def status(self) -> str:
		base_status = super().status()
		return f"{base_status} with feature {self.feature}"


class LifecycleTracer:
	"""Prints when __new__ and __init__ fire so their roles are obvious."""

	def __new__(cls, label: str) -> "LifecycleTracer":
		print(f"LifecycleTracer.__new__ -> allocating object for {label}")
		instance = super().__new__(cls)
		instance.label_from_new = label  # Attribute created before __init__ runs
		return instance

	def __init__(self, label: str) -> None:
		print(f"LifecycleTracer.__init__ -> initializing object for {label}")
		self.label = label


class CachedGadget(Gadget):
	"""Uses __new__ to reuse instances and __init__ to guard double setup."""

	_cache: dict[str, "CachedGadget"] = {}

	def __new__(cls, name: str, feature: str) -> "CachedGadget":
		if name in cls._cache:
			print(f"CachedGadget.__new__ -> reusing cached instance for {name}")
			return cls._cache[name]
		print(f"CachedGadget.__new__ -> creating fresh instance for {name}")
		instance = super().__new__(cls)
		cls._cache[name] = instance
		return instance

	def __init__(self, name: str, feature: str) -> None:
		if getattr(self, "_initialized", False):
			print(f"CachedGadget.__init__ skipped for {name} (already initialized)")
			return
		print(f"CachedGadget.__init__ -> initializing {name}")
		super().__init__(name, feature)
		self._initialized = True


if __name__ == "__main__":
	laptop = Device("Laptop")
	drone = Gadget("Drone", "stabilizer")

	print(laptop.status())
	print(drone.status())

	print("\n=== isinstance demo ===")
	print("Is laptop a Device?", isinstance(laptop, Device))
	print("Is laptop a Gadget?", isinstance(laptop, Gadget))
	print("Is drone a Device?", isinstance(drone, Device))
	print("Is drone a Gadget?", isinstance(drone, Gadget))

	print("\n=== __new__ vs __init__ sequencing ===")
	tracer = LifecycleTracer("alpha")
	print("label_from_new (set in __new__):", tracer.label_from_new)
	print("label (set in __init__):", tracer.label)

	print("\n=== __new__ returning cached instances ===")
	cached_one = CachedGadget("Raven", "optical kit")
	cached_two = CachedGadget("Raven", "thermal kit")  # __new__ reuses cached_one
	print("cached_one is cached_two?", cached_one is cached_two)
	print("Feature preserved from first initialization:", cached_two.feature)
