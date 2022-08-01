import datetime
import json

from common.entities.db_config import Base
import decimal

class GenericService:
    @staticmethod
    def get_root_exception(exc: Exception):
        while hasattr(exc, 'inner_exception') and exc.inner_exception is not None:
            exc = exc.inner_exception
        return exc

    @staticmethod
    def compose_datetime(date: str, hour: int, minute: int, date_split_delim: str):
        split_date = date.split(date_split_delim)
        date_year = int(split_date[2])
        date_month = int(split_date[1])
        date_day = int(split_date[0])

        compose_date = datetime.datetime(date_year, date_month, date_day,  hour, minute, 0)
        return compose_date

    @staticmethod
    def has_method(o, name):
        return callable(getattr(o, name, None))

    @staticmethod
    def wrap_list_dict(response: list, props: tuple):
        retval = []
        for val in response:
            # FOR EVERY ITEM IN LIST
            val_dict = {}
            for i in range(len(props)):
                # FOR EVERY PROPERTY IN ITEM
                val_dict[props[i]] = val[i]
            retval.append(val_dict)
        return retval

    @staticmethod
    def get_serialized_response(response):
        serialize_response = None
        if response is None:
            serialize_response = None
        elif isinstance(response, list):
            serialize_response = [GenericService.serialize(val) for val in response]
        else:
            serialize_response = GenericService.serialize(response)
        return serialize_response

    @staticmethod
    def serialize(obj):
        # BASE (ALCHEMY)
        serialize = getattr(type(obj), 'serialize', None)
        if serialize:
            return obj.serialize
        return obj

    @staticmethod
    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return json.dumps(float(obj))
        serialize = getattr(type(obj), 'serialize', None)
        if serialize:
            return obj.serialize
        raise TypeError("Type %s not serializable" % type(obj))

