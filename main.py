import cherrypy
import json
from  logic.parsers import SriptExpressions, Mapper, Request, ParsingError
from  logic.process import get_range, get_optimized_range, generate_matrix
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
        nulls =[]
        if request.nulls > 0:
            if request.null_method == 0:
                nulls = get_optimized_range(request.percent_nulls)
            else:
                nulls = get_range(request.nulls,request.len)

        preformated_fields = []
        for i in request.fields:
            script = SriptExpressions(i['sctript'])
            raw_func = mapper.get_function(i['type'], i['id'], script.params)
            preformated_fields.append(
                {
                    'id': i['id'],
                    'func': raw_func,
                    'null':i['null'],
                    'mutations':script.functions
                }
            )
        try:
            result = generate_matrix(nulls, preformated_fields, request.len)
            return json.dumps({'data': result})
        except Exception as e:
            print(e)
        return json.dumps({'data':[]})
if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        },
        'global': {
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8080,
            'server.thread_pool': 4,
            'server.shutdown_timeout': 1
        },
    }
    cherrypy.tree.mount(LargeSetService(), '/', conf)
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()

