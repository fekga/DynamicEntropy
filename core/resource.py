# resource.py
from dataclasses import dataclass
from core.recipe import Recipe

float_eps = 1e-10

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
        return self.amount >= amount - float_eps

    def can_take_recipe(self, recipe):
        return (self.can_take(recipe.amount)
        and self.amount >= recipe.at_least - float_eps
        and self.amount + self._delay <= recipe.at_most + float_eps)

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


