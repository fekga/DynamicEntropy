from core.resource import Resource
from core.converter import Converter
from core.upgrade import Upgrade, Cost
from core.change import Change

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
cotton = Resource(name="Cotton", amount=0, max_amount=100)
fabric = Resource(name="Fabric", amount=0, max_amount=100)
wheat = Resource(name="Wheat", amount=0, max_amount=100)
flour = Resource(name="Flour", amount=0, max_amount=100)
bread = Resource(name="Bread", amount=0, max_amount=100)
iron_ore = Resource(name="Iron ore", amount=0, max_amount=100)
iron = Resource(name="Iron", amount=0, max_amount=100)
tool = Resource(name="Tool", amount=0, max_amount=10)

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
            sleep.change_by(
                needs=[],
                makes=[
                    dreaming(amount=5)
                ]
            )
        ]
)
Upgrade(name="Bed",
        costs=[
            Cost(resource=wood, amount=50),
            Cost(resource=fabric, amount=50),
        ],
        requires=[],
        changes=[
            sleep.change_by(
                needs=[],
                makes=[
                    dreaming(amount=15)
                ]
            )
        ]
)
Converter(name="Twiddling thumbs"
    ,needs=[
        stamina(amount=1),
    ]
    ,makes=[])

water_source = Converter(name="Creek"
    ,needs=[
        stamina(amount=5)
    ]
    ,makes=[
        water(amount=1,at_least=0),
    ])
water_upgrade_road = Upgrade(name="Built road",
        costs=[
            Cost(resource=brick, amount=10)
        ],
        requires=[],
        changes=[
            water_source.change_by(
                needs=[
                    stamina(amount=-3)
                ],
                makes=[]
            )
        ]
)
water_upgrade_hole = Upgrade(name="Dig down to ground-water",
        costs=[
            Cost(resource=stamina, amount=100)
        ],
        requires=[],
        changes=[
            water_source.change_by(
                needs=[
                    stamina(amount=5)
                ],
                makes=[
                    water(amount=1)
                ],
            )
        ]
)
Upgrade(name="Build well",
        costs=[
            Cost(resource=stamina, amount=50),
            Cost(resource=brick, amount=25)
        ],
        requires=[ water_upgrade_road, water_upgrade_hole ],
        changes=[
            water_source.change_to(
                needs=[
                    stamina(amount=1)
                ],
                makes=[
                    water(amount=1)
                ],
                converter_new_name="Well"
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
wood_cutting = Converter(name="Wood cutting"
    ,needs=[
        plant(amount=10,at_least=0),
        stamina(amount=10,at_least=0),
    ]
    ,makes=[
        wood(amount=6,at_least=0),
    ])
Upgrade(name="Advanced handle",
        costs=[
            Cost(resource=fabric, amount=10)
        ],
        requires=[],
        changes=[
            wood_cutting.change_by(
                needs=[
                    stamina(amount=-5)
                ],
                makes=[]
            )
        ]
)

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
        dreaming(amount=0,at_most=0)
    ]
    ,makes=[
        seed(amount=10,at_least=0),
        stamina(amount=0.1)
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

dig_clay = Converter(name="Dig clay"
    ,needs=[
        stamina(amount=5,at_least=0),
        water(amount=5,at_least=50),
    ]
    ,makes=[
        clay(amount=3,at_least=0),
    ])
Upgrade(name="Use digger",
        costs=[
            Cost(resource=tool, amount=1)
        ],
        requires=[],
        changes=[
            dig_clay.change_to(
                needs=[stamina(amount=1)],
                makes=[clay(amount=3)]
            )
        ]
)

Converter(name="Clay furnace"
    ,needs=[
        clay(amount=2,at_least=0),
        fire(amount=1,at_least=50),
    ]
    ,makes=[
        brick(amount=1,at_least=0),
    ])
Converter(name="Cotton field"
    ,needs=[
        water(amount=1,at_least=0),
        seed(amount=0,at_least=10),
    ]
    ,makes=[
        cotton(amount=1),
    ])
Converter(name="Loom"
    ,needs=[
        cotton(amount=5,at_least=0),
        stamina(amount=3,at_least=0),
    ]
    ,makes=[
        fabric(amount=1),
    ])
Converter(name="Wheat field"
    ,needs=[
        water(amount=1,at_least=0),
        seed(amount=0,at_least=10),
    ]
    ,makes=[
        wheat(amount=1)
    ])
Converter(name="Mill"
    ,needs=[
        wheat(amount=1,at_least=0),
        stamina(amount=1),
    ]
    ,makes=[
        flour(amount=0.1),
    ])
Converter(name="Bread furnace"
    ,needs=[
        flour(amount=1),
        water(amount=0.3),
        fire(amount=1,at_least=20),
        stamina(amount=0.5)
    ]
    ,makes=[
        bread(amount=1),
    ])

iron_mine = Converter(name="Iron mine"
    ,needs=[
        stamina(amount=5)
    ]
    ,makes=[
        iron_ore(amount=.1)
    ])
Upgrade(name="Use pickaxe",
        costs=[
            Cost(resource=tool, amount=1)
        ],
        requires=[],
        changes=[
            iron_mine.change_by(
                needs=[stamina(-4)],
                makes=[]
            )
        ]
)
Upgrade(name="Build minecart",
        costs=[
            Cost(resource=tool, amount=1)
        ],
        requires=[],
        changes=[
            iron_mine.change_by(
                needs=[],
                makes=[iron_ore(.4)]
            )
        ]
)

Converter(name="Iron smelter"
    ,needs=[
        iron_ore(amount=1),
        fire(amount=5)
    ]
    ,makes=[
        iron(amount=.1)
    ])
Converter(name="Tool maker"
    ,needs=[
        iron(amount=5),
        fire(amount=1)
    ]
    ,makes=[
        tool(amount=1)
    ])