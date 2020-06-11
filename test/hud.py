# hud.py

from browser import document, svg



class Hud:
    tooltip = document['tooltip']
    rect = tooltip.getBoundingClientRect()
    width,height = rect.width,rect.height
    node_name = svg.text("", x=10, y=0, z=10, transform="translate(10)", font_size=20,text_anchor="start")

    tooltip <= node_name

    hover_node = None
    active_node = None
    tspans = []

    def create_tspan(text,dy='1em'):
        tspan = svg.tspan(text,x=0,dy=dy)
        Hud.tspans.append(tspan)
        return tspan

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
            Hud.tspans.clear()
            return
        else:
            Hud.hover_node = node
        Hud.node_name.attrs['transform'] = f"translate({Hud.hover_node.position[0] + 30})"
        Hud.node_name.attrs['y'] = Hud.hover_node.position[1] - 30
        Hud.node_name <= Hud.create_tspan(node.name)

        if node.in_recipes:
            Hud.node_name <= Hud.create_tspan('Needs:',dy=25)
            for in_recipe in node.in_recipes:
                text = f'{in_recipe.resource.name} [>{in_recipe.min_amount}]: {in_recipe.amount}'
                Hud.node_name <= Hud.create_tspan(text)
        if node.out_recipes:
            Hud.node_name <= Hud.create_tspan('Produces:',dy=25)
            for out_recipe in node.out_recipes:
                text = f'{out_recipe.resource.name}: {out_recipe.amount}'
                Hud.node_name <= Hud.create_tspan(text)