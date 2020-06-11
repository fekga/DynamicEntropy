# core.py

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

class Converter:
    converters = dict()
    # States
    OK = 1 << 0
    NO_INPUT = 1 << 1
    MAX_OUTPUT = 1 << 2
    STOPPED = 1 << 3

    def __init__(self, name, in_recipes, out_recipes, upgrades=None):
        self.name = name
        self.in_recipes = in_recipes
        self.out_recipes = out_recipes
        if upgrades is None:
            upgrades = []
        self.upgrades = upgrades
        Converter.converters[name] = self
        self.state = Converter.STOPPED

    def still_locked(self):
        for rec in self.in_recipes:
            res, need, min_amount = rec.resource, rec.amount, rec.min_amount
            if res.amount > 0 :
                return False
            else:
                return True

    def update(self):
        self.try_upgrade(0)
        if self.state == Converter.STOPPED:
            return
        for rec in self.out_recipes:
            res,prod = rec.resource,rec.amount
            if res.amount >= res.max_amount:
                self.state = Converter.MAX_OUTPUT
                return
        for rec in self.in_recipes:
            res,need,min_amount = rec.resource,rec.amount,rec.min_amount
            if not res.can_take(need) or res.amount < min_amount:
                self.state = Converter.NO_INPUT
                return
        self.state = Converter.OK
        for rec in self.in_recipes:
            res,need = rec.resource,rec.amount
            res.take(need)
        for rec in self.out_recipes:
            res,prod = rec.resource,rec.amount
            res.give(prod)

    def changeRecipies(self, basic_recipies, change_recipies):
        for change in change_recipies:
            resource, change_amount, change_min_amount= change.resource, change.amount, change.min_amount
            for rec in basic_recipies:
                if rec.resource == resource:
                    rec.amount += change_amount
                    rec.min_amount += change_min_amount
                    break
            else:
                print("Implement me: upgrade, recipe error:", resource)
    def do_upgrade(self,upgrade):
        self.changeRecipies(self.in_recipes, upgrade.in_change)
        self.changeRecipies(self.out_recipes, upgrade.out_change)
        upgrade.upgraded = True
        print("upgraded")

    def try_upgrade(self, upgradeIdx):
        if 0 <= upgradeIdx < len(self.upgrades):
            upgrade = self.upgrades[upgradeIdx]
            if upgrade.upgraded:
                return False
            for cost in upgrade.cost:
                resource, price = cost.resource,cost.amount
                if not resource.can_take(price):
                    return False
            for cost in upgrade.cost:
                resource, price = cost.resource,cost.amount
                resource.take(price)
            self.do_upgrade(upgrade)




