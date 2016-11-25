import unittest
import DbQueries
import pymysql


class TestingDbQueries(unittest.TestCase):
    def setUp(self):
        self.dbQueries = DbQueries.DbQueries('MysqlConDetails.cfg')

    def test_connectdb(self):
        self.assertNotEqual(self.dbQueries._cursor, None)

    def test_select(self):
        self.dbQueries.select('Employee', {})
        size = self.dbQueries._cursor.rowcount
        self.assertEqual(size, 9)

    def test_select1(self):
        self.dbQueries.select('department', {'Dnumber': 1, 'Dname': 'Research'})
        cursor = self.dbQueries._cursor
        size = cursor.rowcount
        self.assertEqual(size, 1)
        for row in cursor:
            self.assertEqual(row[2], '333445555')

    def test_insert(self):
        deptRecord = {'Dname': 'IT', 'Dnumber': 2, 'Mgr_ssn': '987654321', 'Mgr_start_date': '2010-03-30'}
        self.dbQueries.insert(deptRecord, 'department')
        size = self.dbQueries._cursor.rowcount
        self.assertEqual(size, 1)

    def test_update(self):
        self.dbQueries.update({'Mgr_start_date': '2009-05-31'}, 'department', {'Dnumber': 2})
        size = self.dbQueries._cursor.rowcount
        self.assertEqual(size, 1)


if __name__ == '__main__':
    unittest.main()
