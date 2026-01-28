from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any
import copy


class RichExample:
	"""Showcase class implementing a wide variety of dunder hooks."""

	def __init__(self, name: str, values: Iterable[int] | None = None) -> None:
		object.__setattr__(self, "name", name)
		object.__setattr__(self, "_values", list(values or []))
		object.__setattr__(self, "_extras", {})
		object.__setattr__(self, "_active", False)

	def __repr__(self) -> str:
		return f"RichExample(name={self.name!r}, values={self._values!r})"

	def __str__(self) -> str:
		return f"{self.name}: {self._values}"

	def __bytes__(self) -> bytes:
		return str(self).encode("ascii", "ignore")

	def __format__(self, format_spec: str) -> str:
		return format(str(self), format_spec) if format_spec else str(self)

	def __hash__(self) -> int:
		return hash((self.name, tuple(self._values)))

	def __bool__(self) -> bool:
		return bool(self._values)

	def __len__(self) -> int:
		return len(self._values)

	def __iter__(self) -> Iterator[int]:
		return iter(self._values)

	def __contains__(self, item: Any) -> bool:
		return item in self._values

	def __getitem__(self, index: int) -> int:
		return self._values[index]

	def __setitem__(self, index: int, value: int) -> None:
		self._values[index] = value

	def __delitem__(self, index: int) -> None:
		del self._values[index]

	def __call__(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
		return {
			"name": self.name,
			"sum": sum(self._values),
			"args": args,
			"kwargs": kwargs,
		}

	def __eq__(self, other: Any) -> bool:
		return isinstance(other, RichExample) and (self.name, self._values) == (other.name, other._values)

	def __lt__(self, other: Any) -> bool:
		if not isinstance(other, RichExample):
			return NotImplemented
		return (self.name, self._values) < (other.name, other._values)

	def __add__(self, other: Any) -> "RichExample":
		return RichExample(self.name, self._values + self._coerce_iterable(other))

	def __radd__(self, other: Any) -> "RichExample":
		return RichExample(self.name, self._coerce_iterable(other) + self._values)

	def __iadd__(self, other: Any) -> "RichExample":
		self._values.extend(self._coerce_iterable(other))
		return self

	def __enter__(self) -> "RichExample":
		self._active = True
		return self

	def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
		self._active = False
		return False

	def __getattr__(self, item: str) -> Any:
		try:
			return self._extras[item]
		except KeyError as err:
			raise AttributeError(item) from err

	def __setattr__(self, key: str, value: Any) -> None:
		if key.startswith("_"):
			object.__setattr__(self, key, value)
		else:
			self._extras[key] = value

	def __delattr__(self, item: str) -> None:
		if item.startswith("_"):
			object.__delattr__(self, item)
		else:
			try:
				del self._extras[item]
			except KeyError as err:
				raise AttributeError(item) from err

	def __dir__(self) -> list[str]:
		return sorted(set(super().__dir__()) | set(self._extras.keys()))

	def __getstate__(self) -> dict[str, Any]:
		return {
			"name": self.name,
			"values": list(self._values),
			"extras": dict(self._extras),
		}

	def __setstate__(self, state: dict[str, Any]) -> None:
		object.__setattr__(self, "name", state.get("name", "unknown"))
		object.__setattr__(self, "_values", state.get("values", []))
		object.__setattr__(self, "_extras", state.get("extras", {}))
		object.__setattr__(self, "_active", False)

	def __copy__(self) -> "RichExample":
		cloned = RichExample(self.name, self._values)
		cloned._extras = self._extras.copy()
		return cloned

	def __deepcopy__(self, memo: dict[int, Any]) -> "RichExample":
		cloned = RichExample(copy.deepcopy(self.name, memo), copy.deepcopy(self._values, memo))
		cloned._extras = copy.deepcopy(self._extras, memo)
		return cloned

	def _coerce_iterable(self, other: Any) -> list[int]:
		# Converts supported operands into a list of ints for arithmetic dunders.
		if isinstance(other, RichExample):
			return list(other._values)
		if isinstance(other, (str, bytes)):
			raise TypeError("string-like operands are not supported")
		if isinstance(other, Iterable):
			return [int(value) for value in other]
		return [int(other)]


if __name__ == "__main__":
	demo = RichExample("demo", [1, 2, 3])
	demo.color = "blue"
	print(repr(demo))
	print(str(demo))
	print(format(demo, "^30"))
	print(bytes(demo))
	print(len(demo), bool(demo), 2 in demo)
	demo += [4, 5]
	print(demo())
	with demo as ctx:
		print("Context active:", ctx._active)
	print("Attributes:", dir(demo))
