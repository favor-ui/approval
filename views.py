from flask import Flask, jsonify, request, abort
from app import init, isid, error
from flask_pymongo import PyMongo
from config import Config
from functools import wraps

app = Flask(__name__)


app.config.from_object(Config)

mongo = PyMongo(app)


@app.route('/')
def index():
    return jsonify ({"message":"test"})




@app.route('/enrollson', methods=['GET'])
def get_enrollson():
    # try:
    mongo_data = mongo.db.GS
    output = []
    for q in mongo_data.find({}):
        output.append({"name": q["name"],
                        "gender" : q["gender"],
                        "lga" : q["lga"],
                        "phone_number" : q["phone_number"],
                        "genotype" : q["genotype"],
                        "blood_group" : q["blood_group"],
                        "ward" : q["ward"],
                        "id" : q["id"],
                        "dob" : q["dob"],
                        "occupation" : q["occupation"],
                        "next_of_kin" : q["next_of_kin"],
                        "nok_contact" : q["nok_contact"]
                    })
    
    return jsonify({"result": output})
    # except Exception:
    #     return jsonify({"Message":"Something went wrong Please check"})




@app.route('/enrollsof', methods=['GET'])
def get_enrollsof():
    # try:
    mongo_data = mongo.db.enrollments
    output = []
    for q in mongo_data.find({}):
        output.append({
                        # "_id" : q["_id"],
                        # "Submission ID": q["Submission ID"],
                        "Name" : q["Name"],
                        "Gender": q["Gender"],
                        "Marital Status" : q["Marital Status"],
                        "Date of Birth" : q["Date of Birth"],
                        "Phone Number" : q["Phone Number"],
                        "Email" : q["Email"],
                        "Nationality" : q["Nationality"],
                        "Occupation" : q["Occupation"],
                        "Blood Group" : q["Blood Group"],
                        "Genotype" : q["Genotype"],
                        "LGA" : q["LGA"],
                        "Ward" : q["Ward"],
                        "Next of Kin" : q["Next of Kin"],
                        "Next of kin Contact" : q["Next of kin Contact"],
                        "ID Types" : q["ID Types"],
                        # "ID Card":q["ID Card"],
                        # "Passport" : q["Passport"],
                        "Relationship" : q["Relationship"],
                        # "Timestamp" : q["Timestamp"],
                        "Status" : q["Status"]
                    })
    
    return jsonify({"result": output})
    # except Exception:
    #     return jsonify({"Message":"Something went wrong Please check"})

@app.route('/enrollon', methods=['GET'])
def get_one_enrollon():
    # try:
    mongo_data = mongo.db.GS
    request_data = request.get_json()
    name1 = request_data['name']
    name2 = "_".join(name1.split())
    name = name2.lower()
    
    if not name:
        return jsonify({"Error":"Field can not be blank", "status":0})
    
    q = mongo_data.find_one({"Name":name})

    if q:
        output = {"Enrollee":q["name"]}
    else:
        output = "No results"
    
    return jsonify({"result": output})
    # except Exception:
    #     abort(500)

@app.route('/enrollof', methods=['GET'])
def get_one_enrollof():
    # try:
    mongo_data = mongo.db.enrollments
    request_data = request.get_json()
    name1 = request_data['name']
    name2 = "_".join(name1.split())
    name = name2.lower()
    
    if not name:
        return jsonify({"Error":"Field can not be blank", "status":0})
    
    q = mongo_data.find_one({"Name":name})

    if q:
        output = {"Enrollee":q["name"]}
    else:
        output = "No results"
    
    return jsonify({"result": output})
    # except Exception:
    #     abort(500)
