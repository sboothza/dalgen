from enum import Enum
from typing import Any, Union, List

from naming import Name
from serializer import serializer_instance, Serializer


class DataException(Exception):
    pass


class DatatypeException(DataException):
    pass


class FieldType:
    pass


class FieldType(Enum):
    Undefined = 0
    Integer = 1
    String = 2
    Float = 3
    Decimal = 4
    Datetime = 5
    Boolean = 6
    Item = 7
    ListOfItem = 8

    @classmethod
    def get_fieldtype(cls, value: str) -> FieldType:
        value = value.lower()
        if value == "integer" or value == "int" or value == "bigint" or value == "tinyint":
            return FieldType.Integer
        elif value == "string" or value == "varchar" or value == "char" or value == "text":
            return FieldType.String
        elif value == "float" or value == "real":
            return FieldType.Float
        elif value == "datetime" or value == "date":
            return FieldType.Datetime
        elif value == "boolean" or value == "bool":
            return FieldType.Boolean
        elif value == "decimal" or value == "money":
            return FieldType.Decimal
        elif value == "__item__":
            return FieldType.Item
        elif value == "[__item__]":
            return FieldType.ListOfItem
        elif value == "none":
            return FieldType.Undefined
        else:
            raise DatatypeException(f"Unknown field type {value}")

    def __str__(self):
        if self == FieldType.Integer:
            return "Integer"
        elif self == FieldType.String:
            return "String"
        elif self == FieldType.Float:
            return "Float"
        elif self == FieldType.Datetime:
            return "Datetime"
        elif self == FieldType.Boolean:
            return "Boolean"
        elif self == FieldType.Decimal:
            return "Decimal"
        elif self == FieldType.Item:
            return "__Item__"
        elif self == FieldType.ListOfItem:
            return "[__Item__]"
        elif self == FieldType.Undefined:
            return "None"
        else:
            raise DatatypeException("Unknown field type ")

    def map_to_dict(self, serializer: Serializer) -> str:
        return str(self)


class Field(object):
    pass


class Field(object):
    name: Name
    type: FieldType
    size: int
    scale: int
    auto_increment: bool
    default: Any
    required: bool

    def __init__(self, name: Name = None, field_type: FieldType = FieldType.Undefined, size: int = 0, scale: int = 0,
                 auto_increment: bool = False, default=None, required: bool = False):
        self.name = name
        self.type = field_type
        self.size = size
        self.scale = scale
        self.auto_increment = auto_increment
        self.default = default
        self.required = required

    def __str__(self):
        return f"{str(self.name)} {self.type} ({self.size},{self.scale}) {'AUTOINC ' if self.auto_increment else ''}" \
               f"{'DEFAULT ' + self.default + ' ' if self.default else ''}{'NOT NULL' if self.required else 'NULL'}"

    def map_to_object(self, obj, serializer, naming):
        self.name = naming.string_to_name(obj["name"])
        self.type = FieldType.get_fieldtype(obj["type"])
        self.size = obj["size"]
        self.scale = obj["scale"]
        self.auto_increment = obj["auto_increment"]
        self.default = obj["default"]
        self.required = obj["required"]


serializer_instance.register_class(Field)


class KeyType:
    pass


class KeyType(Enum):
    Undefined = 0
    PrimaryKey = 1
    Index = 2
    Unique = 3
    ForeignKey = 4
    Lookup = 5

    @classmethod
    def get_keytype(cls, value: str) -> KeyType:
        value = value.lower()
        if value == "undefined":
            return KeyType.Undefined
        elif value == "primarykey" or value == "primary key":
            return KeyType.PrimaryKey
        elif value == "index":
            return KeyType.Index
        elif value == "unique":
            return KeyType.Unique
        elif value == "foreignkey" or value == "foreign key":
            return KeyType.ForeignKey
        elif value == "lookup":
            return KeyType.Lookup
        else:
            raise DatatypeException(f"Unknown key type {value}")

    def __str__(self):
        if self == KeyType.Undefined:
            return "Undefined"
        elif self == KeyType.PrimaryKey:
            return "PrimaryKey"
        elif self == KeyType.Index:
            return "Index"
        elif self == KeyType.Unique:
            return "Unique"
        elif self == KeyType.ForeignKey:
            return "ForeignKey"
        elif self == KeyType.Lookup:
            return "Lookup"
        else:
            raise DatatypeException("Unknown key type ")


class Table(object):
    pass


class Key(object):
    pass


class Key(object):
    name: Name
    fields: List[str]
    primary_table: str
    primary_fields: List[str]
    referenced_table: str
    key_type: KeyType

    def __init__(self, name: Name = None, key_type: KeyType = KeyType.Undefined, primary_table: str = ""):
        self.name = name
        self.fields: List[str] = list()
        self.primary_table = primary_table
        self.primary_fields: List[str] = list()
        self.key_type = key_type
        self.referenced_table = ""

    def __str__(self):
        return f"{self.name} {self.key_type} {','.join(self.fields)}{self.primary_table}" \
               f"{'' if len(self.primary_fields) == 0 else ','.join(self.primary_fields)}"

    def map_to_object(self, obj, serializer, naming):
        self.name = naming.string_to_name(obj["name"])
        self.fields = serializer.map_to_object(obj["fields"], extra=naming)
        self.primary_table = "" if "primary_table" not in obj else str(obj["primary_table"])
        self.primary_fields = "" if "primary_fields" not in obj else serializer.map_to_object(
            obj["primary_fields"], extra=naming)
        self.key_type = KeyType.get_keytype(obj["key_type"])
        self.referenced_table = "" if "referenced_table" not in obj else str(obj["referenced_table"])

    def map_to_dict(self, serializer: Serializer):
        obj = {
            "name": self.name.raw(),
            "fields": serializer.map_to_dict(self.fields),
            "key_type": str(self.key_type)
        }
        if self.key_type == KeyType.ForeignKey or self.key_type == KeyType.Lookup:
            obj["primary_table"] = str(self.primary_table)
            obj["primary_fields"] = serializer.map_to_dict(self.primary_fields)

        obj["referenced_table"] = str(self.referenced_table)

        return obj


serializer_instance.register_class(Key)
serializer_instance.register_class(Key, "fields:key_type:name:referenced_table")


class TransformType:
    pass


class TransformType(Enum):
    Undefined = 0
    Map = 1
    IntToBool = 2

    @classmethod
    def get_transformtype(cls, value: str) -> TransformType:
        value = value.lower()
        if value == "undefined" or value == "none":
            return TransformType.Undefined
        elif value == "map":
            return TransformType.Map
        elif value == "inttobool":
            return TransformType.IntToBool
        else:
            raise DatatypeException(f"Unknown transform type {value}")


class QueryType:
    pass


class QueryType(Enum):
    Undefined = 0
    FetchScalar = 1
    FetchOne = 2
    FetchAll = 3
    Execute = 4

    @classmethod
    def get_querytype(cls, value: str) -> QueryType:
        value = value.lower()
        if value == "undefined":
            return QueryType.Undefined
        elif value == "fetchscalar":
            return QueryType.FetchScalar
        elif value == "fetchone":
            return QueryType.FetchOne
        elif value == "fetchall":
            return QueryType.FetchAll
        elif value == "execute":
            return QueryType.Execute
        else:
            raise DatatypeException("Unknown query type {}".format(value))


class Parameter(object):
    name: Name
    type: FieldType

    def __init__(self, name: Name = None, type: FieldType = FieldType.Undefined):
        self.name = name
        self.type = type

    def map_to_object(self, obj, serializer, naming):
        self.name = naming.string_to_name(obj["name"])
        self.type = FieldType.get_fieldtype(obj["type"])


serializer_instance.register_class(Parameter)


class CustomQuery(object):
    name: Name
    parameters: List[Parameter]
    return_type: FieldType
    transform: TransformType
    query_type: QueryType
    query: str

    def __init__(self, name: Name = None):
        self.name = name
        self.parameters: List[Parameter] = list()
        self.return_type = FieldType.Undefined
        self.transform = TransformType.Undefined
        self.query_type = QueryType.Undefined
        self.query = ""

    def __str__(self):
        return str(self.name)

    def map_to_object(self, obj, serializer, naming):
        self.name = naming.string_to_name(obj["name"])
        self.parameters = serializer.map_to_object(obj["parameters"], extra=naming)
        self.return_type = FieldType.get_fieldtype(obj["return_type"])
        self.transform = TransformType.get_transformtype(obj["transform"])
        self.query_type = QueryType.get_querytype(obj["query_type"])
        self.query = str(obj["query"])


serializer_instance.register_class(CustomQuery)


class Table(object):
    name: Name
    fields: List[Field]
    pk: Union[Key, None]
    keys: List[Key]
    foreign_keys: List[Key]
    custom_queries: List[CustomQuery]

    def __init__(self, name: Name = None):
        self.name = name
        self.fields: List[Field] = list()
        self.pk: Union[Key, None] = None
        self.keys: List[Key] = list()
        self.foreign_keys: List[Key] = list()
        self.custom_queries: List[CustomQuery] = list()

    def find_field(self, name: str) -> Field:
        found_fields = [f for f in self.fields if f.name.raw().lower() == name.lower()]
        if len(found_fields) > 0:
            return found_fields[0]
        else:
            raise DataException("Could not find field")

    def __str__(self):
        return str(self.name)

    def map_to_object(self, obj, serializer, naming):
        self.name = naming.string_to_name(obj["name"])
        self.fields = serializer.map_to_object(obj["fields"], extra=naming)
        self.pk = serializer.map_to_object(obj["pk"], extra=naming)
        self.keys = serializer.map_to_object(obj["keys"], extra=naming)
        self.custom_queries = serializer.map_to_object(obj["custom_queries"], extra=naming)

    def map_to_dict(self, serializer: Serializer):
        obj = {
            "name": self.name.raw(),
            "fields": serializer.map_to_dict(self.fields),
            "pk": serializer.map_to_dict(self.pk),
            "keys": serializer.map_to_dict(self.keys),
            "custom_queries": serializer.map_to_dict(self.custom_queries)
        }
        return obj


serializer_instance.register_class(Table, "custom_queries:fields:keys:name:pk")


class Database(object):
    pass


class Database(object):
    name: Name
    tables: List[Table]

    def __init__(self, name: Name = None):
        self.name = name
        self.tables: List[Table] = []

    def map_to_object(self, obj, serializer, naming):
        self.name = naming.string_to_name(obj["name"])
        self.tables = serializer.map_to_object(obj["tables"], extra=naming)

    def get_table(self, table_name: str):
        result = [table for table in self.tables if table.name.raw() == table_name]
        if len(result) > 0:
            return result[0]
        return None


serializer_instance.register_class(Database)
