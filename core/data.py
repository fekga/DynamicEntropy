from core.resource import Resource
from core.converter import Converter
from core.upgrade import Upgrade, Cost
from core.change import Change, ChangeTo, ChangeBy

# Resources
stamina = Resource(name="Stamina",amount=100,max_amount=100)
dreaming = Resource(name="Dreaming",amount=0,max_amount=100)
seed = Resource(name="Seed",amount=0.0,max_amount=100)
fruit = Resource(name="Fruit",amount=0.0,max_amount=100)
plant = Resource(name="Plant",amount=0.0,max_amount=100)
water = Resource(name="Water",amount=0.0,max_amount=100)
wood = Resource(name="Wood",amount=0.0,max_amount=100)
fire = Resource(name="Fire",amount=0.0,max_amount=100)
brick = Resource(name="Brick",amount=0.0,max_amount=100)
clay = Resource(name="Clay",amount=0.0,max_amount=100)

# Converters
Converter(name="Wake up", unstoppable=True
    ,needs=[
        dreaming(amount=dreaming.max_amount, at_least=dreaming.max_amount),
    ]
    ,makes=[
        stamina(amount=stamina.max_amount)
    ])
sleep = Converter(name="Sleep", unstoppable=True
    ,needs=[
        stamina(at_most=1, amount=0),
        dreaming(amount=0),
    ]
    ,makes=[
        dreaming(amount=5),
    ])
Upgrade(name="House",
        costs=[
            Cost(resource=brick, amount=5),
            Cost(resource=stamina, amount=5),
        ],
        requires=[],
        changes=[
            ChangeBy(
                converter=sleep,
                needs=[],
                makes=[
                    dreaming(amount=20)
                ]
            )
        ]
)
Converter(name="Twiddling thumbs"
    ,needs=[
        stamina(amount=1),
    ]
    ,makes=[])
well = Converter(name="Well"
    ,needs=[
        stamina(amount=4)
    ]
    ,makes=[
        water(amount=1,at_least=0),
    ])
Upgrade(name="Well upgrade",
        costs=[
            Cost(resource=water, amount=10)
        ],
        requires=[],
        changes=[
            ChangeBy(
                converter=well,
                needs=[],
                makes=[
                    water(amount=2,at_least=0)
                ]
            )
        ]
)
Converter(name="Forest"
    ,needs=[
        water(amount=20,at_least=0),
        plant(amount=20,at_least=50),
    ]
    ,makes=[
        plant(amount=30,at_least=0),
    ])
Converter(name="Wood cutting"
    ,needs=[
        plant(amount=10,at_least=0),
        stamina(amount=10,at_least=0),
    ]
    ,makes=[
        wood(amount=6,at_least=0),
    ])
Converter(name="Gather fruit"
    ,needs=[
        stamina(amount=5,at_least=0),
    ]
    ,makes=[
        fruit(amount=10,at_least=0),
    ])
Converter(name="Eat fruit"
    ,needs=[
        fruit(amount=1,at_least=0),
    ]
    ,makes=[
        seed(amount=10,at_least=0),
    ])
Converter(name="Garden"
    ,needs=[
        seed(amount=5,at_least=0),
        water(amount=5,at_least=0),
    ]
    ,makes=[
        plant(amount=5,at_least=0),
    ])
Converter(name="Start a fire"
    ,needs=[
        wood(amount=5,at_least=50),
        stamina(amount=5,at_least=50),
    ]
    ,makes=[
        fire(amount=5,at_least=0),
    ])
Converter(name="Fireplace"
    ,needs=[
        wood(amount=5,at_least=10),
        fire(amount=5,at_least=50),
    ]
    ,makes=[
        fire(amount=30,at_least=0),
    ])
Converter(name="Dig clay"
    ,needs=[
        stamina(amount=5,at_least=0),
        water(amount=5,at_least=50),
    ]
    ,makes=[
        clay(amount=30,at_least=0),
    ])
Converter(name="Furnace"
    ,needs=[
        clay(amount=2,at_least=0),
        fire(amount=1,at_least=50),
    ]
    ,makes=[
        brick(amount=1,at_least=0),
    ])
