
import re
import json

def add_field(item, name, result, transform = lambda x: x):
    if isinstance(result, list) and len(result) > 0:
        item[name] = transform(result[0])
    elif len(result) > 0:
        item[name] = transform(result)
    else:
        item[name] = None

def to_float(extract):
    out = extract
    out = out.replace("$","")
    out = out.replace(",", "")
    out = float(out)
    return out


def transform_initial_data(data_string):
    cleaned_string = re.sub('.*initialData.*?{', '{', data_string)

    cleaned_string = re.sub('}\).*$', '}', cleaned_string)
    print(cleaned_string)
    return json.loads(cleaned_string)
