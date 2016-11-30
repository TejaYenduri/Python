import unittest
import requests
import json


class TestDbQueriesSvc(unittest.TestCase):

    def test_select(self):
        payload = {'tableName': 'department', 'columns': {'Mgr_ssn': '333445555'}}
        r = requests.post("http://127.0.0.1:5000/select", json=payload)
        rows = json.loads(r.text)
        size = len(rows)
        assert size, 2

    def test_select_error(self):
        payload = {'tableName': 'department', 'columns': 2}
        error = "2 is not of type 'object'"
        r = requests.post("http://127.0.0.1:5000/select", json=payload)
        rows = json.loads(r.text)
        assert rows == error

    def test_select1(self):
        payload1 = {'tableName': 'department', 'columns': {'Mgr_ssn': '333445555', 'Dnumber': 1}}
        r1 = requests.post("http://127.0.0.1:5000/select", json=payload1)
        rows = json.loads(r1.text)
        assert len(rows), 1
        assert rows[0][0] == 'Research'

    def test_select2(self):
        payload = {'tableName': 'department', 'columns': {'Mgr_ssn': '333445555', 'Dnumber': [1, 5]}}
        result = requests.post("http://127.0.0.1:5000/select", json=payload)
        rows = json.loads(result.text)
        assert len(rows), 2

    def test_insert(self):
        payload = {'tableName': 'Test', 'columns': {'lname': 'Howard', 'fname': 'Zoe'}}
        result = requests.post("http://127.0.0.1:5000/insert", json=payload)
        assert json.loads(result.text), "success"

    def test_update(self):
        payload = {'tableName': 'Test', 'columns': {'lname': 'Root'}, 'conditions': {'id': 2}}
        result = requests.post("http://127.0.0.1:5000/update", json=payload)
        assert json.loads(result.text), "success"

    def test_insert_all(self):
        files = {'file': open('data.csv', 'rb')}
        result = requests.post("http://127.0.0.1:5000/insert_all", params={'tablename': 'Test'}, files=files)
        assert json.loads(result.text), True
