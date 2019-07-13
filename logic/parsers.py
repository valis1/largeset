from mimesis import Generic
import json
import uuid
import re

class SriptExpressions:

    def __init__(self, codestring):
        self.functions = {
            'multipy': lambda x, y: x * y,
            'left_devision': lambda x, y: x / y,
            'right_devision': lambda x, y: y / x,
            'add': lambda x, y: x + y,
            'left_subtract': lambda x, y: x - y,
            'right_subtract': lambda x, y: y - x
        }
        self.code = codestring.split(';')
        self.res = {}
        self.regexps= {
            'min': r'min\s*=\s*[0-9]*',
            'mgax': r'max\s*=\s*[0-9]*',
            'format': r'format\s*=\s*.*',
            'qty': r'qty\s*=\s*[0-9]*',
            'type':r'type\s*=\s*ean-13|ean-8',
            'multiply' : r'lambda x\s*:\s*x|[0-9]+\s*\*\s*[0-9]+|x',
            'left_devision' : r'lambda x\s*:\s*x\s*\\\s*[0-9]+',
            'right_devision': r'lambda x\s*:\s*[0-9]+\s*\\\s*x',
            'add' : r'lambda x\s*:\s*x|[0-9]+\s*\+\s*[0-9]+|x',
            'left_subtract' : r'lambda x\s*:\s*x\s*-\s*[0-9]+',
            'right_subtract': r'lambda x\s*:\s*[0-9]+\s*-\s*x',
        }
        self.__parseCode()

    def __parseCode(self):
        for i in self.code:
            for k, v in self.regexps.items():
                if re.match(v, i):
                    if k != 'format' or k!='type':
                        x = re.search(r'[0-9]+\.[0-9]+')
                        if x:
                            self.res.update({k: (float(x.group(0)), self.functions.get(k, False))})
                        else:
                            x = re.search(r'[0-9]+')
                            if x:
                                self.res.update({k: (int(x.group(0)),self.functions.get(k, False))})
                    elif k=='format':
                        x = re.search(r'(%{1}[a-zA-Z]{1}[\s\.:-]*)+')
                        if x:
                            self.res.update({k:(x.group(0),)})
                    else:
                        x = re.search(r'ean-13|ean-8')
                        self.res.update({k:(x.group(0),)})

    @property
    def results(self):
        return self.res



class Mapper:
    def __init__(self, locate):
        self.g = Generic(locate)
        # Default global counter for sequence function
        self.sequences={'global':{'current':0, 'step':1}}
        self.map ={
            'address': (self.g.address.address,),
            'city': (self.g.address.city,),
            'latitude': (self.g.address.latitude,),
            'longitude': (self.g.address.longitude,),
            'postal_code': (self.g.address.postal_code,),
            'company': (self.g.business.company,),
            'price': (self.g.business.price,'min','max'),
            'datetime': (self.g.datetime.datetime, 'format'),
            'date': (self.g.datetime.date, 'format'),
            'day_of_week': (self.g.datetime.day_of_week,),
            'timestamp': (self.g.datetime.timestamp,),
            'dish': (self.g.food.dish, ),
            'drink': (self.g.food.drink,),
            'fruit': (self.g.food.fruit,),
            'vegetable': (self.g.food.vegetable,),
            'email': (self.g.person.email,),
            'full_name': (self.g.person.full_name,),
            'job': (self.g.person.occupation,),
            'phone': (self.g.person.telephone,),
            'username': (self.g.person.username,),
            'text': (self.g.text.text,),
            'title': (self.g.text.title, ),
            'ean_code': (self.g.code.ean,'type'),
            'uuid': (uuid.uuid4,),
            'file_name': (self.g.file.file_name,),
            'url_home': (self.g.internet.home_page,),
            'mac': (self.g.internet.mac_address,),
            'ip': (self.g.internet.ip_v4,),
            'digit_range': (self.g.numbers.between,'min', 'max'),
            'float': (self.__get_float, 'min', 'max'),
            'int': (self.__get_int, 'min', 'max'),
            'car_model': (self.g.transport.car, ),
            'sequence':(self.__get_sequence_item,'field_name')
        }
    def get_function(self,name,params={}):
        if name == 'sequence':
            self.__set_sequence(name,params)
        func = self.map.get(name)
        return func

    def __set_sequence(self,name='global',params={}):
        self.sequences.update({name:{'current':params.get('start',0),'step':params.get('step',1)}})

    def __get_sequence_item(self,field_name):
        c = self.sequences.get(field_name,'counter')
        x = c['current']
        step = c['step']
        self.sequences.update({field_name:{'current':x+step,'step':step}})
        return x

class ParsingError(Exception):
    pass

# JSON Format {"language":"en|ru", "null_method":"percent_optimized|combination_optimized", "fields":[]}
# Fields {'id':'my_field', 'type':'int', 'null':True, 'percent_nulls':'30','sctript':'a=1'}

class Request:
    def __init__(self, request):
        try:
            self.data = json.loads(request)
        except json.decoder.JSONDecodeError:
            raise ParsingError('Unsupported json format')

        try:
            self.language = self.data['language']

