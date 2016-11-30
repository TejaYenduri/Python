import csv

import jsonschema
import logging
import datetime
from flask import Flask, request, jsonify
from jsonschema import validate

import DbQueries

app = Flask(__name__)
schema = {
    "type": "object",
    "properties": {
        'tableName': {"type": "string"},
        'columns': {'type': "object"}
    }
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
log_name = str(datetime.date.today()) + 'api.log'
handler = logging.FileHandler(log_name)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@app.route("/select", methods=['POST', 'GET'])
def select():
    data = request.get_json()
    try:
        validate(data, schema)
        table_name = data.get('tableName')
        columns = data.get('columns', {})
        db_queries = DbQueries.DbQueries('MysqlConDetails.cfg')
        select_result = db_queries.select(table_name, columns)
        logger.info(select_result)
        return jsonify(select_result)
    except (jsonschema.exceptions.ValidationError, AttributeError) as e:
        message = e.args[0]
        logger.info(message)
        print type(message)
        return jsonify(message)


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
    if table_name and 'file' in request.files:
        fileobj = request.files['file']
        if fileobj and fileobj.filename != '' and fileobj.filename.endswith('.csv'):
            db_queries = DbQueries.DbQueries('MysqlConDetails.cfg')
            try:
                records = csv.DictReader(fileobj)
                logger.info(records)
                for record in records:
                    insert_result = db_queries.insert(record, table_name)
                    if insert_result != 'success':
                        print insert_result
                        result = False
            except csv.Error as e:
                logger.info(e.message)
                print e
                result = False
            finally:
                db_queries.close_connection()
        else:
            logger.info("invalid file")
            result = False
    else:
        result = False
    print result
    return jsonify(result)


if __name__ == "__main__":
    app.run()
