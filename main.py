import cherrypy
import json
from  logic.parsers import SriptExpressions, Mapper, Request, ParsingError
from  logic.process import get_range, get_optimized_range
import time


@cherrypy.expose
class LargeSetService:
    @cherrypy.tools.accept(media='application/json')
    def POST(self):
        rawData = cherrypy.request.body.read(int(cherrypy.request.headers['Content-Length']))
        try:
            request = Request(rawData)
        except ParsingError as e:
            cherrypy.response.status = 400
            return json.dumps({'error_desc':str(e)})
        mapper = Mapper(request.language)
        if request.nulls > 0:
            if request.null_method == 0:
                nulls = get_optimized_range(request.percent_nulls)
            else:
                nulls = get_range(request.nulls,request.len)
        preformated_fields = []
        for i in request.fields:
            script = SriptExpressions(i['sctript'])
            if i['type'] == 'sequence':
                params = {'start': script.get('start',1),'step':script.get('step',1), 'name': i['id']}
            else:
                params={}

            raw_func = mapper.get_function(i['type'],params)
            func = {'main':raw_func[0],'mutations':[],'params':[]}
            for k,v in script.items():
                if k in raw_func:
                    func['params'].append(v[0])
                elif v[1]:
                    func['mutations'].append(v)

            preformated_fields.append(
                {
                    'id': i['id'],
                    'func': func,
                    'null':i['null']
                }
            )





if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        }
    }
    cherrypy.quickstart(LargeSetService(), '/', conf)
