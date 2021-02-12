__version__ = "0.0.1"

# 1. system
import argparse
import datetime
# 2. local
from . import body, heap


def __init_cli():
    """ Handle CLI """
    parser = argparse.ArgumentParser(description='Process blockchain.')
    parser.add_argument('-m', '--mode', metavar='n', type=int, nargs='?', default=0,
                        help='Mode: 0 - simple walk, 1 - deep walk, 2 - full process (default=0)')
    parser.add_argument('-f', '--from', dest='beg', metavar='n', type=int, nargs='?', default=None,
                        help='kBk start from (default=0)')
    parser.add_argument('-q', '--qty', metavar='n', type=int, nargs='?', default=1, help='kBk to process (default=1)')
    # parser.add_argument('-k', '--keep', action='store_true', help='Keep existing Tx/Addr (default=false)')
    parser.add_argument('-l', '--log', action='store_true', help='Logfile (default=false)')
    parser.add_argument('-o', '--out', action='store_true', help='DB output (default=false)')
    parser.add_argument('-c', '--cache', type=str, metavar='dir', nargs='?', default=".", help='Cache dir (default=.)')
    return parser


def main():
    """
    CLI commands/options handler.
    """
    parser = __init_cli()
    args = parser.parse_args()
    if args.mode is None:
        parser.print_help()
    elif args.mode > 2:
        print("Wrong mode: %d" % args.mode)
    else:
        if args.log:
            heap.Opts.log = True
            heap.logfile = open("%s.log" % datetime.datetime.now().strftime('%y%m%d%H%M%S'), 'wt')
        heap.Opts.mode = args.mode
        # heap.Opts.keep = args.keep
        heap.Opts.out = args.out
        heap.Opts.kvdir = args.cache
        body.walk(args.beg, args.qty)
