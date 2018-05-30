# -*- coding: utf-8 -*-
from re import match


class RCONF:
    def __init__(self, filepath):
        self.filepath = filepath
        self.attrib = self.readconf()
        self.keys = self.attrib.keys()
        for a in self.attrib:
            setattr(self, a.lower(), self.attrib[a.lower()])
            setattr(self, a.upper(), self.attrib[a.upper()])

    def readconf(self):
        res = {}
        with open(self.filepath) as f:
            data = f.read()
            lines = data.split('\n')  # should make support for \r
            for line in lines:
                g = match('(\w+)\s*=\s*([\w.,\-]+)', line)
                if g:
                    res[(str(g.group(1))).lower()] = str(g.group(2))
                    res[(str(g.group(1))).upper()] = str(g.group(2))
        return res

    def __str__(self):
        return 'Configuration object from "%s"' % self.filepath

    def __repr__(self):
        return self.__str__()
