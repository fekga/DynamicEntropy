# info_panel.py
from browser import svg, document

class InfoPanelItem:
    def __init__(self, resource, line_pos, nodes):
        info_panel = document['info_panel']
        self.resource = resource
        self.line_pos = line_pos
        line_height = 25
        voffset = 5
        # Name string HACK:dominant-baseline
        self.text = svg.text(resource.name,
                             x=10, y=line_pos*line_height+voffset,
                             font_size=20, text_anchor='start' )
        self.text.attrs['dominant-baseline'] = "hanging"
        # Progress rectangle
        self.rect_width = 100
        rect_right_margin = 5
        window_width = info_panel.parent.getBoundingClientRect().width
        rect_x_start = window_width-self.rect_width-rect_right_margin
        rect_y_start = line_pos*line_height+voffset
        rect_height = 15
        rect_rx = 5
        self.rect = svg.rect(x=rect_x_start,
                             y=rect_y_start, width=self.rect_width,
                             height=rect_height, rx=0)
        self.number_text = svg.text("",
                                    x=window_width-rect_right_margin-(self.rect_width/2),
                                    y=line_pos * line_height+voffset + 2,
                                    font_size=16, text_anchor="middle", font_weight="bold")
        self.number_text.attrs['dominant-baseline'] = "hanging"
        # Contour rectangle
        id_str = "contour_" + str(line_pos)
        clip_id_str = "clip_rect_"+str(line_pos)
        clip_rect = svg.rect(x=rect_x_start,
                                y=rect_y_start, width=self.rect_width,
                                height=rect_height, rx=rect_rx,
                                stroke="black", style={"fill-opacity":"0","stroke-opacity":"1"},
                                id=clip_id_str)
        # 'use' structure
        clip = svg.clipPath(id=id_str)
        clip <= clip_rect
        g = svg.g(style={"clip-path": "url(#"+id_str+")"})
        g <= self.rect
        g <= svg.use(href="#"+clip_id_str)

        self.border = svg.rect(id="itemContainer_rect",
                               x=0, y=line_pos * line_height,
                               width=window_width, height=line_height,
                               rx=rect_rx, fill="grey",
                               style={"fill-opacity":"0.5"}
                               )
        self.border.attrs['visibility'] = 'hidden'
        info_panel <= self.border

        # SVG elements
        info_panel <= clip
        info_panel <= g
        info_panel <= self.text
        info_panel <= self.number_text

        self.text.bind("mouseover", lambda ev: self.highlight_connections(nodes))
        self.text.bind("mouseout", lambda ev: self.remove_highlight_connections(nodes))

    def draw(self):
        max_amount = self.resource.max_amount
        if max_amount != 0:
            amount = self.resource.amount
            ratio = amount / max_amount
            th = 0.8
            if ratio < th:
                r = 0
                g = 255
            else:
                r = (ratio-th) / (1-th) * 255
                g = 255 - r
            ratio = max(ratio,0)
            self.rect.attrs["width"] = self.rect_width*ratio
            self.rect.attrs["fill"] = f"rgb({r},{g},0)"
            self.number_text.text = f"{int(amount)} / {int(max_amount)}"

    def highlight_item(self):
        self.border.attrs['visibility'] = 'visible'

    def highlight_item_remove(self):
        self.border.attrs['visibility'] = 'hidden'

    def highlight_connections(self, nodes):
        self.highlight_item()

        for node in nodes:
            # Nodes to manual property set
            node.manual_property_set = True

            needed = False
            for need in node.converter.needs:
                if need.resource == self.resource and need.amount > 0:
                    needed = True
            makes = False
            for make in node.converter.makes:
                if make.resource == self.resource and make.amount > 0:
                    makes = True
            if needed and makes:
                node.highlight_node(color="yellow", forced=True)
            elif needed:
                node.highlight_node(color="red", forced=True)
            elif makes:
                node.highlight_node(color="lightgreen", forced=True)
            else:
                node.remove_highlight_node(forced=True)

            # Connection
            for connection in node.connections:
                connection.manual_property_set = True
                if self.resource == connection.resource:
                    connection.drawConnectionAsActive(forced=True)
                else:
                    connection.drawConnectionAsInactive(forced=True)

    def remove_highlight_connections(self, nodes):
        self.highlight_item_remove()

        for node in nodes:
            # Nodes to automatic property set
            node.manual_property_set = False

            node.remove_highlight_node()

            # Connection
            for connection in node.connections:
                connection.manual_property_set = False