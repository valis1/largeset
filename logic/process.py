import itertools
import operator
import numpy as np

# Итертулс имеет ограничения по памяти. Думаю ограничить 20 необязательными полями на интерфейсе
def get_range(num, qty):
    # Обрабатываем одно нуловое поле
    if num == 1:
        return { (1, ): abs(qty/2)}
    combinations = list(itertools.product([1,0], repeat=num))
    combinations.sort(key=lambda x: sum(x), reverse=True)

    if len(combinations)>qty:
        qty_per_combination = 1
        addition = 0
        combinations = combinations[:qty]
    else:
       qty_per_combination = int(qty / len(combinations))
       addition = qty - qty_per_combination * num
    res = {}
    for i in combinations:
        if res.get(i,False):
            res[i] += qty_per_combination
        else:
            res.update({i:qty_per_combination})
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
    print(nulls)
    res = []
    null_schema_iterator = None
    if nulls:
        nulls_iterator = iter(nulls.keys())
        current_null = next(nulls_iterator)
        null_schema_iterator = iter(current_null)
    l_count = 0
    while l_count<qty:
        row = {}
        for field in fields:
            # Processing nulls
            if null_schema_iterator and field['null']:
                try:
                    is_null = next(null_schema_iterator)
                except StopIteration:
                    nulls[current_null] -= 1
                    if nulls[current_null] == 0:
                        try:
                            current_null = next(nulls_iterator)
                            null_schema_iterator = iter(current_null)
                        except StopIteration:
                            is_null = 0
                            null_schema_iterator = None
                    else:
                        null_schema_iterator = iter(current_null)
                        is_null = next(null_schema_iterator)
                if is_null == 1:
                    row.update({field['id']: None})
                else:
                    fnc = field['func']
                    val = fnc()
                    # ToDo Do not mutate if result is not numeric or date
                    for i in field['mutations']:
                        val = i(val)
                    row.update({field['id']: val})
            else:
            # Processing not null
                fnc = field['func']
                val=fnc()
            #ToDo Do not mutate if result is not numeric or date
                for i in field['mutations']:
                    val = i(val)
                row.update({field['id']:val})
        l_count+=1
        res.append(row)
    return res













