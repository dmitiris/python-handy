# -*- coding: utf-8 -*-

from os import listdir


def main(mypath='.', extension=None):
    if extension:
        return [f for f in listdir(mypath) if f.split('.')[-1] in extension]
    else:
        return [f for f in listdir(mypath)]

