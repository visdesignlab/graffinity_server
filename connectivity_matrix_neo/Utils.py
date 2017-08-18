def get_property_as_string(entity, name):
    if not entity.properties[name]:
        return "Null"
    else:
        return str(entity.properties[name].encode('ascii', 'ignore').decode('ascii'))


def get_propoery_as_list(entity, name):
    return list(entity.properties[name])


def get_property_as_float(entity, name):
    return float(entity.properties[name])


def get_property_as_int(entity, name):
    return int(entity.properties[name])


def pad_string_for_time(string):
    if len(string) == 3:
        return "0" + string
    elif len(string) == 2:
        return "00" + string
    elif len(string) == 1:
        return "000" + string
    else:
        return string


def pad_string_for_date(string):
    if len(string) == 1:
        return "0" + string
    return string
