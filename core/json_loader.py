# loader.py

from test.core import Resource, Recipe, Converter
import json

converters = []
with open('settlers.json','r') as f:
    d = json.load(f)

    for resource in d['resources']:
        name = resource['name']

        amount = float(resource.get('amount',0))
        max_amount = float(resource.get('max_amount',float('inf')))

        Resource(name,amount=amount,max_amount=max_amount)

    for converter in d['converters']:
        name = converter['name']
        inputs = converter['input']
        outputs = converter['output']

        input_recipes = []
        output_recipes = []
        for recipe in inputs:
            resource = recipe['resource']
            amount = float(recipe['amount'])
            min_amount = float(recipe.get('min_amount',0))
            input_recipes.append(Recipe(Resource.resources[resource],amount,min_amount))
        for recipe in outputs:
            resource = recipe['resource']
            amount = float(recipe['amount'])
            min_amount = float(recipe.get('min_amount',0))
            output_recipes.append(Recipe(Resource.resources[resource],amount,min_amount))
        Converter(name,input_recipes,output_recipes)


for resource in Resource.resources:
    print(f'{resource.name.lower().replace(" ","_")} = Resource(name="{resource.name}",amount={resource.amount},max_amount={resource.max_amount})')

for converter in Converter.converters.values():
    print(f'Converter(name="{converter.name}"\n\t,in_recipes=[')
    for recipe in converter.in_recipes:
        print(f'\t\tRecipe(resource={recipe.resource.name.lower().replace(" ","_")},amount={recipe.amount},min_amount={recipe.min_amount}),')
    print('\t]\n\t,out_recipes=[')
    for recipe in converter.out_recipes:
        print(f'\t\tRecipe(resource={recipe.resource.name.lower().replace(" ","_")},amount={recipe.amount},min_amount={recipe.min_amount}),')
    print('\t])')