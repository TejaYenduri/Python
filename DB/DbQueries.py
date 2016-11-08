import pymysql
import ConfigParser
import logging
from time import sleep

class DbQueries:
	def __init__(self, configName):
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger(__name__)
		#create a file handler
		handler = logging.FileHandler('DbQueries.log')
		handler.setLevel(logging.INFO)
		# create a logging format
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)
		#create ConfigParser to read data from config file
		config = ConfigParser.SafeConfigParser()
		config.read(configName)
		user = config.get('MySQLConfig','user')
		host = config.get('MySQLConfig','host')
		port = config.getint('MySQLConfig','port')
		password = config.get('MySQLConfig','passwd')
		database = config.get('MySQLConfig','db')
		connectionAttempts = config.getint('MySQLConfig','conectionAttempts')
		#self._cursor = None
		self._cursor = self.connectDb(host,port,user,password,database,connectionAttempts) 	
		#self._connection = pymysql.connect(host=host, port=port, user=user, passwd=password, db=database)

	def connectDb(self,host,port,user,password,database,connectionAttempts):
		for i in range(connectionAttempts):
			try:
				self._connection = pymysql.connect(host=host, port=port, user=user, passwd=password, db=database)
				cursor = self._connection.cursor()
			except pymysql.err.Error as error:
				time.sleep(5)
			finally:
				if cursor:
					break
		return cursor


	#Selects and prints the rows from given table based on given columns. if dictionary is empty, returns all rows from the table
	def select(self,table,dict):
		try:
			#cursor = self._connection.cursor()
			if(len(dict) >= 1):
				#whereString = 'and '.join("%s = '%s'" % (key,value) for key,value in dict.iteritems())
				#query = "select * from %s where %s" % (table, whereString)	
				qStringList = self.buildQuery(dict)
				whereString = 'and '.join('%s'%string for string in qStringList)
				query = "select * from %s where %s"%(table,whereString)
			else:
				query =" select * from %s" %(table)
			self.logger.info(query)
			self._cursor.execute(query)
			for row in self._cursor:
				print row
		except pymysql.err.Error as error:
			self.logger.error(error)
			code, message = error.args
			print code, message
		finally:
			self._cursor.close()
			self.closeConnection()
	def buildQuery(self,columns):
		queryList = []
		for column,val in columns.iteritems():
			qString =''
			if(type(val) == list):
				columnList =','.join("'%s'"% value for value in val)
				qString = ''.join("%s IN (%s)"%(column,columnList))
			else :
				 qString = ''.join("%s = '%s'"%(column,val))
			queryList.append(qString)
		return queryList

	#inserts values from dictionary into table
	def insert(self,dict,table):
		try:
			#cursor = self._connection.cursor()
			columnNames = ','.join("%s" % (value) for value in dict.iterkeys())
			columnValues = ",".join("'%s'" % (value) for value in dict.itervalues()) 
			query = "insert into %s(%s) values (%s)"%(table,columnNames,columnValues)
			self.logger.info(query)
			self._cursor.execute(query)
			self._connection.commit()
			print "success"
		except pymysql.err.Error as error:
			self.logger.error(error)
			code, message = error.args
			print code, message
		finally:
			self._cursor.close()
			self.closeConnection()

	#updates rows based on given conditions
	def update(self,dict,table,conditionDict):
		try:
			#cursor = self._connection.cursor()
			setString = ','.join("%s = '%s'" % (key,value) for key,value in dict.iteritems())
			whereString = ','.join("%s = '%s'" % (key,value) for key,value in conditionDict.iteritems())
			query = "update %s set %s where %s" % (table, setString, whereString)
			self.logger.info(query)
			self._cursor.execute(query)
			self._connection.commit()
			print "success"
		except pymysql.err.Error as error:
			self.logger.error(error)
			code, message = error.args
			print code, message
		finally:
			self._cursor.close()
			self.closeConnection()

	def closeConnection(self):
		self._connection.close()

x=DbQueries('MysqlConDetails.cfg')
y=DbQueries('MysqlConDetails.cfg')
#x.select('department',{})
#x.finalQuery('Employee',{'Dno':[1,4],'Sex':'M'})
x.select('Employee',{'Dno':1,'Sex':'M'})
print "next select is executing "
y.select('department',{})
#x.select('noDatabase',{})
#x.insert({'Dname':'HR','Dnumber':'6','Mgr_ssn':'999999999','Mgr_start_date':'2001-09-02'},'department')
#x.update({'Dname':'Management','Mgr_ssn':'987654321'},'department',{'Dnumber':6})
