def to_float(extract):
    out = 0.0
    if len(extract) > 0:
        out = extract[0]
        out = out.replace("$","")
        out = out.replace(",", "")
        out = float(out)
    return out

def xcontains(el_type, class_name, func = "text()"):
    return "//{0}[contains(@class, '{1})']/{2}".format(el_type, class_name, func)

def add_attr(item, name, value):
    pass
