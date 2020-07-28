import json
import os

import jsonschema

InvalidDoc = jsonschema.SchemaError


def load_schema(version):
    schema_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'openapi_{}_schema.json'.format(version))

    with open(schema_file) as f:
        return json.load(f)


v3_schema = load_schema('v3')


def validate(data, version='v3'):
    try:
        return jsonschema.validate(data, v3_schema)
    except (jsonschema.SchemaError,
            jsonschema.exceptions.ValidationError) as err:
        raise InvalidDoc(err)
