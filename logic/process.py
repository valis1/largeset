import itertools
import numpy as np

"""

Takes quantity of null fields (num) and quantity of generated rows for the COMBINATION OPTIMIZED null method.
Returns the dict object where:
                            key - combination set (1 - null, 0 - not null);
                            value - integer value. Times of usage this combination;
>>> get_range(2,3)
{(1, 1): 1, (1, 0): 1, (0, 1): 1}

"""


def get_range(num, qty):
    # If one null field
    if num == 1:
        return {(1, ): int(qty/2)}
    combinations = list(itertools.product([1, 0], repeat=num))
    combinations.sort(key=lambda x: sum(x), reverse=True)

    if len(combinations) > qty:
        qty_per_combination = 1
        combinations = combinations[:qty]
    else:
        qty_per_combination = int(qty / len(combinations))
    res = {}
    for i in combinations:
        if res.get(i,False):
            res[i] += qty_per_combination
        else:
            res.update({i: qty_per_combination})
    return res



def generate_matrix(nulls, fields, qty):
    res = []
    warns = []
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
                    try:
                         val = i(val)
                    except TypeError as e:
                        warns.append({'function execution error': str(e)})
                row.update({field['id']:val})
        l_count+=1
        res.append(row)
    return res #To-Do Return warns













