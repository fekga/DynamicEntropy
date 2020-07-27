# info_panel.py
from browser import svg, document

from gui.info_panel_item import InfoPanelItem

class InfoPanel:
    def __init__(self, resources, nodes):
        self.info_area = document['info_area'] # container of the whole info panel elements NOTE: don't use if not necessary
        self.info_panel = document['info_panel']
        self.all_nodes = nodes # store

        item_height = 25
        window_width = self.info_panel.parent.getBoundingClientRect().width

        # Init resource items
        self.items = []
        for idx, res in enumerate(resources):
            item = InfoPanelItem(resource=res, line_height=item_height, line_width=window_width)
            self.info_panel <= item.graphic_container
            self.items.append(item)

    def update_item_positions(self):
        height = 0
        for item in self.items:
            if not item.hidden:
                item.graphic_container.attrs['transform'] = f'translate(0,{height})'
                height += item.item_height
        self.info_area.attrs['style'] = f'height:{height}px;' # update the html container element

    def draw(self):
        for item in self.items:
            if item.hidden:
                item.hidden = item.stay_hidden(self.all_nodes)
                if not item.hidden:
                    self.update_item_positions() # update list
            item.draw()