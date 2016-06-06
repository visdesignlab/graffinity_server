def get_property_as_string(entity, name):
    if not entity.properties[name]:
        return "Null"
    else:
        return str(entity.properties[name].encode('ascii', 'ignore').decode('ascii'))


def get_property_as_float(entity, name):
    return float(entity.properties[name])


def get_property_as_int(entity, name):
    return int(entity.properties[name])
