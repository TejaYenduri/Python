import pymysql
import ConfigParser
import logging
import time
import datetime


class DbQueries:
    def __init__(self, configname):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        log_name = str(datetime.date.today()) + '.txt'
        # create a file handler
        handler = logging.FileHandler(log_name)
        handler.setLevel(logging.INFO)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        # create ConfigParser to read data from config file
        config = ConfigParser.SafeConfigParser()
        config.read(configname)
        user = config.get('MySQLConfig', 'user')
        host = config.get('MySQLConfig', 'host')
        port = config.getint('MySQLConfig', 'port')
        password = config.get('MySQLConfig', 'passwd')
        database = config.get('MySQLConfig', 'db')
        connection_attempts = config.getint('MySQLConfig', 'conectionAttempts')
        # self._cursor = None
        self._connection = self.connect_db(host, port, user, password, database, connection_attempts)
        self._cursor = self._connection.cursor()

    def connect_db(self, host, port, user, password, database, connection_attempts):
        for i in range(connection_attempts):
            connection = None
            try:
                connection = pymysql.connect(host=host, port=port, user=user, passwd=password, db=database)
                if connection:
                    break
            except pymysql.err.Error as e:
                print "retrying"
                time.sleep(5)
                if i == connection_attempts - 1:
                    print "exceeded connection attempts. not able to connect"
                    raise e

        return connection

    def select(self, table, query_params):

        """ Takes table name and dictionary of column names and values as input.
        Selects and prints the rows from given table based on given columns.
        if dictionary is empty, returns all rows from the table"""

        try:
            # cursor = self._connection.cursor()
            if len(query_params) >= 1:
                # whereString = 'and '.join("%s = '%s'" % (key,value) for key,value in dict.iteritems())
                # query = "select * from %s where %s" % (table, whereString)
                params_list = self.build_query(query_params)
                where_string = 'and '.join('%s' % string for string in params_list)
                query = "select * from %s where %s" % (table, where_string)
            else:
                query = " select * from %s" % table
            self.logger.info(query)
            self._cursor.execute(query)
            result = self._cursor.fetchall()
            for row in result:
                print row
            return result
        except pymysql.err.Error as error:
            self.logger.error(error)
            code, message = error.args
            print code, message
        finally:
            self._cursor.close()
            self.close_connection()

    def build_query(self, columns):

        query_list = []
        for column, val in columns.iteritems():
            query_string = ''
            if type(val) == list:
                column_list = ','.join("'%s'" % value for value in val)
                query_string = ''.join("%s IN (%s)" % (column, column_list))
            else:
                query_string = ''.join("%s = '%s'" % (column, val))
            query_list.append(query_string)
        return query_list

    def insert(self, query_params, table):
        """ inserts values from dictionary into table """
        try:
            # cursor = self._connection.cursor()
            column_names = ','.join("%s" % value for value in query_params.iterkeys())
            column_values = ",".join("'%s'" % value for value in query_params.itervalues())
            query = "insert into %s(%s) values (%s)" % (table, column_names, column_values)
            self.logger.info(query)
            self._cursor.execute(query)
            self._connection.commit()
            return "success"
        except pymysql.err.Error as error:
            self.logger.error(error)
            code, message = error.args
            print code, message
            return message

    def update(self, query_params, table, condition_params):
        """ updates rows based on given conditions """
        try:
            # cursor = self._connection.cursor()
            set_string = ','.join("%s = '%s'" % (key, value) for key, value in query_params.iteritems())
            where_string = ','.join("%s = '%s'" % (key, value) for key, value in condition_params.iteritems())
            query = "update %s set %s where %s" % (table, set_string, where_string)
            print query
            self.logger.info(query)
            self._cursor.execute(query)
            self._connection.commit()
            return "success"
        except pymysql.err.Error as error:
            self.logger.error(error)
            code, message = error.args
            print code, message
            return message
        finally:
            self._cursor.close()
            self.close_connection()

    def close_connection(self):

        try:
            self._cursor.close()
            self._connection.close()
        except pymysql.err.Error as error:
            self.logger.error(error)
            code, message = error.args
            print code, message

# x = DbQueries('MysqlConDetails.cfg')
# y = DbQueries('MysqlConDetails.cfg')
# x.select('department', {})
# x.finalQuery('Employee',{'Dno':[1,4],'Sex':'M'})
# x.select('Employee', {'Dno': 1, 'Sex': 'M'})
# print "next select is executing "
# y.select('department', {})
# x.select('noDatabase',{})
# x.insert({'Dname':'HR','Dnumber':'6','Mgr_ssn':'999999999','Mgr_start_date':'2001-09-02'},'department')
# x.update({'Dname':'Management','Mgr_ssn':'987654321'},'department',{'Dnumber':6})
