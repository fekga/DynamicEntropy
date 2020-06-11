# hud.py

from browser import document, svg

def create_tspan(text,x,dy='1em'):
    tspan = svg.tspan(text,x=x,dy=dy)
    Hud.tspans.append(tspan)
    return tspan

class Hud:
    panel = document['panel']
    rect = panel.parent.getBoundingClientRect()
    width,height = rect.width,rect.height
    node_name = svg.text("", x=10, y=0, z=10, font_size=20,text_anchor="start")

    panel <= node_name

    last_node = None
    tspans = []

    def show_info(node):
        if node == Hud.last_node:
            Hud.last_node = None
            Hud.node_name.text = ''
            for e in Hud.tspans:
                del e
            return
        Hud.tspans = []
        Hud.last_node = node
        Hud.node_name.text = node.name

        if node.in_recipes:
            Hud.node_name <= create_tspan('Needs:',x=10,dy=25)
            for in_recipe in node.in_recipes:
                text = f'{in_recipe.resource.name} [>{in_recipe.min_amount}]: {in_recipe.amount}'
                Hud.node_name <= create_tspan(text,x=20)
        if node.out_recipes:
            Hud.node_name <= create_tspan('Produces:',x=10,dy=25)
            for out_recipe in node.out_recipes:
                text = f'{out_recipe.resource.name}: {out_recipe.amount}'
                Hud.node_name <= create_tspan(text,x=20)
        Hud.node_name.attrs['y'] = Hud.height - 20 - (len(Hud.tspans)-2) * 20 - 50