from mimesis import Generic
from mimesis import enums
import json
import uuid
import re
import random
import ast

class SriptExpressions:

    def __init__(self, codestring):
        self.warns = []
        self.function_patterns = {
            'lambda': r'^\s*lambda',
            'upper': r'\s*upper\(\s*x\s*\)',
            'lower': r'\s*lower\(\s*x\s*\)',
            'preffix': r'^\+',
            'suffix': r'.+\+'
        }
        self.code = codestring.split(';')
        self.formated_params ={}
        self.formated_functions = []
        self.num_params= {
            'min': r'\s*min\s*=\s*[0-9]*',
            'max': r'\s*max\s*=\s*[0-9]*',
            'qty': r'\s*qty\s*=\s*[0-9]*',
            'step':  r'\s*step\s*=\s*[0-9]*',
            'start':  r'\s*start\s*=\s*[0-9]*',
            'end': r'\s*end\s*=\s*[0-9]*',
            'round': r'\s*round\s*=\s*[0-9]*',

        }
        self.string_params = {
            'format': r'\s*format\s*=\s*.*',
            'type': r'\s*type\s*=\s*(ean-13|ean-8|isbn-10|isbn-13)\s*',
            'const': r'\s*const\s*=.*',
            'items': r'\s*items\s*=\s*\[.*]\s*'
        }

        self.__parseCode()

    def __get_num_params(self, code_string):
        for k, v in self.num_params.items():
            if re.match(v, code_string):
                x = re.search(r'[0-9]+\.[0-9]+', code_string)
                if x:
                    self.formated_params.update({k:float(x.group(0))})
                    return True
                else:
                    x = re.search(r'[0-9]+', code_string)
                    if x:
                        self.formated_params.update({k: int(x.group(0))})
                        return True

        return False

    def __get_functions(self, code_string):
        for k,v in self.function_patterns.items():
            if re.match(v, code_string):
                if k == 'upper':
                    self.formated_functions.append(lambda x: x.upper())
                    return True
                elif k == 'lower':
                    self.formated_functions.append(lambda x: x.lower())
                    return True
                elif k == 'preffix':
                    value = code_string.replace(' ', '')[1:]
                    self.formated_functions.append(lambda x: x +value)
                elif k == 'suffix':
                    value = code_string.replace(' ', '')[:-1]
                    self.formated_functions.append(lambda x: value + x )
                    return True
                elif k == 'lambda':
                    try:
                        if self.__lambdavalidator(code_string):
                            func = eval(code_string)
                            self.formated_functions.append(func)
                        else:
                            self.warns.append({'not allowed function': code_string})
                    except SyntaxError:
                        self.warns.append({'invalid_syntax':code_string})
        return False

    def __get_string_params(self, code_string):
        for k, v in self.string_params.items():
            if re.match(v, code_string):
                x = code_string.split('=')[1].strip()
                self.formated_params.update({k:x})
                return True
        return False

    @staticmethod
    def __lambdavalidator(x):
        if x.find('while')!= -1:
            return False
        elif x.find('for')!= -1:
            return False
        elif x.find('if')!=-1:
            return False
        elif len(x) > 60:
            return False
        else:
            return True


    def __parseCode(self):
        for i in self.code:
            if self.__get_num_params(i):
                continue
            elif self.__get_string_params(i):
                continue
            elif self.__get_functions(i):
                continue
            else:
                self.warns.append({'function not found': i})

    @property
    def params(self):
        return self.formated_params

    @property
    def functions(self):
        return self.formated_functions

class Mapper:
    def __init__(self, locate):
        self.g = Generic(locate)
        # Default global counter for sequence function
        self.sequences={'global':{'current':0, 'step':1}}
        self.map ={
            'address': self.g.address.address,
            'city': self.g.address.city,
            'latitude': self.g.address.latitude,
            'longitude': self.g.address.longitude,
            'postal_code': self.g.address.postal_code,
            'company': self.g.business.company,
            'day_of_week': self.g.datetime.day_of_week,
            'timestamp': self.g.datetime.timestamp,
            'dish': self.g.food.dish,
            'drink': self.g.food.drink,
            'fruit': self.g.food.fruit,
            'vegetable': self.g.food.vegetable,
            'email': self.g.person.email,
            'full_name': self.g.person.full_name,
            'job': self.g.person.occupation,
            'phone': self.g.person.telephone,
            'username': self.g.person.username,
            'text': self.g.text.text,
            'title': self.g.text.title,
            'uuid': lambda : str(uuid.uuid4()),
            'file_name': self.g.file.file_name,
            'url_home': self.g.internet.home_page,
            'mac': self.g.internet.mac_address,
            'ip': self.g.internet.ip_v4,
            'car_model': self.g.transport.car,
            'imei': self.g.code.imei,
            'boolean':self.g.development.boolean,
            'operation_system': self.g.development.os,
            # Hardware
            'phone_model': self.g.hardware.phone_model,
            'cpu': self.g.hardware.cpu,
            'cpu_codename':self.g.hardware.cpu_codename,
            'cpu_frequency': self.g.hardware.cpu_frequency,
            'cpu_generation':self.g.hardware.generation,
            'graphics': self.g.hardware.graphics,
            'manufacturer': self.g.hardware.manufacturer,
            'ram_size':self.g.hardware.ram_size,
            'ram_type': self.g.hardware.ram_type,
            'resolution':self.g.hardware.resolution,
            'screen_size':self.g.hardware.screen_size,
        }

    def get_function(self, name, field_id, params={}):
        if name == 'sequence':
            self.__set_sequence(field_id,params=params)
        func = self.map.get(name, False)
        if func:
            return func
        elif name == 'price':
            kw = {'minimum':params.get('min', 1), 'maximum':params.get('max',100)}
            return lambda : self.g.business.price(**kw)
        elif name == 'datetime':
            kw = {'start':params.get('min',1999),'end':params.get('max',2040)}
            return lambda : self.g.datetime.datetime(**kw).strftime(params.get('format', '%c'))
        elif name == 'date':
            kw = {'start':params.get('min',1999),'end':params.get('max',2040)}
            return lambda : self.g.datetime.date(**kw).strftime(params.get('format', '%c'))
        elif name == 'ean_code':
            if params.get('type', 'ean-13')=='ean-13':
                return lambda : self.g.code.ean(enums.EANFormat.EAN13)
            else:
                return lambda : self.g.code.ean(enums.EANFormat.EAN8)
        elif name == 'isbn':
            if params.get('type', 'isbn-10') == 'isbn-10':
                return lambda : self.g.code.isbn(enums.ISBNFormat.ISBN10)
            else:
                return lambda : self.g.code.isbn(enums.ISBNFormat.ISBN13)

        elif name == 'int':
            kw = {'minimum':params.get('min', 1), 'maximum':params.get('max',100)}
            return lambda : self.g.numbers.between(**kw)
        elif name == 'float':
            kw = {'minimum': params.get('min', 1), 'maximum': params.get('max',100), 'round_param': params.get('round',2)}
            return lambda : self.__gen_float(**kw)
        elif name == 'sequence':
            return lambda : self.__get_sequence_item(field_id)
        elif name == 'const':
            return lambda : params.get('const', 0)
        elif name == 'choice':
            return lambda : random.choice(ast.literal_eval(params.get('items', '[1,2,3]')))


    def __gen_float(self, minimum=1, maximum=100, round_param=2):
        return round(random.uniform(minimum, maximum), round_param)

    def __set_sequence(self,field_id,params={},):
        self.sequences.update({field_id:{'current':params.get('start',0),'step':params.get('step',1)}})

    def __get_sequence_item(self,field_name):
        c = self.sequences.get(field_name, False)
        if c:
            x = c['current']
            step = c['step']
            self.sequences.update({field_name:{'current':x+step,'step':step}})
            return x
        return 0

class ParsingError(Exception):
    pass

# JSON Format {"language":"en|ru", "null_method":"percent_optimized|combination_optimized", "data_len":10,"fields":[]}
# Fields {'id':'my_field', 'type':'int', 'null':True, 'percent_nulls':'30','sctript':'a=1'}

class Request:
    def __init__(self, request):
        null_methods = {
            'percent_optimized': 0,
            'combination_optimized': 1
        }
        try:
            self.data = json.loads(request)
        except json.decoder.JSONDecodeError:
            raise ParsingError('Unsupported json format')

        try:
            self.null_method = null_methods[self.data['null_method']]
        except KeyError:
            raise ParsingError('null method must be in (percent_optimized, combination_optimized) ')

        self.nulls = 0
        self.percent_nulls = []

        try:
            self.language = self.data['language']
            self.len = int(self.data['data_len'])
            self.fields = []
            for i in self.data['fields']:
                if i.get('id') and i.get('type'):
                    if int(i.get('percent_nulls', 0)) >0 and self.null_method==0:
                        self.nulls += 1
                        self.percent_nulls.append((self.len/100)*int(i['percent_nulls']))
                        i['null'] = True
                    elif self.null_method == 1 and i.get('null'):
                        self.nulls += 1
                    else:
                        i['null'] = False
                    self.fields.append(i)
                else:
                    raise ParsingError('Field id and field type are required')
        except KeyError:
            raise ParsingError('Language, null method, data_len fields range are required')
        except ValueError:
            raise ParsingError('percent_nulls, data_len must be integers')



