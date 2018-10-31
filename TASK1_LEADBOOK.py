import mysql.connector
import json, ast
from mysql.connector import Error

import socketio
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import eventlet

sio = socketio.Server()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def query_sql():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="rahasia2016",
      database="leadbook"
    )

    mycursor = mydb.cursor()

    try:
        mycursor.execute("select cont.id, cont.name, cont.email, cont.company_id, comp.name, comp.country, comp.revenue from company comp, contact cont where cont.company_id = comp.id;")

        desc = mycursor.description
        data = []
        for row in mycursor.fetchall():
            row_dict = {}
            row_dict['id'] = row[0]
            row_dict['name'] = row[1]
            row_dict['email'] = row[2]
            row_dict['company'] = {}
            row_dict['company']['id'] = row[3]
            row_dict['company']['name'] = row[4]
            row_dict['company']['country'] = row[5]
            row_dict['company']['revenue'] = row[6]
            
            data.append(row_dict)

    except Error as e:
        print(e)

    finally:
        mycursor.close()
        mydb.close()

    contacts = ast.literal_eval(json.dumps(data))
    return contacts



@app.route("/contacts/", methods=['GET'])
@cross_origin()
def get_all_contacts():
    print(request.args)
    print(bool(request.args))
    
    result = {}
    if 'company_id' in request.args:
        company_id = request.args.get('company_id', None)

        result['data'] = []
        try:
            for contact in contacts:
                if contact['company']['id'] == int(company_id):
                    result['data'].append(contact)

        except Exception as e:
            print(e)
            result['message'] = e

        if not result['data']:
            result['status_code'] = 200
            result['message'] = "company_id {} doesn't exist".format(company_id)
            return jsonify(result)
        else:
            result['status_code'] = 200
            result['message'] = 'successful'

        return jsonify(result)

    elif 'revenue_gte' in request.args:
        revenue = request.args.get('revenue_gte', None)
        result['data'] = []
        try:
            for contact in contacts:
                if contact['company']['revenue'] >= int(revenue):
                    result['data'].append(contact)

        except Exception as e:
            print(e)
            result['message'] = e


        if not result['data']:
            result['status_code'] = 200
            result['message'] = "revenue {} doesn't exist".format(revenue)
            return jsonify(result)
        else:
            result['status_code'] = 200
            result['message'] = 'successful'

        return jsonify(result)

    elif 'name' in request.args:
        name = request.args.get('name', None)

        result['data'] = []
        try:
            for contact in contacts:
                if contact['name'] == name:
                    result['data'].append(contact)

        except Exception as e:
            print(e)


        if not result['data']:
            result['status_code'] = 200
            result['message'] = "name {} doesn't exist".format(name)
            return jsonify(result)

        result['status_code'] = 200
        result['message'] = 'successful'

        return jsonify(result)

    elif not request.args:
        result['status_code'] = 200
        result['message'] = 'successful'
        result['data'] = contacts
        return jsonify(result)

    else:
        result['status_code'] = 404
        result['message'] = 'Parameter should be <revenue_gte>, <name>, or <company_id>'
        return jsonify(result)




@app.route("/contacts/<contact_id>", methods=['GET'])
@cross_origin()
def get_contact(contact_id):
    result = {}

    try:
        for contact in contacts:
            if contact['id'] == int(contact_id):
                result['data'] = contact
                break
    except Exception as e:
        print(e)

    if 'data' not in result:
        result['status_code'] = 404
        result['message'] = "contact_id {} doesn't exist".format(contact_id)
        return jsonify(result)

    result['status_code'] = 200
    result['message'] = 'successful'

    return jsonify(result)

if __name__ == "__main__":
    contacts = query_sql()

    app = socketio.Middleware(sio, app)

    eventlet.wsgi.server(eventlet.listen(('', 62010)), app)






