import os
from pymongo import MongoClient

"""
Adaptor for mongoDB adaptors.
MONGODB_URI must be in environ variables
Where:
- Fields property - returns list of dicts with possible data types for generator

>>>client = DbClient()
>>>len(client.fields) > 0
True

"""
class DbClient():
    def __init__(self):
        self.mongo_ulr = os.environ.get("MONGODB_URI")
        connect = MongoClient(self.mongo_ulr)
        db = connect.heroku_lfsxmz64
        self.field_collection = db.fields

    @property
    def fields(self):
        try:
            return list(self.field_collection.find({}, {'_id':False}))
        except Exception:
            return [{'id': 'Error', 'desc': 'Connection Error', 'example': 'SERVER ERROR', 'script': '',
         'resolved_functions': ['']
         }]





