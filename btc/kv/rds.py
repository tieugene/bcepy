"""
Key-value things.
Redis version (https://github.com/andymccurdy/redis-py)
"""

import redis


def _prn_key(key):
    """ Prints key as hex or string """
    if type(key) == int:
        return "%06x" % (key,)
    else:  # str
        return key


class KV(object):
    """ Key-value store over Kyoto Cabinet """

    def __init__(self):
        self.__counter = 0
        self.__db = None

    def open(self, dbno: int):
        """
        @param pfx: filename for storage (w/o ext)
        """
        self.__db = redis.Redis(unix_socket_path='/tmp/redis.sock', db=dbno)
        self.__counter = self.__db.dbsize()

    def clean(self):
        self.__db.flushdb()
        self.__counter = self.__db.dbsize()

    def get_count(self) -> int:
        """Ask counter
        @return: store size
        """
        return self.__counter  # self.__db.count()

    def exists(self, key) -> bool:
        return self.__db.exists(key) >= 0

    def get(self, key) -> int:  # or None
        """
        Get value by key
        TODO: add strict mode (get or exception)
        return: value or None
        """
        res = self.__db.get(key)    # value or None
        if res is not None:
            res = int(res)
        return res

    def add(self, key) -> int:
        """
         Adds record _strictly_ (no dup)
         @return: v of new record; exception if exists
         """
        res = self.__db.setnx(key, self.__counter)
        assert res, "Can't add record k=%s, v=%d" % (_prn_key(key), self.__counter)
        self.__counter += 1
        return self.__counter - 1
