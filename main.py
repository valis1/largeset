import cherrypy
import os
import json
from logic.parsers import SriptExpressions, Mapper, Request, ParsingError
from logic.process import get_range, generate_matrix
from adaptors.dbclient import DbClient, ClientError

CLIENT = DbClient()

class LargeSetUI:
    @cherrypy.expose
    def index(self):
        return open('static/index.html', encoding='utf-8')

    @cherrypy.expose
    def fields(self):
        res = CLIENT.fields
        return json.dumps(res)

@cherrypy.expose
class Schemas:
    def GET(self, schema_id):
        try:
            res = CLIENT.get_schema(schema_id)
            return json.dumps(res)
        except ClientError as e:
            cherrypy.response.status = 400
            return json.dumps({'error':str(e)})

    def POST(self):
        data  = cherrypy.request.body.read(int(cherrypy.request.headers['Content-Length']))
        try:
            res = CLIENT.insertSchema(json.loads(data))
            return json.dumps({'schema_id':res})
        except json.decoder.JSONDecodeError as e:
            cherrypy.response.status = 400
            return json.dumps({'error': 'bad schema json'})
        except ClientError as e:
            cherrypy.response.status = 400
            return json.dumps({'error': str(e)})

    def PUT(self,schema_id):
        data = cherrypy.request.body.read(int(cherrypy.request.headers['Content-Length']))
        try:
            msg = CLIENT.updateSchema(json.loads(data),schema_id)
            return json.dumps({"message": msg})
        except json.decoder.JSONDecodeError as e:
            cherrypy.response.status = 400
            return json.dumps({'error': 'bad schema json'})
        except ClientError as e:
            cherrypy.response.status = 400
            return json.dumps({'error': str(e)})



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
         '/schemas': {
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
    m.schemas = Schemas()
    app = cherrypy.tree.mount(m, '/', conf)
    app.service = LargeSetService()
else:
    app = LargeSetUI()
    app.service = LargeSetService()
    app.schemas = Schemas()
    cherrypy.quickstart(app, '/', conf)

