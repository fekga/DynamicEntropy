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

    hover_node = None
    active_node = None
    tspans = []

    def set_active(node):
        Hud.active_node = node if node != Hud.active_node else None
        Hud.show_info(node)

    def show_info(node):
        if node is None:
            return
        if Hud.active_node is not None:
            node = Hud.active_node
        elif node == Hud.hover_node:
            Hud.hover_node = None
            Hud.node_name.text = ''
            for e in Hud.tspans:
                del e
            return
        else:
            Hud.hover_node = node
        Hud.tspans = []
        
        Hud.node_name.text = node.converter.name

        if node.in_recipes:
            Hud.node_name <= create_tspan('Needs:',x=10,dy=25)
            for in_recipe in node.converter.needs:
                text = f'{in_recipe.resource.name} [>={in_recipe.at_least}]: {in_recipe.amount:.2f}'
                Hud.node_name <= create_tspan(test,x=20)
        if node.out_recipes:
            Hud.node_name <= create_tspan('Produces:',x=10,dy=25)
            for out_recipe in node.converter.makes:
                text = f'{out_recipe.resource.name}: {out_recipe.amount:.2f}'
                Hud.node_name <= create_tspan(text,x=20)
        Hud.node_name.attrs['y'] = Hud.height - 20 - (len(Hud.tspans)-2) * 20 - 50