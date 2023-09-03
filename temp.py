from taipy.gui import Gui

hii = 'hey'
hi = f'{hii} /n '
page = """<|{hii}|>
heyy
"""

Gui(page=page).run()