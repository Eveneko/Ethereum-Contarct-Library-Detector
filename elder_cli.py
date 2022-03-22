#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
# import logging
import sys

from elder import *

# require python version >= 3.6
assert (sys.version_info.major >= 3 and sys.version_info.minor >= 6)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='ELDER - Ethereum Library DEtectoR')

    subparsers = parser.add_subparsers(dest="subparsers",
                                       help='sub-command parser')

    crawler_parser = subparsers.add_parser('crawler',
                                           help='crawler parser')

    crawler_parser.add_argument('--update',
                        action='store_true',
                        help='update contracts csv.')

    crawler_parser.add_argument('--overwrite',
                        action='store_true',
                        help='clean contracts folder.')

    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='emit verbose debug output to stderr.')

    parser.add_argument('-vv',
                        '--prolix',
                        action='store_true',
                        help='higher verbosity level, including extra debug '
                            'messages from dataflow analysis and elsewhere.')

    args = parser.parse_args()

    if args.subparsers is None:
        parser.print_help()
        sys.exit(1)

    # set up logger
    log_level = logging.WARNING
    if args.prolix:
        log_level = logging.DEBUG
    elif args.verbose:
        log_level = logging.INFO
    logger.setLevel(log_level)
    

    if 'crawler' in args.subparsers:
        _crawler = Crawler(args.update, args.overwrite)
        _crawler()


if __name__ == '__main__':
    main()
