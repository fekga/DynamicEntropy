from browser import document, svg

title = svg.text('Tintiboy TM', x=70, y=25, font_size=22,
                 text_anchor="middle")
circle = svg.circle(cx=70, cy=120, r=40,
                    stroke="black",stroke_width="2",fill="red")
panel = document['panel']
panel <= title
panel <= circle