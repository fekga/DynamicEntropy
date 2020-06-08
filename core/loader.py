# loader.py

from core import Resource, Recipe, Converter
import json

converters = []
with open('data.json','r') as f:
    d = json.load(f)

    for resource in d['resources']:
        name = resource['name']
        max_amount = float(resource.get('max_amount',float('inf')))
        Resource(name,max_amount)

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