# -*- coding: utf-8 -*-
from re import match


class RCONF:
    def __init__(self, filepath):
        self.filepath = filepath
        attrib = self.readconf()
        self.keys = attrib.keys()
        for a in attrib:
            setattr(self, a, attrib[a])

    def readconf(self):
        res = {}
        with open(self.filepath) as f:
            data = f.read()
            lines = data.split('\n')  # should make support for \r
            for line in lines:
                g = match('(\w+)\s*=\s*(\w+)', line)
                if g:
                    res[str(g.group(1))] = str(g.group(2))
        return res

    def __str__(self):
        return 'Configuration object from "%s"' % self.filepath

    def __repr__(self):
        return self.__str__()
