"""Demonstrates abstract and class methods in Python."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable, Mapping


class PaymentProcessor(ABC):
	"""Contract for processing customer payments."""

	@abstractmethod
	def process(self, amount: float) -> str:
		"""Charge the provided amount and return a status message."""


class CardProcessor(PaymentProcessor):
	"""Processes payments using a credit card gateway."""

	def process(self, amount: float) -> str:
		fee = amount * 0.029 + 0.3
		net_amount = amount - fee
		return f"Charged ${amount:.2f}, net after fees: ${net_amount:.2f}."


class SalesReport:
	"""Aggregates sales amounts and builds a concise summary."""

	def __init__(self, total: float, generated_at: datetime) -> None:
		self.total = total
		self.generated_at = generated_at

	@classmethod
	def from_entries(cls, entries: Iterable[Mapping[str, float]]) -> "SalesReport":
		total = sum(entry["amount"] for entry in entries)
		return cls(total=total, generated_at=datetime.utcnow())

	def summary(self) -> str:
		timestamp = self.generated_at.strftime("%Y-%m-%d %H:%M:%S")
		return f"Total sales ${self.total:.2f} as of {timestamp}."


if __name__ == "__main__":
	processor: PaymentProcessor = CardProcessor()
	print(processor.process(49.99))

	sample_entries = (
		{"amount": 49.99},
		{"amount": 19.50},
		{"amount": 5.25},
	)
	report = SalesReport.from_entries(sample_entries)
	print(report.summary())
