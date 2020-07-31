from . import exceptions


class Node:
    @classmethod
    def isinstance(cls, obj):
        def is_subclass_instance(subclass):
            return subclass.isinstance(obj)

        subclasses = cls.__subclasses__()
        return any(map(is_subclass_instance, subclasses))

    @classmethod
    def handle(cls, obj):
        return obj


class Unknown(Node):
    pass


class Combiner(Node):
    @classmethod
    def handle(cls, obj):
        obj = cls.handle_items(obj)
        obj = cls.handle_


class anyOf(Combiner):
    @classmethod
    def isinstance(cls, obj):
        return isinstance(obj, dict) and 'anyOf' in obj


class oneOf(Combiner):
    @classmethod
    def isinstance(cls, obj):
        return isinstance(obj, dict) and 'oneOf' in obj


class allOf(Combiner):
    @classmethod
    def isinstance(cls, obj):
        return isinstance(obj, dict) and 'allOf' in obj


class Schema(Node):
    @classmethod
    def isinstance(cls, obj):
        return isinstance(obj, dict) and 'type' in obj


class String(Schema):
    @classmethod
    def isinstance(cls, obj):
        return isinstance(obj, dict) and obj.get('type') == 'string'


class Number(Schema):
    @classmethod
    def isinstance(cls, obj):
        return isinstance(obj, dict) and obj.get('type') == 'number'


class Integer(Schema):
    @classmethod
    def isinstance(cls, obj):
        return isinstance(obj, dict) and obj.get('type') == 'integer'


class Object(Schema):
    @classmethod
    def isinstance(cls, obj):
        return isinstance(obj, dict) and obj.get('type') == 'object'


class Array(Schema):
    @classmethod
    def isinstance(cls, obj):
        return isinstance(obj, dict) and obj.get('type') == 'array'


class Boolean(Schema):
    @classmethod
    def isinstance(cls, obj):
        return isinstance(obj, dict) and obj.get('type') == 'boolean'


class Null(Schema):
    @classmethod
    def isinstance(cls, obj):
        return isinstance(obj, dict) and obj.get('type') == 'null'


def get_node_type(obj):
    def get_type_from_subclass(object, cls):
        _type = None
        subclasses = cls.__subclasses__()
        if subclasses:
            for subclass in subclasses:
                _type = get_type_from_subclass(obj, subclass)
                if _type:
                    return _type
        elif cls.isinstance(obj):
            return cls

    _type = get_type_from_subclass(obj, Node)
    if not _type:
        if Schema.isinstance(obj):
            msg = 'invalid schema type: {}'.format(obj['type'])
            raise exceptions.InvalidSchemaType(msg)
        else:
            _type = Unknown
    return _type
