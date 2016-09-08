
def xcontains(el_type, class_name, func = "text()"):
    return "//{0}[contains(@class, '{1}')]/{2}".format(el_type, class_name, func)

def xtract(response, xpath):
    return response.xpath(xpath).extract()
