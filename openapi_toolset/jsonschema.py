def strict_schema(schema):
    '''
    Feature
      1. add required fields
      2. compat nullable in OAI and jsonschema
    '''
    if isinstance(schema, dict):
        return strict_object(schema)
    elif isinstance(schema, list):
        return [strict_schema(item) for item in schema]
    else:
        return schema


def strict_object(schema):
    if schema.get('nullable') is True:
        schema.pop('nullable')
        schema = strict_schema(schema)
        null_type_obj = {'type': 'null'}
        if any(filter(lambda key: key in schema, ['type', 'allOf', 'anyOf'])):
            schema = {'oneOf': [null_type_obj, schema]}
        elif schema.get('oneOf'):
            if null_type_obj not in schema['oneOf']:
                schema['oneOf'].append(null_type_obj)
    if schema.get('type') == 'object':
        schema['additionalProperties'] = \
                schema.get('additionalProperties', False)
        default_required = list(schema.get('properties', {}).keys())
        schema['required'] = schema.get('required', default_required)
        schema['properties'] = {
            key: strict_schema(value)
            for key, value in schema.get('properties', {}).items()
        }
    else:
        for key, value in schema.items():
            schema[key] = strict_schema(value)
    return schema
