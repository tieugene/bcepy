"""
Key-value things.
TKRZW version
"""

import tkrzw


EXT = '.tkh'    # (forgot)


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
        self.__db = tkrzw.DBM()
        self.__fname = None

    @staticmethod
    def name():
        return 'tkrzw'

    def open(self, fname: str):
        """
        @param fname: filename for storage (w/o ext)
        """
        self.__fname = fname + EXT
        res = self.__db.Open(self.__fname, True)  # , truncate=True
        assert res, "Can't open DB '%s'" % self.__fname
        self.__counter = self.__db.Count()

    def clean(self):
        self.__db.Clear()
        self.__counter = self.__db.Count()

    def get_count(self) -> int:
        """Ask counter
        @return: store size
        """
        return self.__counter  # self.__db.count()

    def exists(self, key: bytes) -> bool:
        return self.__db.Get(key) is not None

    def get(self, key: bytes) -> int:
        """
        Get value by key
        TODO: add strict mode (get or exception)
        return: value or None
        """
        res = self.__db.Get(key)    # value or None
        if res is not None:
            res = int(res)
        return res

    def add(self, key: bytes) -> int:
        """
         Adds record _strictly_ (no dup)
         @return: v of new record; exception if exists
         """
        res = self.__db.Set(key, self.__counter)  # True on success, False if exists; set == add_or_replace
        assert res, "Can't add record k=%s, v=%d" % (_prn_key(key), self.__counter)
        self.__counter += 1
        return self.__counter - 1
