# core.py

from dataclasses import dataclass

class Resource:
    resources = dict()

    def __init__(self, name, amount = 0, max_amount = float('inf')):
        self.name = name
        self.amount = amount
        self.max_amount = max_amount
        self._postupdate = 0
        Resource.resources[name] = self

    def update(self):
        self.amount = min(self.amount + self._postupdate, self.max_amount)
        self._postupdate = 0

    def can_take(self, amount):
        return self.amount >= amount

    def give(self, amount):
        self._postupdate += amount

    def take(self, amount):
        if self.can_take(amount):
            self.amount -= amount

    def __str__(self):
        return f"{self.name}: {self.amount:.2f}"

from enum import Enum, auto
class ConverterState(Enum):
    OK = auto()
    NO_INPUT = auto()
    MAX_OUTPUT = auto()
    STOPPED = auto()
class Converter:
    converters = dict()

    def __init__(self, name, in_recipes, out_recipes):
        self.name = name
        self.in_recipes = in_recipes
        self.out_recipes = out_recipes
        Converter.converters[name] = self
        self.state = ConverterState.STOPPED

    def update(self):
        self.could_convert = False
        if self.state == ConverterState.STOPPED:
            return
        for rec in self.out_recipes:
            res,prod = rec.resource,rec.amount
            if res.amount >= res.max_amount:
                self.state = ConverterState.MAX_OUTPUT
                return
        for rec in self.in_recipes:
            res,need,min_amount = rec.resource,rec.amount,rec.min_amount
            if not res.can_take(need) or res.amount < min_amount:
                self.state = ConverterState.NO_INPUT
                return
        self.state = ConverterState.OK
        for rec in self.in_recipes:
            res,need = rec.resource,rec.amount
            res.take(need)
        for rec in self.out_recipes:
            res,prod = rec.resource,rec.amount
            res.give(prod)


@dataclass
class Recipe:
    resource: Resource
    amount: float = 0
    min_amount: float = 0

