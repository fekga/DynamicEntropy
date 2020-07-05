# ending.py
from browser import document, html
from gui.front_page import *

# Call for final scene
def trigger_ending_scene():
    content = create_front_blank_page("THE END") # already added to html

    # content <= html.IFRAME(width="100%",height="100%",src="http://www.youtube.com/embed/5CdoyqsNdaE?&autoplay=1")
    content <= html.IMG(src="images/tenor.gif", width=498, alt="Finally awake...")

    # content <= html.DIV("End of Dynamic Entropy " + document['version'].text)
    #
    # img = html.IMG(src="images/dynamic_entropy_xkcd.png")
    # img_link = html.A(href="https://xkcd.com/2318/", target="_blank")
    # img_link <= img
    # content <= img_link
    content <= html.BR()
    content <= "Hey, you! You're finally awake."
    content <= html.BR()
    content <= "You were trying to cross the border, right? Walked right into that imperial ambush, same as us."
    content <= html.BR()
    content <= "To be continued..."
    content <= html.BR()

    btn = html.BUTTON("Thanks for playing")
    btn.bind("click", lambda e, content=content: remove_front_page(content))
    content <= btn
