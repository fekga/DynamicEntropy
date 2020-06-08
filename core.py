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
            return amount
        return 0

    def __str__(self):
        return f"{self.name}: {self.amount:.2f}"

class Converter:
    converters = dict()

    def __init__(self, name, in_recipes, out_recipes):
        self.name = name
        self.in_recipes = in_recipes
        self.out_recipes = out_recipes
        self.running = True
        Converter.converters[name] = self

    def update(self):
        if not self.running:
            return
        for rec in self.out_recipes:
            res,prod = rec.resource,rec.amount
            if res.amount + prod > res.max_amount:
                return
        for rec in self.in_recipes:
            res,need,min_amount = rec.resource,rec.amount,rec.min_amount
            if not res.can_take(need) and res.amount < min_amount:
                return
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

