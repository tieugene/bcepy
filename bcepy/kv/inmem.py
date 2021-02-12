"""
Key-value things.
In-memory version.
"""


def prn_key(key):
    """ Prints key as hex or string """
    if type(key) == int:
        return "%06x" % (key,)
    else:  # str
        return key


class KV(object):
    """ Key-value store over built-in dict """

    def __init__(self):
        self.__counter = 0
        self.__db = dict()

    def open(self, fname: str = None):
        pass

    def clean(self):
        """Clean all data"""
        self.__db.clear()
        self.__counter = 0

    def get_count(self) -> int:
        """Ask counter
        @return: store size
        """
        return len(self.__db)

    def exists(self, key: bytes) -> bool:
        """Check key exists
        TODO: return id or None
        @param key: key to check
        @return: True if exists, False if not
        """
        return key in self.__db

    def get(self, key: bytes) -> int:
        """Get existant record
        @param key: key of record to get
        @return: record value or None
        """
        return self.__db.get(key, None)

    def add(self, key: bytes) -> int:
        """Add key to store strictly
        TODO: err if exists | or not
        @param key: key to  store
        @return: value of added record
        """
        self.__db[key] = self.__counter
        self.__counter += 1
        return self.__counter - 1

    def print(self):
        """ Print out self content"""
        for k, v in self.__db:
            print(k, int(v))
