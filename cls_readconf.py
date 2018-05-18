# -*- coding: utf-8 -*-
from re import match


class RCONF:
    def __init__(self, filepath):
        self.filepath = filepath
        self.attrib = self.readconf()
        self.keys = self.attrib.keys()
        for a in self.attrib:
            setattr(self, lower(a), self.attrib[lower(a)])
            setattr(self, upper(a), self.attrib[upper(a)])

    def readconf(self):
        res = {}
        with open(self.filepath) as f:
            data = f.read()
            lines = data.split('\n')  # should make support for \r
            for line in lines:
                g = match('(\w+)\s*=\s*([\w\.\,\-]+)', line)
                if g:
                    res[lower(str(g.group(1)))] = str(g.group(2))
                    res[upper(str(g.group(1)))] = str(g.group(2))
        return res

    def __str__(self):
        return 'Configuration object from "%s"' % self.filepath

    def __repr__(self):
        return self.__str__()
