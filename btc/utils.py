import os
import sys
import time
import datetime
import platform
import hashlib
import base58
from pathlib import Path
from resource import getpagesize
import btc.heap as heap

PAGESIZE = getpagesize()
PATH = Path('/proc/self/statm')


def snow() -> str:
    return datetime.datetime.now().strftime('%y.%m.%d %H:%M:%S')


def eprint(s: str):
    print(s, file=sys.stderr)
    if heap.logfile:
        print(s, file=heap.logfile)
        heap.logfile.flush()


def load_conf(btc_conf_file: str = None) -> str:
    """
    Load bitcoin.conf.
    Powered by python-bitcoinlib.rpc module.
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
    # Extract contents of bitcoin.conf to build service_url
    conf = {}
    try:
        with open(btc_conf_file, 'r') as fd:
            for line in fd.readlines():
                if '#' in line:
                    line = line[:line.index('#')]
                if '=' not in line:
                    continue
                k, v = line.split('=', 1)
                conf[k.strip()] = v.strip()
    # Treat a missing bitcoin.conf as though it were empty
    except FileNotFoundError:
        pass
    # Defaults
    conf['rpchost'] = conf.get('rpcconnect', 'localhost')
    conf['rpcport'] = int(conf.get('rpcport', '8332'))
    return ('http://%s:%s@%s:%d' %
            (conf['rpcuser'], conf['rpcpassword'], conf['rpchost'], conf['rpcport']))


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
