from pymongo import MongoClient

client = MongoClient('mongodb+srv://nourelhoudaguelmami:VL78Y8bfzi9Uqp15@cluster0.7dfmo.mongodb.net/')
db = client['TechTestGenerator']

test_collection = db['Test']
jd_collection = db['job_description']

