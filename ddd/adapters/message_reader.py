import arrow


class MessageReader(object):
    """
    A tolerant reader for reading float, int, str, etc. from a message (dict).
    See 'tolerant reader' pattern.
    """
    def __init__(self, message):
        super().__init__()
        self.message = message

    def bool_value(self, keys, default=False):
        value = self.get_value(self.message, keys)
        if isinstance(value, bool):
            return value

        for m in ["true", True, "1", 1]:
            if value == m and type(value) == type(m):
                return True

        for m in ["false", False, "0", 0]:
            if value == m and type(value) == type(m):
                return False

        return default

    def dict_value(self, keys, default={}):
        value = self.get_value(self.message, keys)
        if isinstance(value, dict):
            return value
        else:
            return default

    def list_value(self, keys, default=[]):
        value = self.get_value(self.message, keys)
        if isinstance(value, list):
            return value
        else:
            return default

    def string_value(self, keys, default=None):
        value = self.get_value(self.message, path=keys, default=default)
        if isinstance(value, str):
            return value
        elif value is None:
            return default
        return str(value)

    def entity_id_value(self, keys, class_, default=None):
        value = self.get_value(self.message, path=keys, default=default)
        if isinstance(value, str):
            return class_(value)
        elif value is None:
            return default
        return None

    def lang_value(self, keys, default=None):
        value = self.get_value(self.message, path=keys, default=default)
        _map = {
            'en': 'en',
            'eng': 'en',
            'sv': 'sv',
            'swe': 'sv',
        }
        if isinstance(value, str):
            if value in _map:
                return _map[value]
            return value
        return default

    def date_value(self, keys):
        value = self.get_value(self.message, keys)
        if not isinstance(value, str):
            return None
        else:
            date = None
            try:
                date = arrow.get(value)
            except:
                pass
            return date

    def date_value_iso8601(self, keys):
        date = self.date_value(keys=keys)
        if date:
            return date.format("YYYY-MM-DDTHH:mm:ss.SSSSSSZZ")
        return None

    def int_value(self, keys):
        value = self.get_value(self.message, keys)
        if isinstance(value, int):
            return value
        else:
            return int(value) if isinstance(value, str) and value.isdigit() else None

    def float_value(self, keys):
        value = self.get_value(self.message, keys)
        if isinstance(value, float):
            return value
        elif isinstance(value, int):
            return float(value)
        else:
            return float(value) if isinstance(value, str) and value.replace('.','',1).isdigit() else None

    def has_value(self, keys):
        value = self.get_value(self.message, keys, default=None)
        return value is not None

    def get_value(self, the_dict, path, default=""):
        keys = path.split('.')
        if the_dict != None and keys[0] in the_dict:
            if len(keys) == 1:
                return the_dict[keys[0]]
            else:
                return self.get_value(the_dict[keys[0]], ".".join(keys[1:]), default)
        else:
            return default
