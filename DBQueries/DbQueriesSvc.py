from flask import Flask, request, jsonify
import DbQueries

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


if __name__ == "__main__":
    app.run()
