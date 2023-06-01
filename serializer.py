#!/usr/bin/python3
import inspect
import json
from enum import Enum


class Serializer(json.JSONEncoder):
    classes = dict()

    def default(self, o):  # pylint: disable=E0202
        if hasattr(o, 'json'):
            return o.json()
        if hasattr(o, '__dict__'):
            return o.__dict__
        return str(o)

    @staticmethod
    def get_object_signature(_dict):
        return ':'.join(sorted(_dict.keys()))

    @staticmethod
    def get_class_signature(sig):
        return ":".join(sorted([v for v in sig if not v.startswith("_")]))

    def register_object(self, obj, signature=""):
        if signature == "":
            signature = self.get_object_signature(obj.__dict__)
        self.classes[signature] = type(obj)

    def register_class(self, cls, signature=""):
        if signature == "":
            sig = [s for s in inspect.getmembers(cls) if s[0] == "__annotations__"]
            signature = self.get_class_signature(sig[0][1])
        self.classes[signature] = cls

    def serialize(self, obj, pretty: bool = False):
        d = self.map_to_dict(obj)
        return json.dumps(d, cls=Serializer, indent="\t" if pretty else None)

    def de_serialize(self, json_data, extra=None):
        obj = json.loads(json_data)
        obj = self.map_to_object(obj, extra=extra)
        return obj

    def map_to_dict(self, obj):
        if isinstance(obj, list):
            new_list = []
            for item in obj:
                new_item = self.map_to_dict(item)
                new_list.append(new_item)
            return new_list

        if isinstance(obj, Enum):
            if hasattr(obj, 'map_to_dict'):
                return obj.map_to_dict(self)
            else:
                return str(obj).replace("{}.".format(type(obj).__name__), "")

        if not isinstance(obj, dict):
            if hasattr(obj, 'map_to_dict'):
                d = obj.map_to_dict(self)
                if not isinstance(d, dict):
                    return d
            elif hasattr(obj, '__dict__'):
                d = {k: v for (k, v) in obj.__dict__.items() if not k.startswith("_")}
            else:
                return obj
        else:
            d = obj

        for child in d:
            d[child] = self.map_to_dict(d[child])
        return d

    def map_to_object(self, obj, cls=None, extra=None):
        if type(obj) is list:
            new_list = []
            for item in obj:
                new_item = self.map_to_object(item, cls=cls, extra=extra)
                new_list.append(new_item)
            return new_list

        if not isinstance(obj, dict):
            return obj

        must_remap_properties = True
        signature = self.get_object_signature(obj)
        if signature in self.classes or cls:
            if cls:
                clas = cls
            else:
                clas = self.classes[signature]

            new_obj = clas()
            if hasattr(new_obj, 'map_to_object'):
                new_obj.map_to_object(obj, self, extra)
                must_remap_properties = False
            else:
                for key in new_obj.__dict__.keys():
                    new_obj.__dict__[key] = obj.get(key, "")

            obj = new_obj

        if must_remap_properties:
            if isinstance(obj, dict):
                props = obj
            else:
                props = obj.__dict__

            for child in props:
                props[child] = self.map_to_object(props[child], extra=extra)

        return obj


# customer = entities.Customer(1, 'Stephen', datetime.datetime.now())
# customer.addresses.append(entities.Address(id=1, addresstype='Normal', street='Street', city='City', code='Code', country='Country'))
# customer.addresses.append(entities.Address(id=2, addresstype='Extra', street='Street', city='City', code='Code', country='Country'))
# customer.orders.append(entities.Order(id=1, orderdate=datetime.datetime.now(), amount=100))
# customer.orders.append(entities.Order(id=2, orderdate=datetime.datetime.now(), amount=100))
# ser = Serializer()
# ser.register(entities.Customer())
# ser.register(entities.Envelope())
# ser.register(entities.Address())
# ser.register(entities.Order())
# ser.register(utils.Version())

# envelope = entities.Envelope('create', customer)
# data = ser.serialize(envelope)
# print(data)
# item = ser.deSerialize(data)
# print(item)
# print(item.object.address)

serializer_instance = Serializer()
