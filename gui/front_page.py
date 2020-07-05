# front_page.py
from browser import document, html

def create_front_blank_page(text):
    content = html.DIV(id="front_page", style={
        'width': '80%', "height": "70%", "border": "3px solid #000",
        'background': 'white',
        'position': 'absolute', 'top': '50px',
        'margin': "50px", 'text-align': 'center',
    })
    content <= html.DIV(text, style={
        'margin': "50px", 'font-size': '20px'
    })
    content.attrs['class'] = "appear"
    document['content'] <= content
    return content

def remove_front_page(front_page):
    front_page.attrs['class'] = "disappear"
    # Late remove
    front_page.bind("animationend", front_page.remove)