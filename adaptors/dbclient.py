import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
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
        self.schema_collection = db.schemas

    @property
    def fields(self):
        try:
            return list(self.field_collection.find({}, {'_id':False}))
        except Exception:
            return [{'id': 'Error', 'desc': 'Connection Error', 'example': 'SERVER ERROR', 'script': '',
         'resolved_functions': ['']
         }]

    def get_schema(self, schema_id):
        try:
            obj_id = ObjectId(schema_id)
            schema = list(self.field_collection.find({"_id":obj_id},{'_id':False}))
            if len(schema) == 0:
                raise ClientError('Schema not found')
            else:
                return schema[0]
        except InvalidId:
            raise ClientError('Invalid schema ID')

    def updateSchema(self,schema, schema_id):
        try:
            obj_id = ObjectId(schema_id)
            result = self.field_collection.update_one({"_id":obj_id}, {"$set":schema})
            if result.matched_count == 0:
                return  "Schema not found"
            elif result.modified_count == 0:
                return "Nothing to update"
            else:
                return "Updated success"
        except InvalidId:
            raise  ClientError('Invalid Schema id')

    def insertSchema(self, schema):
        try:
            result = self.field_collection.insert_one(schema)
            return str(result.inserted_id)
        except Exception as e:
            raise ClientError(str(e))





class ClientError(Exception):
    pass



