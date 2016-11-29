from flask import Flask, request, jsonify
import DbQueries
import csv
import logging
import datetime

app = Flask(__name__)


@app.route("/select", methods=['POST', 'GET'])
def select():
    data = request.get_json()
    table_name = data.get('tableName')
    columns = data.get('columns', {})
    db_queries = DbQueries.DbQueries('MysqlConDetails.cfg')
    select_result = db_queries.select(table_name, columns)
    return jsonify(select_result)


@app.route("/insert", methods=['POST', 'GET'])
def insert():
    data = request.get_json()
    table_name = data.get('tableName')
    columns = data.get('columns', {})
    db_queries = DbQueries.DbQueries('MysqlConDetails.cfg')
    insert_result = db_queries.insert(columns, table_name)
    db_queries.close_connection()
    return jsonify(insert_result)


@app.route("/update", methods=['POST', 'GET'])
def update():
    data = request.get_json()
    table_name = data.get('tableName')
    columns = data.get('columns', {})
    conditions = data.get('conditions', {})
    db_queries = DbQueries.DbQueries('MysqlConDetails.cfg')
    update_result = db_queries.update(columns, table_name, conditions)
    return jsonify(update_result)


@app.route("/insert_all", methods=['POST'])
def read_csv():
    result = True
    table_name = request.args.get('tablename')
    if 'file' in request.files:
        fileobj = request.files['file']
        if fileobj and fileobj.filename != '' and fileobj.filename.endswith('.csv'):
            db_queries = DbQueries.DbQueries('MysqlConDetails.cfg')
            try:
                records = csv.DictReader(fileobj)
                for record in records:
                    insert_result = db_queries.insert(record, table_name)
                    if insert_result != 'success':
                        print insert_result
                        result = False
            except csv.Error as e:
                print e
                result = False
            finally:
                db_queries.close_connection()
        else:
            result = False
    else:
        result = False
    print result
    return jsonify(result)


if __name__ == "__main__":
    app.run()
