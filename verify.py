#!/usr/bin/env python
from __future__ import print_function
import rdoinfo
import yaml


def verify(fn):
    info = rdoinfo.parse_info_file(fn)
    print(yaml.dump(info))
    cbstags = list_cbs_tags(info)
    for pkg in info['packages']:
        verify_cbs_tags(pkg, cbstags)
    print("\n%s looks OK" % fn)

def verify_cbs_tags(pkg, cbstags):
    if 'cbs-tags' in pkg.keys():
        tags = pkg['cbs-tags']
        for tag in tags.keys():
            if tag not in cbstags:
                raise Exception("cbs-tag %s for package %s does not exist" %
                                 (tag, pkg['name']))
            if tags[tag] is None:
                raise Exception("cbs-tag %s for package %s: %s is incorrect" %
                                 (tag, pkg['name'], tags[tag]))
    return True

def list_cbs_tags(info):
    tags = []
    for release in info['releases']:
        if 'cbs-tags' in release.keys():
            tags = tags + release['cbs-tags']
    return tags

if __name__ == '__main__':
    verify('rdo.yml')
