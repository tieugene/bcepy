import os
import sys
import time
import datetime
import platform
import hashlib
import base58
from pathlib import Path
from resource import getpagesize
from configobj import ConfigObj
import btc.heap as heap

PAGESIZE = getpagesize()
PATH = Path('/proc/self/statm')


def snow() -> str:
    """ String repr of current datetime """
    return datetime.datetime.now().strftime('%y.%m.%d %H:%M:%S')


def eprint(s: str):
    """ Print log into stderr [and logfile] """
    print(s, file=sys.stderr)
    if heap.logfile:
        print(s, file=heap.logfile)
        heap.logfile.flush()


def load_conf(btc_conf_file: str = None) -> str:
    """
    Load bitcoin.conf.
    @param btc_conf_file
    @return connection url (default "http://login:password@127.0.0.1:8332")
    """
    # Figure out the path to the bitcoin.conf file
    if btc_conf_file is None:
        if platform.system() == 'Darwin':
            btc_conf_file = os.path.expanduser('~/Library/Application Support/Bitcoin/')
        elif platform.system() == 'Windows':
            btc_conf_file = os.path.join(os.environ['APPDATA'], 'Bitcoin')
        else:
            btc_conf_file = os.path.expanduser('~/.bitcoin')
        btc_conf_file = os.path.join(btc_conf_file, 'bitcoin.conf')
    if not os.path.exists(btc_conf_file):
        raise Exception("Can't find '{}'".format(btc_conf_file))
    cfg = ConfigObj(btc_conf_file)
    if ('rpcuser' not in cfg) or ('rpcpassword' not in cfg):
        raise Exception("Not 'rpcuser' or 'rpcpassword' in bitcoin.conf")
    if 'rpcconnect' not in cfg:
        cfg['rpcconnect'] = 'localhost'
    if 'rpcport' not in cfg:
        cfg['rpcport'] = '8332'
    return ('http://{}:{}@{}:{}'.format(
            cfg['rpcuser'], cfg['rpcpassword'], cfg['rpcconnect'], cfg['rpcport']))


class Timer(object):
    def __init__(self):
        self.__t0 = 0

    def start(self):
        self.__t0 = int(time.time())

    def now(self) -> int:
        return int(time.time()) - self.__t0


class Memer(object):
    def get_used_mem(self) -> int:
        """Return the current resident set size in bytes."""
        # statm columns are: size resident shared text lib data dt
        __statm = PATH.read_text()
        __fields = __statm.split()
        return (int(__fields[1]) * PAGESIZE) >> 20

    def __init__(self):
        self.__m0 = 0

    def start(self):
        self.__m0 = self.get_used_mem()

    def now(self) -> int:
        return self.get_used_mem() - self.__m0

def pk2addr(s: str) -> str:
    """
    Converts pubkey into base58 addr
    @param s - pubkey string (130 chars)
    @return base58 pubkey representation
    """
    r160 = b'\0'+hashlib.new('ripemd160', hashlib.sha256(bytes.fromhex(s)).digest()).digest()
    return base58.b58encode(r160 + hashlib.sha256(hashlib.sha256(r160).digest()).digest()[:4]).decode('ascii')
