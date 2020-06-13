# recipe.py
from dataclasses import dataclass
from typing import Type

@dataclass
class Recipe:
    resource: Type["Resource"]
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