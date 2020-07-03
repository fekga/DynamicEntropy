# change.py
from dataclasses import dataclass, field
from typing import List,Type
from core.recipe import Recipe

empty = lambda: field(default_factory=list)

@dataclass
class Change:
    converter: Type['Converter']
    delta: bool
    needs: List[Recipe] = empty()
    makes: List[Recipe] = empty()
    converter_new_name: str = ""

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
        if self.converter_new_name:
            self.converter.changeName(self.converter_new_name)

    def __str__(self):
        if not self.needs and not self.makes:
            return ''
        text = f'{self.converter.name} will '
        s = []
        if self.converter_new_name:
            s += [f'become {self.converter_new_name}']

        if self.needs:
            s += [f'require {abs(need.amount)}{[" more"," less"][need.amount<0]if self.delta else""} {need.resource.name}' for need in self.needs]

        if self.makes:
            s += [f'create {abs(make.amount)}{[" more"," less"][make.amount<0]if self.delta else""} {make.resource.name}' for make in self.makes]

        text += ', '.join(s)
        return text
