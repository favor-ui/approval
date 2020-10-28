from flask import Flask, jsonify, request, abort
from app import init, isid
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
    mongo_data_1 = mongo.db.approved
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
        # if q:
        #     return jsonify({"message":"All ready exist "})
        # else:
        #     mongo_data_1.insert(output)
    return jsonify({"result": output})
    # except Exception:
    #     return jsonify({"Message":"Something went wrong Please check"})

@app.route('/enrollon', methods=['GET'])
def get_one_enrollon():
    # try:
    mongo_data = mongo.db.GS
    request_data = request.get_json()
    phone_number = request_data["phone_number"]
    if len(data["phone_number"]) != 11 or len(''.join(i for i in data["phone_number"] if i.isdigit())) != 11:
            return {"status": False, "error": "Phone number must be 11 digits"}, 404
    
    if not phone_number:
        return jsonify({"Error":"Field can not be blank", "status":0})
    
    q = mongo_data.find_one({"phone_number":phone_number})

    if q:
        output = {"name": q["name"],
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
                        "nok_contact" : q["nok_contact"]}
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
    Phone Number = request_data["Phone Number"]
    if len(data["Phone Number"]) != 11 or len(''.join(i for i in data["Phone Number"] if i.isdigit())) != 11:
            return {"status": False, "error": "Phone number must be 11 digits"}, 404
    
    if not Phone_Number:
        return jsonify({"Error":"Field can not be blank", "status":0})
    
    q = mongo_data.find_one({"Phone Number":Phone_Number})

    if q:
        output = {  # "_id" : q["_id"],
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
                    "Status" : q["Status"]}
    else:
        output = "No results"
    
    return jsonify({"result": output})
    # except Exception:
    #     abort(500)


# @app.route('/approvedon', methods=['PUT'])
# def approvedon():
#     # try:
#     mongo_data = mongo.db.GS
#     request_data = request.get_json()
#     name1 = request_data['name']
#     name2 = "_".join(name1.split())
#     name = name2.lower()
    
#     if not name:
#         return jsonify({"Error":"Field can not be blank", "status":0})
    
#     q = mongo_data.find_one({"name":name})

#     if q:
#         output = {"name":q["name"]}
#     else:
#         output = "No results"
    
#     return jsonify({"result": output})
#     # except Exception:
#     #     abort(500)



#     app.route('/approvedof', methods=['PUT'])
# def approvedof():
#     # try:
#     mongo_data = mongo.db.enrollments
#     request_data = request.get_json()
#     name1 = request_data['name']
#     name2 = "_".join(name1.split())
#     name = name2.lower()
    
#     if not name:
#         return jsonify({"Error":"Field can not be blank", "status":0})
    
#     q = mongo_data.find_one({"Name":name})

#     if q:
#         output = {"Name":q["name"]}
#     else:
#         output = "No results"
    
#     return jsonify({"result": output})
#     # except Exception:
#     #     abort(500)


# app.route('/notApprovedon', methods=['PUT'])
# def notApprovedon():
#     # try:
#     mongo_data = mongo.db.enrollments
#     request_data = request.get_json()
#     name1 = request_data['name']
#     name2 = "_".join(name1.split())
#     name = name2.lower()
    
#     if not name:
#         return jsonify({"Error":"Field can not be blank", "status":0})
    
#     q = mongo_data.find_one({"Name":name})

#     if q:
#         output = {"Name":q["name"]}
#     else:
#         output = "No results"
    
#     return jsonify({"result": output})
#     # except Exception:
#     #     abort(500)


# app.route('/notApprovedof', methods=['PUT'])
# def notApprovedof():
#     # try:
#     mongo_data = mongo.db.enrollments
#     request_data = request.get_json()
#     name1 = request_data['name']
#     name2 = "_".join(name1.split())
#     name = name2.lower()
    
#     if not name:
#         return jsonify({"Error":"Field can not be blank", "status":0})
    
#     q = mongo_data.find_one({"Name":name})

#     if q:
#         output = {"Name":q["name"]}
#     else:
#         output = "No results"
    
#     return jsonify({"result": output})
#     # except Exception:
#     #     abort(500)

    
    
@app.errorhandler(400)
def bad_request__error(exception):
    return jsonify(
        {
            "Message": "Sorry you entered wrong values kindly check and resend!"
        },
        {
            "status": 400
        }
    )


@app.errorhandler(401)
def internal_error(error):
    return jsonify(
        {
            "Message": "Access denied ! please register and login to generate API KEY"
        },
        {
            "status": 401
        }
    )


@app.errorhandler(404)
def not_found_error(error):
    return jsonify(
        {
            "Message": "Sorry the page your are looking for is not here kindly go back"
        },
        {
            "status": 404
        }
    )


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(
        {
            "Message": "Sorry the requested method is not allowed kindly check and resend !"
        },
        {
            "status": 405
        }
    )


@app.errorhandler(500)
def method_not_allowed(error):
    return jsonify(
        {
            "Message": "Bad request please check your input and resend !"
        },
        {
            "status": 500
        }
    )
