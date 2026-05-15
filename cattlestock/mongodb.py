from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)

db = client['CattleStock']

article_collection = db['article']
bookmarks_collection = db['bookmarks']
likes_collection = db['likes']
comments_collection = db['comments']

alerts_collection = db['alerts']