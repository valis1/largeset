import cherrypy
import os
import json
from logic.parsers import SriptExpressions, Mapper, Request, ParsingError
from logic.process import get_range, get_optimized_range, generate_matrix
from  logic.ui_data import get_field_types


class LargeSetUI(object):
    @cherrypy.expose
    def index(self):
        return open('static/index.html', encoding='utf-8')

    @cherrypy.expose
    def fields(self):
        res = get_field_types()
        return json.dumps(res)

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
        result = generate_matrix(nulls, preformated_fields, request.len)
        return json.dumps({'data': result}, ensure_ascii=False)

conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/service': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        },
        'global': {
            'engine.autoreload.on': False
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }

    }
if os.getenv('PROD'):
    cherrypy.server.unsubscribe()
    cherrypy.engine.start()
    m = LargeSetUI()
    m.service = LargeSetService()
    app = cherrypy.tree.mount(m, '/', conf)
    app.service = LargeSetService()
else:
    app = LargeSetUI()
    app.service = LargeSetService()
    cherrypy.quickstart(app, '/', conf)

