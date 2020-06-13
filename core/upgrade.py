# upgrade.py
from dataclasses import dataclass, field
from typing import List, Type
from core.change import Change
from core.resource import Resource

empty = lambda: field(default_factory=list)

@dataclass
class Upgrade:
    name: str
    changes: List[Change]
    costs: List[Resource] = empty()
    requires: List[Type['Upgrade']] = empty()
    bought: bool = False
    upgrades = list()

    def __post_init__(self):
        Upgrade.upgrades.append(self)

    def __repr__(self):
        if self.bought:
            return f'{self.name} {{Bought}}'
        s = []
        if self.costs:
            s += ['Costs: ' + ', '.join(map(str,self.costs))]
        if self.requires:
            s += ['Requires: ' + ', '.join(map(lambda e:e.name,self.requires))]
        if self.changes:
            s += ['Changes: ' + ', '.join(map(str,self.changes))]
        return f'{self.name} {{{" | ".join(s)}}}'

    def buy(self):
        if self.bought:
            return False
        for requirement in self.requires:
            if not requirement.bought:
                return False
        for cost in self.costs:
            if not cost.resource.can_take(cost.amount):
                return False
        for cost in self.costs:
            cost.resource.take(cost.amount)
        for change in self.changes:
            change.apply()
        self.bought = True
        return True