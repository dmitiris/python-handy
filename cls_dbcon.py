# -*- coding: utf-8 -*-

# standart modules
from datetime import datetime

# my modules
from psycopg2 import connect


class DB():
    def __init__(self):
        self.CON = False
        self.CUR = False
        self.CONSTR = ''


    def functions(self):
        print 'dbcon'
        print 'check_connection'
        print 'commit'
        print 'bulk_upsert'
        print 'bulk_delete'


    def dbcon(self, constr=None, reporting=True):
        if self.CON:
            try: self.CUR.close()
            except: pass
            try: self.CON.close()
            except: pass
            self.CUR = False
            self.CON = False
            if reporting:
                print '%s\tDisconnected from DB' % datetime.now()
        else:
            if constr:
                self.CONSTR = constr
            self.CON = connect(self.CONSTR)
            self.CUR = self.CON.cursor()
            if reporting:
                print '%s\tConnected to DB' % datetime.now()


    def check_connection(self):
        try:
            if not any([self.CON.closed, self.CUR.closed]):
                return True
        except AttributeError:
            try: self.CUR.close()
            except: pass
            try: self.CON.close()
            except: pass
        return False


    def commit(self):
        if self.check_connection():
            self.CON.commit()
            return '%s\t%s' % (datetime.now(), 'Commited')
        return '%s\t%s' % (datetime.now(), '(NF) Error. No DB connection.')


    def bulk_upsert(self, table, columns, unique, data, schema='public'):
        ''' data = [{}, {}, {}] '''
        # print 'DATA:', data
        if len(data) == 0: return None      # Just in case data is empty
        if not self.check_connection():
            self.dbcon()
        pcolumns = ', '.join(columns)
        value_plc = ','.join(['(%s)' % ','.join(['%s' for x in item]) for item in data])
        punique = ', '.join(unique)
        update = ', '.join(['%s=EXCLUDED.%s' % (column, column) for column in columns])
        sql_query = """
            INSERT INTO %(schema)s.%(table)s (%(columns)s) VALUES %(value_placeholder)s
            ON CONFLICT (%(unique)s) DO UPDATE SET %(update)s;
            """ % {
                'schema': schema, 'table': table, 'columns': pcolumns,
                'value_placeholder': value_plc, 'unique': punique, 'update': update
            }
        """"""
        if type(data[0]) == type({}):
            sql_data = [sublist[item] for sublist in data for item in columns]
        elif type(data[0]) == type([]):
            sql_data = [item for sublist in data for item in sublist]
        self.CUR.execute(sql_query, sql_data)
        return self.CUR.statusmessage

    def bulk_delete(self, table, data, data_key, column_key=False, schema='public'):
        if len(data) == 0: return 0
        if not self.check_connection():
            self.dbcon()
        if not column_key:
            column_key = data_key
        keys = ', '.join(["'%s'::text" % item[data_key] for item in data])
        sql_query = """ 
            DELETE FROM %(schema)s.%(table)s WHERE ARRAY[%(unique)s::text] <@ ARRAY[%(keys)s] 
            """ % {'schema': schema, 'table': table, 'unique': column_key, 'keys': keys}
        """"""
        self.CUR.execute(sql_query)
        return self.CUR.statusmessage


DBCon = DB()
