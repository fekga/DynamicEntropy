#test.py
from browser import document, svg, window
import math

circle = svg.circle(cx=270, cy=120, r=100, stroke="black",stroke_width="2", fill="green")

class Test:
    x=100

window.Test = Test
print("test:"+str(Test.x))
print("alma")