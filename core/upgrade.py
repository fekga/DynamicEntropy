# upgrade.py
from dataclasses import dataclass, field
from typing import List, Type
from core.change import Change
from core.resource import Resource
from core.save_load_game import SaveLoadGame

empty = lambda: field(default_factory=list)

@dataclass
class Cost:
    resource: Resource
    amount: float

    def __str__(self):
        return f'{self.amount} {self.resource.name}'

@dataclass
class Upgrade:
    name: str
    changes: List[Change]
    costs: List[Cost]
    requires: List[Type['Upgrade']] = empty()
    bought: bool = False
    upgrades = list()

    def __post_init__(self):
        if not self.changes:
            return
        if len(self.changes) == 1:
            self.changes[0].converter.upgrades.append(self)
        else:
            Upgrade.upgrades.append(self)

    def __repr__(self):
        if self.bought:
            return f'{self.name} {{Bought}}'
        costs_str = "Free"
        if self.costs:
            costs_str = "Cost:" if len(self.costs) == 1 else "Costs:"
            costs_str += "["
            for c in self.costs:
                costs_str += f'{c.resource.name}: {c.amount}'
            costs_str += "]"
        requires = ""
        if self.requires:
            requires = "Requires: ["
            for r in self.requires:
                requires += "\'" + r.name + "\' "
            requires += "]"
        changes = ""
        if self.changes:
            has_change = False
            for change in self.changes:
                if len(change.needs) or len(change.makes):
                    has_change = True

            if has_change:
                changes = f"Changes: {list(map(str,self.changes))}"
            else:
                changes = ''
        return f'{self.name}: {costs_str} {requires} {changes}'

    def __str__(self):
        return self.name

    def all_requirements_bought(self):
        for r in self.requires:
            if not r.bought:
                return False
        return True

    def isBuyable(self):
        if self.bought:
            return False
        for requirement in self.requires:
            if not requirement.bought:
                return False
        for cost in self.costs:
            if not cost.resource.can_take(cost.amount):
                return False
        return True

    def buy(self):
        if not self.isBuyable():
            return False
        for cost in self.costs:
            cost.resource.take(cost.amount)
        self.apply_changes()
        return True

    def apply_changes(self):
        for change in self.changes:
            change.apply()
        self.bought = True
        # NOTE: we have to store the upgrade buy sequence
        SaveLoadGame.bought_upgrades.append(self.name)