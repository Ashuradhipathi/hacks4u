from pymongo import MongoClient

mongostr = "mongodb+srv://Fellowship:1A7oialpAswV5I2B@cluster0.ub5pbd6.mongodb.net/?retryWrites=true&w=majorityS"
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







