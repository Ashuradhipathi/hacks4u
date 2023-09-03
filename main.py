from taipy.gui import Gui, navigate

index = """"<|menu|label=Menu|lov={[('Page-1', 'Page 1'), ('Page-2', 'Page 2')]}|on_action=on_menu|>"""
page_1 =  """
#TAIPY GUI TUTORIALS - Layouts

<|Expandable Description|expandable|expanded=False|
##How does it work? 
<|layout|columns= 1 3 2|

<|#Resources|>

<|#Courses|>

<|#Roadmaps|>
|>
|>
"""

page_2 = """
<|layout|columns=1 1 1|

    <|
###FIRST COLUMN

    |>

    <|
###SECOND COLUMN

    |>

    <|
###THIRD COLUMN
Button 1:  
 

Button 2:  


Button 3:  


|> 
|>
"""

def on_menu(state, var_name, function_name, info):
    page = info['args'][0]
    navigate(state, to=page)

if __name__ == '__main__':
    pages = {
        "/":index,
        "Page-1" : page_1,
        "Page-2": page_2
    }
    gui = Gui(pages=pages)
    gui.run(dark_mode=False)

