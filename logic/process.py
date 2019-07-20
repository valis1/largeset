import itertools
import operator
import numpy as np

# Итертулс имеет ограничения по памяти. Думаю ограничить 20 необязательными полями на интерфейсе
def get_range(num, qty):
    combinations = list(itertools.product([1,0], repeat=num))
    combinations.sort(key=lambda x: sum(x), reverse=True)

    if len(combinations)>qty:
        qty_per_combination = 1
        addition = 0
        combinations = combinations[:qty]
    else:
       qty_per_combination = int(qty / num)
       addition = qty - qty_per_combination * num
    res = {}
    for i in combinations:
        if res.get(i,False):
            res[i]+=qty_per_combination+addition
        else:
            res.update({i:qty_per_combination+addition})
        if addition>0:
            addition = 0
    return res

def get_optimized_range(percents):
    combinations = list(itertools.product([1,0], repeat=len(percents)))
    combinations = list(filter(lambda x: sum(x)!=0,combinations))
    combinations.sort(key= lambda x: sum(x), reverse=True)
    res ={}
    percents = np.array(percents)
    combinations = np.array(combinations)
    while np.sum(percents)!=0:
        for i in combinations:
            r = percents - i
            if len(r[r<0])==0:
                percents = r
                k = tuple(i)
                if res.get(k,False):
                    res[k]+=1
                else:
                    res.update({k:1})
    return res

def generate_matrix(nulls, fields, qty):
    res = []
    if nulls:
        null_schema = max(nulls.items(), key=operator.itemgetter(1))[0]
        null_schema_iterator = iter(null_schema)
    i = 0
    while i<qty:
        row = {}
        for field in fields:
            # Processing nulls
            if field['null'] and null_schema_iterator:
                try:
                    is_null = next(null_schema_iterator)
                    nulls[null_schema]-=1
                except StopIteration:
                    null_schema = max(nulls.items(), key=operator.itemgetter(1))
                    if null_schema[1] == 0:
                        is_null = 0
                        null_schema_iterator = False
                    else:
                        null_schema = null_schema[0]
                        null_schema_iterator = iter(null_schema)
                if is_null == 1:
                    row.update({field['id']:None})
            else:
            # Processing not null
                fnc = field['func']
                val=fnc()
                for i in field['mutations']:
                    v = i(val)
                row.update({field['id']:val})
        i+=1
        res.append(row)
    return res













