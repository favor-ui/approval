from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo
import os, sys
from datetime import *
from dateutil.relativedelta import *
import calendar
import requests, json, uuid
from functools import wraps
import lgs
from config import Config



app = Flask(__name__)


app.config.from_object(Config)


mongo = PyMongo(app)


api = Api(app)




def cur_time_and_date():
    now = datetime.utcnow()
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    tm = now.strftime("%H:%M:%S")
    return (d2 +' '+'at'+' '+tm)

def sms(message, phone_number):
        headers = {
            'content-type': 'application/json',
            'Accept': 'application/json',
            'x-access-token': 'healthradar 1200980'
        }
        data = {
            'sender': 'InstantDeposit',
            'receiver': phone_number,
            'message': message
        }
        response = requests.post('https://isusubackend.herokuapp.com/api/client/sms', json=data, headers=headers)
        return response.json()

time = cur_time_and_date


@app.route('/')
def index():
    return jsonify ({"message":"test"})


@app.route('/db_backup', methods=['GET'])

def get_enrollsof():
    mongo_data = mongo.db.enrollments
    mongo_data_1 = mongo.db.Approved
    mongo_data_2 = mongo.db.Backup

    pipeline = [ {"$match": {}}, 
        {"$out": "Approved"},]
    
    mongo_data.aggregate(pipeline)
        
    # pipeline_ = [ {"$match": {}}, 
    #             {"$out": "Backup"},]
    # mongo_data.aggregate(pipeline_)

    # source = mongo_data

    # source.remove({})   
    
    return jsonify({"result": "success"})


class Get_all_of(Resource):

    # @require_appkey
    def get(self):
        mongo_data = mongo.db.enrollments
        
        mongo_data_1 = mongo.db.Approved
        
        output = []
        for q in mongo_data_1.find({}):
            output.append({
                            "Submission ID": q["Submission ID"],
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
                            "ID Card":q["ID Card"],
                            "Passport" : q["Passport"],
                            "Relationship" : q["Relationship"],
                            "Timestamp" : q["Timestamp"],
                            "Status" : q["Status"]
                        })
            # if q:
            #     return jsonify({"message":"All ready exist "})
            # else:
            #     mongo_data_1.insert(output)
        return jsonify({"result": output})


api.add_resource(Get_all_of, '/enrollsof')

class Get_all_count(Resource):
    
    # @require_appkey
    def get(self):
        
        mongo_data_1 = mongo.db.Approved
        
        output = mongo_data_1.count()

        return jsonify({"result": output})


api.add_resource(Get_all_count, '/_count')

class Get_one_of(Resource):
    
    # @require_appkey
    def get(self):
        mongo_data = mongo.db.enrollments
        mongo_data_1 = mongo.db.Approved
        request_data = request.get_json()
        phone_number = request_data["phone_number"]
        
        if not phone_number:
            return jsonify({"Error":"Field can not be blank", "status":0})
        
        q = mongo_data_1.find_one({"Phone Number":phone_number})

        if q:
            output = {
                            "Submission ID": q["Submission ID"],
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
                            "ID Card":q["ID Card"],
                            "Passport" : q["Passport"],
                            "Relationship" : q["Relationship"],
                            "Timestamp" : q["Timestamp"],
                            "Status" : q["Status"]}
        else:
            output = "No results"
        
        return jsonify({"result": output})

api.add_resource(Get_one_of, '/enrollof')



class Get_one_on(Resource):

    # @require_appkey
    def get(self):
        mongo_data = mongo.db.GS
        request_data = request.get_json()
        phone_number = request_data["phone_number"]
        if len(phone_number) != 11 or len(''.join(i for i in phone_number if i.isdigit())) != 11:
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


api.add_resource(Get_one_on, '/enrollon')


class Get_all_on(Resource):
    # @require_appkey
    def get(self):
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


api.add_resource(Get_all_on, '/enrollson')


class Approved(Resource):
      
    parser = reqparse.RequestParser()

    parser.add_argument('Submission ID',
                        type=str,
                        required=True,
                        help="Name field cannot be left blank")
    
    parser.add_argument('LGA',
                        type=str,
                        required=True,
                        help="LGA field cannot be left blank")
    
    parser.add_argument('Ward',
                        type=str,
                        required=True,
                        help="Ward field cannot be left blank")
    
    parser.add_argument('Gender',
                        type=str,
                        required=True,
                        help="Ward field cannot be left blank")

    parser.add_argument('Date of Birth',
                        default= date,
                        required=True,
                        help="Date of Birth field cannot be left blank")

    parser.add_argument('Occupation',
                        type=str,
                        required=True,
                        help= "Occupation field cannot be left blank")

    parser.add_argument('Phone Number',
                        type = str,
                        required=True,
                        help= "Phone Number field cannot be left blank")


    def put(self):
        
        mongo_data_1 = mongo.db.Approved

        
        data = Approved.parser.parse_args()

        dob = datetime.strptime(data['Date of Birth'], "%d/%m/%Y")

        sid = data["Submission ID"] 

        Lga = data["LGA"]

        Wod = data["Ward"]

        gen = data["Gender"]

        occ = data["Occupation"] 

        phone = data["Phone Number"] 

        if sid  == "":
            return {"message": "name field cannot be empty", "status": False}, 404
        
        elif Lga == "":
            return {"message": "LGA field cannot be empty", "status": False}, 404
        
        elif Wod == "":
            return {"message": "Ward field cannot be empty", "status": False}, 404

        elif gen == '':
            return {"message": "Gender field cannot be empty", "status": False}, 404

        elif dob == '':
            return {"message": "Date of birth field cannot be empty", "status": False}, 404

        elif occ == '':
            return {"message": "Occupation field cannot be empty", "status": False}, 404

        elif not phone:
            return jsonify({"Error":"Field can not be blank", "status":0})

        # update route
        
        q = mongo_data_1.find_one({"Submission ID": sid})
        
        if not q:
            return {"message": "Enrollee doesn't exit", "status": False}, 404
        
        else:
            data = Approved.parser.parse_args()

            sid = data["Submission ID"] 

            Lga = data["LGA"]

            Wod = data["Ward"]

            gen = data["Gender"]

            occ = data["Occupation"] 

            phone = data["Phone Number"] 
                
            Today = date.today()

            dob = datetime.strptime(data['Date of Birth'], "%d/%m/%Y")

            time_difference = relativedelta(Today, dob)
            
            diff = time_difference.years
            
            if diff <= 5:
                plan = "Equity"
            
            elif diff >= 60:
                plan = "Equity"
            
            elif occ == "Retired":
                plan = "Equity"
            
            else:
                plan = "Nill"

            
            p = str(uuid.uuid4().int)[:6]

            sex = {"Male": "1", "Female" : "2"}
            
            lga = Lga
            # .strip().lower().capitalize()

            gender = gen.strip().lower().capitalize()
            
            ward = data['Ward']
            # .strip().lower().capitalize()

            ward_no = lgs.LGAs[lga][ward]

            ID = p + ward_no + sex[gender]

            
            mongo_data_1.find_one_and_update({"Submission ID": sid}, {"$set": {"Status": "Approved", "ENIR ID": ID, "Plan" : plan}} )


            Suc_cess = "message :Congratulation:Congratulations, we were able to verify your information; Time: %s"%(time)
            
            enrollee_number = data["Phone Number"]

            # sms(message=Suc_cess, phone_number=enrollee_number)

            return {"message": "Your ID has been assigned successfully ", "status": True}, 200


api.add_resource(Approved, '/approve')

class Get_Approved_count(Resource):  
    # @require_appkey
    def get(self):
        # mongo_data= mongo.db.enrollments
        mongo_data_1= mongo.db.Approved
        # output = []
        
        output = mongo_data_1.count({"Status":"Approved"})

        return jsonify({"result": output})


api.add_resource(Get_Approved_count, '/count_Approved')


class Get_Approved(Resource):  
    # @require_appkey
    def get(self):

        mongo_data = mongo.db.Approved
        
        output = []
        
        
        for q in mongo_data.find({"Status":"Approved"}):
            
            output.append({
                            "Submission ID": q["Submission ID"],
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
                            "ID Card":q["ID Card"],
                            "Passport" : q["Passport"],
                            "Relationship" : q["Relationship"],
                            "Timestamp" : q["Timestamp"],
                            "Status" : q["Status"],
                            "ENIR ID" : q["ENIR ID"],
                            "Plan" : q["Plan"]
                            })

        return jsonify({"result": output})



api.add_resource(Get_Approved, '/get_approved')


class Not_Approved(Resource):
    
    # @require_appkey
    def put(self):
        
        mongo_data_1 = mongo.db.Approved
        
        parser = reqparse.RequestParser()

        parser.add_argument('Submission ID',
                            type=str,
                            required=True,
                            help= "Submission ID field cannot be left blank")


        parser.add_argument('Phone Number',
                            type = str,
                            required=True,
                            help= "Phone Number field cannot be left blank")
        
        data = parser.parse_args()

        
        if not data["Submission ID"]:
            return jsonify({"Error":"Field can not be blank", "status":0})
        
        if not data["Phone Number"]:
            return jsonify({"Error":"Field can not be blank", "status":0})

        q = mongo_data_1.find({"Submission ID": data["Submission ID"]})

        if data["Submission ID"]:
            mongo_data_1.update_many({"Submission ID":data["Submission ID"]},{"$set": {"Status": "Not_Approved"}})

            # Failure = "message :Sorry, we couldn't verify your data; Time: %s" %(time)

            # enrollee_phone = data["Phone Number"]

            # sms(message= Failure, phone_number=enrollee_phone)

            return {"message": "Not Approved", "status": True}, 200


        else:
            return 'not_found'


api.add_resource(Not_Approved,'/not_approved')


class Get_notApproved_count(Resource):  
    # @require_appkey
    def get(self):
        mongo_data_1 = mongo.db.Approved
        
        output = mongo_data_1.count({"Status":"Not_Approved"})

        return jsonify({"result": output})


api.add_resource(Get_notApproved_count, '/count_notApproved')

class Get_notApproved(Resource):  
    # @require_appkey
    def get(self):
        mongo_data_1 = mongo.db.Approved
        
        output = []
        
        
        for q in mongo_data_1.find({"Status":"Not_Approved"}) :
            
            output.append({
                            "Submission ID": q["Submission ID"],
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
                            "ID Card":q["ID Card"],
                            "Passport" : q["Passport"],
                            "Relationship" : q["Relationship"],
                            "Timestamp" : q["Timestamp"],
                            "Status" : q["Status"]
                         })
                        

        return jsonify({"result": output})



api.add_resource(Get_notApproved, '/get_not_Approved')

class Get_pending(Resource):  
    # @require_appkey
    def get(self):
        mongo_data_1 = mongo.db.Approved
        
        output = []
        
        
        for q in mongo_data_1.find({"Status":"Pending"}) :
            
            output.append({
                            "Submission ID": q["Submission ID"],
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
                            "ID Card":q["ID Card"],
                            "Passport" : q["Passport"],
                            "Relationship" : q["Relationship"],
                            "Timestamp" : q["Timestamp"],
                            "Status" : q["Status"]
                         })
                        

        return jsonify({"result": output})



api.add_resource(Get_pending, '/get_pending')

class Get_pending_count(Resource):  
    # @require_appkey
    def get(self):
        mongo_data_1 = mongo.db.Approved
        
        output = mongo_data_1.count({"Status":"Pending"})

        return jsonify({"result": output})


api.add_resource(Get_pending_count, '/count_pending')




@app.route('/updatemany', methods = ['PUT'])

def updatemany():
    mongo_data_1 = mongo.db.Approved
    
    for i in mongo_data_1.find():

        mongo_data_1.update_many({}, 
        {"$set":{"Status" : "Pending"}})
    return jsonify({"msg":"Success", "status": 200})



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
def internal_server_error(error):
    return jsonify(
        {
            "Message": "Bad request please check your input and resend !"
        },
        {
            "status": 500
        }
    )


@app.errorhandler(501)
def server_not_found_error(error):
    return jsonify(
        {
            "Message": "inter server error"
        },
        {
            "status": 501
        }
    )
