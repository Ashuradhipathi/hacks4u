from taipy.gui import Gui, navigate
import db
from certificate import *

def list_to_string(input_list):
    result = ""
    for item in input_list:
        result += str(item) + "\n\n"
    return result



index = """"<|menu|label=Menu|lov={[('Page-1', 'Home'), ('Page-2', 'Courses'), ('Page-3','Resources'),('Page-4','Roadmaps'),('Page-5','Certificates'),('https://github.com/mopasha1/hacks4u','Github_Repo'),('https://docs.taipy.io/en/latest/','Taipy_Documentation')]}|on_action=on_menu|>"""
page_1 =  """
#Hacks For U


<|layout|columns= 2 2 2 1 1|

<|#Resources

*Resources*|>

<|#Courses|>

<|#Roadmaps|>

<|#Github|>

<|#Taipy Documentation|>


|>
"""

course_title = []
course_desc = []
course_link = []
courses_ = db.show_courses()
for course in courses_:
    course_title.append(course['Title'])
    course_desc.append(course['Description'])
    course_link.append(course['Link'])

Course_Title = list_to_string(course_title)
Course_Desc = list_to_string(course_desc)
Course_Link = list_to_string(course_link)

page_2 = """
<|layout|columns=1 1 1|

    <|
###Title
<|{Course_Title}|>

    |>

    <|
###Go To 
<|{Course_Link}|>

    |>

    <|
###A little info
<|{Course_Desc}|>


|> 
|>
"""


resource_title = []
resource_desc = []
resource_link = []
resources_ = db.show_FreeStuff()
for resource in resources_:
    resource_title.append(resource['Title'])
    resource_desc.append(resource['Description'])
    resource_link.append(resource['Link'])

Resource_Title = list_to_string(resource_title)
Resource_Desc = list_to_string(resource_desc)
Resource_Link = list_to_string(resource_link)

page_3 = """
<|layout|columns=1 1 1|

    <|
###Title
<|{Resource_Title}|>

    |>

    <|
###Go To 
<|{Resource_Link}|>

    |>

    <|
###A little info
<|{Resource_Desc}|>


|> 
|>
"""


Roadmaps_title = []
Roadmaps_desc = []
Roadmaps_link = []
Roadmaps_ = db.show_roadmaps()
for roadmap in Roadmaps_:
    Roadmaps_title.append(roadmap['Title'])
    Roadmaps_desc.append(roadmap['Description'])
    Roadmaps_link.append(roadmap['Link'])

Roadmap_Title = list_to_string(Roadmaps_title)
Roadmap_Desc = list_to_string(Roadmaps_desc)
Roadmap_Link = list_to_string(Roadmaps_link)

page_4 = """
<|layout|columns=1 1 1|

    <|
###Title
<|{Roadmap_Title}|>

    |>

    <|
###Go To 
<|{Roadmap_Link}|>

    |>

    <|
###A little info
<|{Roadmap_Desc}|>


|> 
|>
"""

User_address = ""
User_name = ""
Cert_name = ""
Cert_desc = ""
image_url = ""
User_id = ""
Cert_id = ""
mint_progress = ""
minter_address="0xf8d6e0586b0a20c7"

img=''
crt_name=''
name=''
desc=''




page_5 = """



<|Create Mint|expandable|expanded=True|
# Certificates NFT Mint


<|{User_address}|input|label=Enter your Flow Account address|><br />
<|{User_name}|input|label=Enter your name|><br />
<|{Cert_name}|input|label=Enter Certification name|><br />
<|{Cert_desc}|input|label=Tell us about it|><br />
<|{image_url}|input|label=Enter the Certification image url|><br />
<| {image_url}|><br />
<|Mint|button|on_action=Mint|>

<|{mint_progress}|>
|>

<|Find Your NFT|expandable|expanded=False|
<|{User_id}|input|label=Enter your Flow Account address|><br />
<|{Cert_id}|input|label=Enter a Certification ID|><br />
<|Retrieve|button|on_action=Retrieve|><br />
|>
## <|{name}|><br />
## <|{crt_name}|><br />
## <|{desc}|><br />
## <|{img}|><br />
"""


def Mint(state):
    print(state.User_address)
    metadata = {"Name": state.User_name,
            "Cert_name": state.Cert_name,
            "Desc": state.Cert_desc,
            "img": state.image_url
            }
    # createCollection(state.User_address, name='Moiz')
    b = MintCert(minter_address, state.User_address, metadata)

    asyncio.run(b.run(ctx = Config(r"C:\Users\moizp\Documents\projects\hacks4u\flow.json", 'emulator-account')))

    mint_progress="Success!"
    

def Retrieve(state):
    my_data = retriveData(state.User_id,state.Cert_id)
    state.name = my_data['Name']
    state.img=my_data['img']
    state.desc=my_data['Desc']
    state.crt_name=my_data['Cert_name']
    
        

def on_menu(state, var_name, function_name, info):
    page = info['args'][0]
    navigate(state, to=page)

if __name__ == '__main__':
    pages = {
        "/":index,
        "Page-1" : page_1,
        "Page-2": page_2,
        "Page-3": page_3,
        "Page-4": page_4,
        "Page-5": page_5,
        
    }
    gui = Gui(pages=pages)
    gui.run(dark_mode=False)

