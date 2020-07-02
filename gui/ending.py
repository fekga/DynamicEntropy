# ending.py
from browser import document, html
from gui.front_page import create_front_blank_page

# Call for final scene
def trigger_ending_scene():
    content = create_front_blank_page("THE END") # already added to html

    content <= html.DIV("End of Dynamic Entropy " + document['version'].text)

    img = html.IMG(src="images/dynamic_entropy_xkcd.png")
    img_link = html.A(href="https://xkcd.com/2318/", target="_blank")
    img_link <= img
    content <= img_link
    content <= html.BR()

    btn = html.BUTTON("Thanks for playing")
    btn.bind("click", lambda e, content=content: content.remove())
    content <= btn
