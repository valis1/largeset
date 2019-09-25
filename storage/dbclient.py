import os
from pymongo import MongoClient

MONGO_URI= os.environ.get("MONGODB_URI")

def get_field_types():
    if not MONGO_URI:
        # To-Do Normal error processing
        return [{'id': 'Error', 'desc': 'NO MONGO URI', 'example': 'SERVER ERROR', 'script': '',
         'resolved_functions': ['']
         }]
    connect = MongoClient(MONGO_URI)
    db = connect.heroku_lfsxmz64
    fields = db.fields
    try:
        res = fields.find({}, {'_id':False})
        connect.close()
        return list(res)
    except Exception:
        connect.close()
        return [{'id': 'Error', 'desc': 'NO MONGO URI', 'example': 'SERVER ERROR', 'script': '',
         'resolved_functions': ['']
         }]





