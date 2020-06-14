from core.resource import Resource
from core.converter import Converter
from core.upgrade import Upgrade, Cost
from core.change import Change, ChangeTo, ChangeBy

# Resources
seed = Resource(name="Seed",amount=0.0,max_amount=10.0)
fruit = Resource(name="Fruit",amount=0.0,max_amount=10.0)
plant = Resource(name="Plant",amount=0.0,max_amount=10.0)
water = Resource(name="Water",amount=0.0,max_amount=10.0)
wood = Resource(name="Wood",amount=0.0,max_amount=10.0)
stamina = Resource(name="Stamina",amount=0.0,max_amount=10.0)
fire = Resource(name="Fire",amount=0.0,max_amount=10.0)
brick = Resource(name="Brick",amount=0.0,max_amount=10.0)
clay = Resource(name="Clay",amount=0.0,max_amount=10.0)

# Converters
well = Converter(name="Well"
    ,needs=[
    ]
    ,makes=[
        water(amount=0.1,at_least=0.0),
    ])
Upgrade(name="Well upgrade",
        costs=[
            Cost(resource=water, amount=1)
        ],
        requires=[],
        changes=[
            ChangeBy(
                converter=well,
                needs=[],
                makes=[
                    water(amount=0.2,at_least=0)
                ]
            )
        ]
)
Converter(name="Forest"
    ,needs=[
        water(amount=2,at_least=0.0),
        plant(amount=2,at_least=5.0),
    ]
    ,makes=[
        plant(amount=3,at_least=0.0),
    ])
Converter(name="Wood cutting"
    ,needs=[
        plant(amount=1,at_least=0.0),
        stamina(amount=1,at_least=0.0),
    ]
    ,makes=[
        wood(amount=1,at_least=0.0),
    ])
Converter(name="Gather fruit"
    ,needs=[
        stamina(amount=1,at_least=0.0),
    ]
    ,makes=[
        fruit(amount=1,at_least=0.0),
    ])
Converter(name="Eat fruit"
    ,needs=[
        fruit(amount=0.1,at_least=0.0),
    ]
    ,makes=[
        seed(amount=0.1,at_least=0.0),
    ])
Converter(name="Garden"
    ,needs=[
        seed(amount=0.5,at_least=0.0),
        water(amount=0.5,at_least=0.0),
    ]
    ,makes=[
        plant(amount=0.5,at_least=0.0),
    ])
Converter(name="Start a fire"
    ,needs=[
        wood(amount=0.5,at_least=5.0),
        stamina(amount=0.5,at_least=5.0),
    ]
    ,makes=[
        fire(amount=0.5,at_least=0.0),
    ])
Converter(name="Fireplace"
    ,needs=[
        wood(amount=0.5,at_least=1.0),
        fire(amount=0.5,at_least=5.0),
    ]
    ,makes=[
        fire(amount=3.0,at_least=0.0),
    ])
Converter(name="Dig clay"
    ,needs=[
        stamina(amount=0.5,at_least=0.0),
        water(amount=0.5,at_least=5.0),
    ]
    ,makes=[
        clay(amount=3.0,at_least=0.0),
    ])
Converter(name="Furnace"
    ,needs=[
        clay(amount=0.2,at_least=0.0),
        fire(amount=0.1,at_least=5.0),
    ]
    ,makes=[
        brick(amount=0.1,at_least=0.0),
    ])
rest = Converter(name="Rest"
    ,needs=[
    ]
    ,makes=[
        stamina(amount=0.1,at_least=0.0),
    ])
Upgrade(name="House",
        costs=[
            Cost(resource=brick, amount=5),
            Cost(resource=stamina, amount=5),
        ],
        requires=[],
        changes=[
            ChangeBy(
                converter=rest,
                needs=[],
                makes=[
                    stamina(amount=0.1)
                ]
            )
        ]
)