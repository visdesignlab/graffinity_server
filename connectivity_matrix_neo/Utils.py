def get_property_as_string(entity, name):
    return str(entity.properties[name])


def get_property_as_float(entity, name):
    return float(entity.properties[name])


def get_property_as_int(entity, name):
    return int(entity.properties[name])
