import requests

payload = {'tableName': 'department', 'columns': {'Mgr_ssn': '333445555'}}
r = requests.post("http://127.0.0.1:5000/select", json=payload)
print (r.text)

payload1 = {'tableName': 'department', 'columns': {'Mgr_ssn': '333445555', 'Dnumber': 1}}
r1 = requests.post("http://127.0.0.1:5000/select", json=payload1)
print (r1.text)

payload2 = {'tableName': 'department', 'columns': {'Mgr_ssn': '333445555', 'Dnumber': [1, 5]}}
r2 = requests.post("http://127.0.0.1:5000/select", json=payload2)
print (r2.text)
