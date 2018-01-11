# -*- coding:utf-8 -*-
from datetime import datetime

# from cls_log import LogObj as LOG
class LOG():
    def __init__(self):
        self.log_name = 'default.log'
        self.to_log = False


    def if_log_exists(self):
        try:
            fp = open(self.log_name, 'r')
            fp.close()
            return True
        except:
            return False


    def show(self, *args):
        data = [str(datetime.now()),]
        data += [str(item) for item in args]
        if self.to_log:
            if self.if_log_exists():
                print >> open(self.log_name, 'a'), '\t'.join(data)
            else:
                print >> open(self.log_name, 'w'), '\t'.join(data)
        else:
            print '\t'.join(data)


LogObj = LOG()
