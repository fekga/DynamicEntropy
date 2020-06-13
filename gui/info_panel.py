# info_panel.py
from browser import svg, document

class InfoPanelItem:
    def __init__(self, resource, line_pos):
        info_panel = document['info_panel']
        self.resource = resource
        self.line_pos = line_pos
        line_height = 25
        # Name string
        self.text = svg.text(resource.name,
                             x=10, y=line_pos*line_height+20,
                             font_size=20, text_anchor="start")
        # Progress rectangle
        self.rect_width = 100
        rect_right_margin = 5
        window_width = info_panel.parent.getBoundingClientRect().width
        rect_x_start = window_width-self.rect_width-rect_right_margin
        rect_y_start = line_pos*line_height+7
        rect_height = 15
        rect_rx = 5
        self.rect = svg.rect(x=rect_x_start,
                             y=rect_y_start, width=self.rect_width,
                             height=rect_height, rx=0)
        self.number_text = svg.text("",
                                    x=window_width-rect_right_margin-(self.rect_width/2),
                                    y=line_pos * line_height + 20,
                                    font_size=16, text_anchor="middle", font_weight="bold")
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

        # SVG elements
        info_panel <= clip
        info_panel <= g
        info_panel <= self.text
        info_panel <= self.number_text




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
            self.rect.attrs["width"] = self.rect_width*ratio
            self.rect.attrs["fill"] = f"rgb({r},{g},0)"
            self.number_text.text = f"{int(amount)} / {int(max_amount)}"