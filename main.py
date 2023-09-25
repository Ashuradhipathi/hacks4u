from taipy.gui import Gui, navigate
import DB

from pymongo import MongoClient

mongostr = "mongodb+srv://Fellowship:1A7oialpAswV5I2B@cluster0.ub5pbd6.mongodb.net/?retryWrites=true&w=majorityS"
client = MongoClient(mongostr, serverSelectionTimeoutMS=60000)
db = client['HacksForU']
from certificate import *


def list_to_string(input_list):
    result = ""
    result = "\n".join( input_list)
    return result




index = """"<|menu|label=Menu|lov={[('Page-1', 'Home'), ('Page-2', 'Courses'), ('Page-3','Resources'),('Page-4','Roadmaps'),('Page-5','Certificates'),('https://github.com/mopasha1/hacks4u','Github_Repo'),('https://docs.taipy.io/en/latest/','Taipy_Documentation')]}|on_action=on_menu|>"""
page_1 =  """
#Hacks For U


<|layout|columns= 2 2 2 1 1|

<|

#Resources
"Student offers" typically refer to discounts, promotions, or special deals specifically designed for students. These offers are a way for businesses, educational institutions, and various service providers to support students and make their products or services more accessible
|>

<|
#Courses<br />
Free course websites are invaluable resources for learners of all ages and backgrounds. These platforms offer a wide range of educational content at no cost, making quality learning accessible to anyone with an internet connection
|>

<|
#Roadmaps<br />
Roadmaps are strategic plans or visual representations that outline the key steps, milestones, and goals necessary to achieve a specific objective, project, or journey. Roadmaps are used in various contexts, including business, project management, product development, and personal development
|>

<|
#Github<br />
Contributions are actions or efforts made by individuals or groups to enhance, improve, or make a positive impact on various aspects of society, organizations, or projects. Contributions can take many forms and play a crucial role in personal development, community building, and the progress of society.
|>

<|
#Taipy Documentation<br />
Taipy is used to build it, so we thought it will be useful. 
|>


|>
"""

course_title = []
course_desc = []
course_link = []
courses_ = DB.show_courses()
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
<|Add Sources for Courses |expandable|expanded=False|
<|{courseTitle}|input|label=Enter Title|><br />
<|{courseDesc}|input|label= Enter Description|><br />
<|{courseimage}|input|label=Enter image url|><br />
<|{courseLink}|input|label=Enter webiste url|><br />
<|Submit|button|on_action=create_courses|><br />
|>
"""

def create_roadmap(state):
    Title = state.roadmapTitle
    Description = state.roadmapDesc
    Image = state.roadmapimage
    Link = state.roadmapLink
    Roadmaps = DB["Roadmaps"]
    new_roadmap = {
        "Title": Title,
        "Description": Description,
        "Image" : Image,
        "Link": Link        
        }
    Roadmaps.insert_one(new_roadmap)

def create_FreeStuff(state):
    Title = state.resourceTitle
    Description = state.resourceDesc
    Image = state.resourceimage
    Link = state.resourceLink
    FreeStuff = DB["FreeStuff"]
    new_stuff = {
        "Title": Title,
        "Description": Description,
        "image" : Image,
        "Link": Link        
    }
    FreeStuff.insert_one(new_stuff)

def create_courses(state):
    Title = state.courseTitle
    Description = state.courseDesc
    Image = state.courseimage
    Link = state.courseLink
    Courses = DB["Courses"]
    new_course = {
        "Title": Title,
        "Description": Description,
        "image" : Image,
        "Link": Link        
    }
    Courses.insert_one(new_course)

resource_title = []
resource_desc = []
resource_link = []
resources_ = DB.show_FreeStuff()
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
<|Add Resources |expandable|expanded=False|
<|{resourceTitle}|input|label=Enter Title|><br />
<|{resourceDesc}|input|label= Enter Description|><br />
<|{resourceimage}|input|label=Enter image url|><br />
<|{resourceLink}|input|label=Enter webiste url|><br />
<|Submit|button|on_action=create_FreeStuff|><br />
|>
"""


Roadmaps_title = []
Roadmaps_desc = []
Roadmaps_link = []
Roadmaps_ = DB.show_roadmaps()
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
<|Add Sources for Resources |expandable|expanded=False|
<|{roadmapTitle}|input|label=Enter Title|><br />
<|{roadmapDesc}|input|label= Enter Description|><br />
<|{roadmapimage}|input|label=Enter image url|><br />
<|{roadmapLink}|input|label=Enter webiste url|><br />
<|Submit|button|on_action=create_roadmap|><br />
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

