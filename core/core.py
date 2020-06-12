# core.py

from dataclasses import dataclass, field
from dataclasses import *
from typing import List,Type

empty = lambda: field(default_factory=list)
foreach = lambda f,k: any(map(f,k))

def split(cond, iterable):
    if cond is None:
        cond = lambda x: True
    true, false = [], []
    for x in iterable:
        (false, true)[cond(x)].append(x)
    return true,false

@dataclass
class Resource:
    name: str
    amount: float = 0
    max_amount: float = float('inf')
    resources = list()
    _delay: float = 0

    def __post_init__(self):
        Resource.resources.append(self)

    def can_take(self, amount):
        return amount <= self.amount

    def take(self, amount):
        if self.can_take(amount):
            self.amount -= amount

    def give(self, amount):
        self._delay += amount

    def update(self):
        self.amount = min(self.max_amount,self.amount + self._delay)
        self._delay = 0

    def __repr__(self):
        amount,max_amount = int(self.amount),int(self.max_amount)
        amount_str = f'[{amount}/{max_amount}]'
        if self.max_amount == float('inf'):
            amount_str = f'{amount}'
        return f'{self.name} {amount_str}'

    def __call__(self, amount=0,at_least=0,at_most=float('inf')):
        ''' Creates recipe '''
        return Recipe(self,amount,at_least,at_most)

@dataclass
class Recipe:
    resource: Resource
    amount: float = 0
    at_least: float = 0
    at_most: float = float('inf')

    def __iadd__(self, other):
        if other.resource == self.resource:
            self.amount += other.amount
            self.at_least += other.at_least
            self.at_most += other.at_most
        else:
            print('Warning: valami nem oke bastya')
        return self

    def __repr__(self):
        at_least_str = f'{self.at_least}' if self.at_least > 0 else ''
        at_most_str = f'{self.at_most}' if self.at_most < float('inf') else ''
        at_least_most = f'[{at_most_str}>={at_least_str}] ' if at_least_str+at_most_str else ''
        return f'{self.resource.name} {at_least_most}{self.amount}'

    def __eq__(self, other):
        return self.resource.name == other.resource.name

@dataclass
class Converter:
    name: str
    needs: List[Recipe] = empty()
    makes: List[Recipe] = empty()
    converters = list()
    OK,STOPPED,NO_INPUT,MAX_OUTPUT = range(4)
    state = OK

    def __post_init__(self):
        Converter.converters.append(self)

    def start(self):
        self.state = Converter.OK

    def stop(self):
        self.state = Converter.STOPPED

    def is_stopped(self):
        return self.state == Converter.STOPPED

    def still_hidden(self):
        print(self.name,self.needs)
        if self.needs is not None:
            for recipe in self.needs:
                if recipe.resource.amount <= 0:
                    return True
        print(self.name,'alma')
        return False

    def update(self):
        if self.state == Converter.STOPPED:
            return
        for recipe in self.makes:
            resource = recipe.resource
            if resource.amount >= resource.max_amount:
                self.state = Converter.MAX_OUTPUT
                return
        for recipe in self.needs:
            resource = recipe.resource
            if (not resource.can_take(recipe.amount) 
                or resource.amount < recipe.at_least
                or resource.amount > recipe.at_most):
                self.state = Converter.NO_INPUT
                return
        self.state = Converter.OK
        for recipe in self.needs:
            recipe.resource.take(recipe.amount)
        for recipe in self.makes:
            recipe.resource.give(recipe.amount)

    def change_by(self, *, needs=None, makes=None):
        return ChangeBy(self,needs,makes)

    def change_to(self, *, needs=None, makes=None):
        return ChangeTo(self,needs,makes)

    def __repr__(self):
        s = []
        if self.needs:
            s += ['Needs: ' + ', '.join(map(str,self.needs))]
        if self.makes:
            s += ['Makes: ' + ', '.join(map(str,self.makes))]
        return f'{self.name} {{{" | ".join(s)}}}'

@dataclass
class Change:
    converter: Converter
    needs: List[Recipe] = empty()
    makes: List[Recipe] = empty()

    def apply(self):
        def _upgrade(current_recipes,upgrade_recipes):
            if upgrade_recipes is not None:
                for upgrade in upgrade_recipes:
                    for i,current in enumerate(current_recipes):
                        if upgrade.resource == current.resource:
                            if self.delta:
                                current_recipes[i] += upgrade
                            else:
                                current_recipes[i] = upgrade
        _upgrade(self.converter.needs,self.needs)
        _upgrade(self.converter.makes,self.makes)

    def __repr__(self):
        change_type = 'by' if self.delta else 'to'
        s = []
        if self.needs:
            s += ['Needs: ' + ', '.join(map(str,self.needs))]
        if self.makes:
            s += ['Makes: ' + ', '.join(map(str,self.makes))]
        return f'{self.converter.name} {change_type} {{{" | ".join(s)}}}'

@dataclass
class ChangeTo(Change):
    delta: bool = False

    def __repr__(self):
        return super().__repr__()

@dataclass
class ChangeBy(Change):
    delta: bool = True

    def __repr__(self):
        return super().__repr__()

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

