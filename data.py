from core import *


# Resources

seed = Resource(name="Seed",amount=0.0,max_amount=100.0)
fruit = Resource(name="Fruit",amount=0.0,max_amount=100.0)
plant = Resource(name="Plant",amount=0.0,max_amount=100.0)
water = Resource(name="Water",amount=0.0,max_amount=100.0)
wood = Resource(name="Wood",amount=0.0,max_amount=100.0)
stamina = Resource(name="Stamina",amount=0.0,max_amount=100.0)
fire = Resource(name="Fire",amount=0.0,max_amount=100.0)
brick = Resource(name="Brick",amount=0.0,max_amount=100.0)
clay = Resource(name="Clay",amount=0.0,max_amount=100.0)
house = Resource(name="House",amount=0.0,max_amount=1.0)

# Converters

Converter(name="Well"
    ,in_recipes=[
    ]
    ,out_recipes=[
        Recipe(resource=water,amount=0.5,min_amount=0.0),
    ])
Converter(name="Forest"
    ,in_recipes=[
        Recipe(resource=water,amount=0.5,min_amount=0.0),
        Recipe(resource=plant,amount=0.5,min_amount=5.0),
    ]
    ,out_recipes=[
        Recipe(resource=plant,amount=0.5,min_amount=0.0),
        Recipe(resource=wood,amount=0.5,min_amount=0.0),
    ])
Converter(name="Gather fruit"
    ,in_recipes=[
        Recipe(resource=stamina,amount=0.5,min_amount=0.0),
    ]
    ,out_recipes=[
        Recipe(resource=fruit,amount=0.5,min_amount=0.0),
    ])
Converter(name="Eat fruit"
    ,in_recipes=[
        Recipe(resource=fruit,amount=0.5,min_amount=0.0),
    ]
    ,out_recipes=[
        Recipe(resource=seed,amount=0.5,min_amount=0.0),
    ])
Converter(name="Garden"
    ,in_recipes=[
        Recipe(resource=water,amount=0.5,min_amount=0.0),
        Recipe(resource=seed,amount=0.5,min_amount=0.0),
    ]
    ,out_recipes=[
        Recipe(resource=plant,amount=0.5,min_amount=0.0),
    ])
Converter(name="Start a fire"
    ,in_recipes=[
        Recipe(resource=wood,amount=0.5,min_amount=5.0),
        Recipe(resource=stamina,amount=0.5,min_amount=50.0),
    ]
    ,out_recipes=[
        Recipe(resource=fire,amount=0.5,min_amount=0.0),
    ])
Converter(name="Fireplace"
    ,in_recipes=[
        Recipe(resource=wood,amount=0.5,min_amount=1.0),
        Recipe(resource=fire,amount=0.5,min_amount=5.0),
    ]
    ,out_recipes=[
        Recipe(resource=fire,amount=3.0,min_amount=0.0),
    ])
Converter(name="Dig clay"
    ,in_recipes=[
        Recipe(resource=stamina,amount=0.5,min_amount=20.0),
        Recipe(resource=water,amount=0.5,min_amount=5.0),
    ]
    ,out_recipes=[
        Recipe(resource=clay,amount=3.0,min_amount=0.0),
    ])
Converter(name="Furnace"
    ,in_recipes=[
        Recipe(resource=clay,amount=0.5,min_amount=20.0),
        Recipe(resource=fire,amount=0.5,min_amount=5.0),
    ]
    ,out_recipes=[
        Recipe(resource=brick,amount=3.0,min_amount=0.0),
    ])
Converter(name="Build house"
    ,in_recipes=[
        Recipe(resource=brick,amount=0.5,min_amount=20.0),
        Recipe(resource=stamina,amount=0.5,min_amount=5.0),
    ]
    ,out_recipes=[
        Recipe(resource=house,amount=0.1,min_amount=0.0),
    ])
Converter(name="Rest"
    ,in_recipes=[
        Recipe(resource=house,amount=0.0,min_amount=1.0),
    ]
    ,out_recipes=[
        Recipe(resource=stamina,amount=0.1,min_amount=0.0),
    ])
Converter(name="Sleep on the ground"
    ,in_recipes=[
    ]
    ,out_recipes=[
        Recipe(resource=stamina,amount=0.5,min_amount=0.0),
    ])