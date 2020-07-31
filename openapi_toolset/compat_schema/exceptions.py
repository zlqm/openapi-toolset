from ..exceptions import ProjectError


class SchemaError(ProjectError):
    pass


class InvalidSchemaType(SchemaError):
    pass


class InvalidItemValue(SchemaError):
    pass
