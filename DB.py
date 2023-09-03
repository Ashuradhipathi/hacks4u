from pymongo import MongoClient

mongostr = ""
client = MongoClient(mongostr, serverSelectionTimeoutMS=60000)
db = client['HacksForU']

def show_roadmaps():
    Roadmaps = db["Roadmaps"]
    roadmaps = iter(Roadmaps.find())
    return roadmaps

def show_courses():
    Courses = db["Courses"]
    courses = iter(Courses.find())
    return courses

def show_FreeStuff():
    FreeStuff = db["FreeStuff"]
    items = iter(FreeStuff.find())
    return items







