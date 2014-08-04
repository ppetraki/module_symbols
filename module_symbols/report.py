import yaml
import logging
import re

from subprocess import Popen, PIPE
from os.path import abspath

log = logging.getLogger('module_symbols.report')

def module_name(ko):
    return ko.split('/')[-1]

def main(args, unknown):
    if unknown:
        raise Exception('%s are not recognized parameters' % ' '.join(unknown))
    log.debug('entering reporter')

    # XXX I suppose one could argue that validating against multiple trees
    # could be a useful feature, however in the meanwhile.
    args.tree = args.tree[0]

    if args.debug:
        log.debug('args content %s' % args)
        log.debug(args.modules)
        log.debug(args.tree)

    log.debug('building symbol list')
    kos = {}

    for ko in args.modules:
        kos[module_name(ko)] = {'symbols': [], 'unresolved_gpl_symbols': []}

    for m in args.modules:
        name = module_name(m)
        cmd = 'nm {0}'
        log.debug("Processing %s" % cmd.format(m))

        p = Popen(cmd.format(m).split(), stdout=PIPE)
        lines = p.communicate()[0]

        for line in lines.split('\n'):
            kos[name]['symbols'].append(line)

    if args.debug:
        for k,v in kos.items():
            log.debug("module %s, values %s" % (k, len(v['symbols'])))

        log.debug("complete symbol list")
        log.debug(yaml.dump(kos, default_flow_style=False))

    for k,v in kos.items():
        for sym in v['symbols']:
            m = re.search('^.* U ', sym)
            if m:
                sname = sym.split()[-1]
                cmd = 'git grep {0}'
                p = Popen(cmd.format(sname).split(),
                        stdout=PIPE,
                        cwd=abspath(args.tree))
                lines = p.communicate()[0]

                for line in lines.split('\n'):
                    m = re.search('EXPORT_SYMBOL_GPL\(%s\)' % sname, line)
                    if m:
                        if args.debug:
                            log.debug('  symbol %s is unresolved' % sname)
                            log.debug(4*' ' + line)
                        tmp = line.strip()
                        tmp = tmp.split(':')[0]
                        v['unresolved_gpl_symbols'].append(tmp + ':' + sname)
                        break
    if not args.full:
        # no need to clutter the output with all unresolved symbols
        for k,v in kos.items():
            v.pop('symbols')

    print(yaml.dump(kos, default_flow_style=False))
