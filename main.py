import cherrypy
import json
from  logic.parsers import SriptExpressions, Mapper
from  logic.process import get_range, get_optimized_range
import time

class LargeSet:
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()

    def process(self):
        request = cherrypy.request.json
        data = json.loads(request)
        mapper = Mapper(request['language'])
        nulls = 0
        ds = []
        for i in data['fields']:
            if i['requaired'] == 'n':
                nulls+=1
            ds.append({
                'id':i['id'],
                'function':mapper.get_function(i['field_type']),
                'arguments':SriptExpressions(i['code']),
                'required':i['required']
            })
        if nulls > 0:
            null_range = get_range(nulls, qty_of_nulls)

