from taipy.gui import Gui
import db
 
resources = iter(db.show_courses())
free_stuff = iter(db.show_FreeStuff())
roadmaps = iter(db.show_roadmaps())


page_1 = """

<|navbar|>
#Home
"""

page_2 = """
<|navbar|>
#Resources
<|{resource['image']}|image|label=this is an image|on_action=function_name|>
"""

page_3 = """
<|navbar|>
#Free Stuff
<|{course['image']}|image|label=this is an image|on_action=function_name|>"""

page_4 = """
<|navbar|>
#Roadmaps
<|{roadmap['image']}|image|label=this is an image|on_action=function_name|>"""

page_5 = """
<|navbar|>
<|{Certificate}|file_selector|>
#Certificates NFT logic goes here"""

if __name__ == "main":
    pages = {
        "/":page_1,
        "Resources":page_2,
        "Free_Stuff":page_3,
        "Roadmaps":page_4,
        "Certificates":page_5
    }
    gui=Gui(pages = pages)
    gui.run(dark_mode=True)


