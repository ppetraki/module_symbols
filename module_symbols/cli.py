#!/usr/bin/env python
# relevant docs: http://www.redhat.com/f/summitfiles/presentation/May31/Open%20Source%20Dynamics/Troan_OpenSourceProprietyPersp.pdf

from __future__ import print_function

import sys
import os
import argparse
import logging
import importlib

PROGRAM='module_symbols'

def basic_args(parser): # pragma: no cover
    parser.add_argument('--debug', action='store_true',
            help='display debug output, implies --verbose')
    parser.add_argument('--verbose', action='store_true',
            help='increase verbosity')


def global_args(parser): # pragma: no cover
    basic_args(parser)

def setup_parser(): # pragma: no cover
    p = argparse.ArgumentParser(prog=PROGRAM,
            description="Reporting tool that determines the EXPORT_SYMBOL "
            "license type.",
            usage='%s report --tree ~/Sandbox/trees/linux '
                '--modules ../sshcache/flashcache/src/*.ko' % PROGRAM)
    sp = p.add_subparsers(title='actions', dest='action', metavar='actions')

    report = sp.add_parser('report', help='generate compliance report')

    report.add_argument('--tree', action='store', dest='tree',
            help='git tree for compliance check', nargs=1)

    report.add_argument('--modules', action='store', dest='modules',
            help='module KOs to analyze', nargs='+')

    report.add_argument('--full', action='store_true', dest='full',
            default=False,
            help='retain parsed unresolved symbols in report')

    version = sp.add_parser('version', help='display version')

    basic_args(version)
    global_args(report)
    return p

def setup_logging(verbose=None, debug=None): # pragma: no cover
    logger = logging.getLogger(PROGRAM)
    logger.setLevel(logging.INFO)

    if debug:
        logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # formatting
    f = '%(levelname)s %(name)s: %(message)s'
    if verbose:
        f = '%(asctime)s ' + f

    formatter = logging.Formatter(f)
    ch.setFormatter(formatter)

    if verbose is None:
        ch = logging.NullHandler()

    logger.addHandler(ch)
    return logger

def main(args=None):
    parser = setup_parser()

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(0)

    known, unknown = parser.parse_known_args(args)

    log = setup_logging(verbose=known.verbose, debug=known.debug)

    log.debug('arguments: %s, unknown: %s' % (str(known), str(unknown)))

    if known.action  == 'version':
        import pkg_resources
        version = pkg_resources.get_distribution("module-symbols").version
        print("%s %s" % ('module-symbols', version))
        sys.exit(0)

    if known.action == 'report':
        if not known.tree or not known.modules:
            parser.print_usage()

    action = importlib.import_module("..%s" % known.action,
            '%s.%s' % (PROGRAM, known.action))
    log.debug('accessing %s.main' % known.action)
    exit = action.main(known, unknown)
    sys.exit(exit)
