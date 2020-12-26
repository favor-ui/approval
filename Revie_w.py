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
import pandas as pd


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

# Base URL
@app.route('/')
def index():
    return {"message":"test"}



# Routh for backup
@app.route('/db_backup', methods=['GET'])

def backup():
    # mongo_data = mongo.db.enrollments
    # mongo_data_1 = mongo.db.Approved
    # mongo_data_2 = mongo.db.Backup

    # pipeline = [ {"$match": {}}, 
    #     {"$out": "Not_Approved"},]
    
    # mongo_data_2.aggregate(pipeline)
        
    # pipeline_ = [ {"$match": {}}, 
    #             {"$out": "Backup"},]
    # mongo_data.aggregate(pipeline_)

    # source = mongo_data

    # source.remove({})   
    
    return {"result": "success"}

class Get_all_of(Resource):

    # @require_appkey
    def get(self):
        
        mongo_data_1 = mongo.db.Not_Approved
        
        output = []
        for q in mongo_data_1.find({}):
            
            q["_id"] = str(q["_id"])


            output.append(q)

        return {"result": output}


api.add_resource(Get_all_of, '/all/enrollments')

class Get_all_count(Resource):
    
    # @require_appkey
    def get(self):
        
        mongo_data_1 = mongo.db.Not_Approved
        
        output = mongo_data_1.count()

        return {"result": output}


api.add_resource(Get_all_count, '/all/count')

class Get_one_of(Resource):
    
    # @require_appkey
    def get(self):

        mongo_data_1 = mongo.db.Not_Approved
        request_data = request.get_json()
        phone_number = request_data["phone_number"]
        
        if not phone_number:
            return jsonify({"Error":"Field can not be blank", "status":0})
        
        q = mongo_data_1.find_one({"Phone Number":phone_number})

        output = []

        if q:
            q["_id"] = str(q["_id"])
            
            output.append(q)
        else:
            output = "No results"
        
        return {"result": output}

api.add_resource(Get_one_of, '/one/enrollee')



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
        
        mongo_data = mongo.db.Approved

        mongo_data_1 = mongo.db.Not_Approved
       
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

            
            result = mongo_data_1.find_one_and_update({"Submission ID": sid, "Date of Birth" : data["Date of Birth"] }, {"$set": {"Status" : "Approved", "Plan": plan, "ENRID": ID , "Print Status" : "Nill"}})
            print(result)
            result["_id"] = str(result["_id"])
                
            mongo_data.insert(result)


            # Suc_cess = "message :Congratulation, we were able to verify your information; Time: %s"%(time)
            
            # enrollee_number = data["Phone Number"]

            # sms(message=Suc_cess, phone_number=enrollee_number)

            return {"message": "Your ID has been assigned successfully ", "status": True}, 200


api.add_resource(Approved, '/approval/enrollment/id')


class Approve_many(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("Submission ID", type=str, required=True, help="this field cannot be left blank")
    parser.add_argument("LGA", type=str, required=True, help="this field cannot be left blank")
    parser.add_argument("Ward", type=str, required=True, help="this field cannot be left blank")
    parser.add_argument("Gender", type=str, required=True, help="this field cannot be left blank")
    parser.add_argument("Occupation", type=str, required=True, help="this field cannot be left blank")
    parser.add_argument("Phone Number", type=str, required=True, help="this field cannot be left blank")
    parser.add_argument("Date of Birth", type=str, required=True, help="this field cannot be left blank")
    
    def put(self):
        
        mongo_data = mongo.db.Approved

        mongo_data_1 = mongo.db.Not_Approved


        data = Approve_many.parser.parse_args()

        Sid = data["Submission ID"].split(",")
        
        Lga = data["LGA"].split(",")
        
        Wod = data["Ward"].split(",")
        
        Gen = data["Gender"].split(",")
        
        occ = data["Occupation"].split(",")

        phon = data["Phone Number"].split(",")

        DOB = data["Date of Birth"].split(",")
        

       

    # convert data to a dateframe and back to dictionary
        df = pd.DataFrame({"Submission ID":Sid, "LGA" : Lga, "Ward" : Wod, "Gender" : Gen, "Occupation": occ, "Phone Number" : phon, "Date of Birth" : DOB})
        
        all_records = df.to_dict("records")
        
        # print(all_records)
        see = {}
        for x in range(len(all_records)):

            sid = all_records[x]["Submission ID"].strip()

            Occ = all_records[x]["Occupation"].strip()

            Dob = all_records[x]["Date of Birth"].strip()
            
            # DOB = 

            dob = datetime.strptime(Dob.strip(), "%d/%m/%Y")

            Today = date.today()

            time_difference = relativedelta(Today, dob)
            
            diff = time_difference.years


            if diff <= 5:
                plan = "Equity"
            
            elif diff >= 60:
                plan = "Equity"
            
            elif Occ == "Retired":
                plan = "Equity"
            
            else:
                plan = "Nill"


            p = str(uuid.uuid4().int)[:6]

            sex = {"Male": "1", "Female" : "2"}
            
            lga = all_records[x]["LGA"].strip()

            gender = all_records[x]["Gender"].strip()
            
            ward = all_records[x]["Ward"].strip()

            ward_no = lgs.LGAs[lga][ward]

            ID = p + ward_no + sex[gender]


            result = mongo_data_1.find_one_and_update({"Submission ID": sid }, {"$set": {"Status" : "Approved", "Plan": plan, "ENRID": ID , "Print Status" : "Null"}})

            result["_id"] = str(result["_id"])
                
            mongo_data.insert(result)

            Suc_cess = "message :Congratulation:Congratulations, we were able to verify your information; Time: %s"%(time)
            
            enrollee_number = data["Phone Number"]

            # sms(message=Suc_cess, phone_number=enrollee_number)

            return {"message": "Your ID has been assigned successfully ", "status": True}, 200
        

api.add_resource(Approve_many, '/approve/enrollments')




class Get_Approved_count(Resource):  
    # @require_appkey
    def get(self):

        mongo_data_1= mongo.db.Approved
        
        output = mongo_data_1.count({"Status":"Approved"})

        return {"result": output}


api.add_resource(Get_Approved_count, '/count_Approved')


class Get_unprinted(Resource):  
    # @require_appkey
    def get(self):

        mongo_data = mongo.db.Approved

        parser = reqparse.RequestParser(bundle_errors= True)

        parser.add_argument("limit", type=int)

        parser.add_argument("skip", type=int)

        data = parser.parse_args()
        
        records = mongo_data.find({"Status" : "Approved"}).limit(data["limit"]).skip(data["skip"])

        output = []
        
        for record in records:

            record["_id"] = str(record["_id"])

            output.append(record)

        if len(output) != 0:
            return jsonify(status = True, data =output)
        else:
             return jsonify(status = False, message = "No records found")

api.add_resource(Get_unprinted, '/all/unprinted')



class Printed(Resource):
    
    # @require_appkey
    def put(self):
        
        mongo_data = mongo.db.Approved
        
        parser = reqparse.RequestParser()

        parser.add_argument("ENRID",
                            type=str,
                            required=True,
                            help= "This field cannot be left blank")

        data = parser.parse_args()

        
        if not data["ENRID"]:
            
            return {"Error":"Field can not be blank", "status":0}
       
        records = mongo_data_1.find({"ENRID": data["ENRID"]})
        
        for record in records:
            
            if record["Print Status"]["status"] == "Printed":

                return {"message" : "Card Already Printed", "status" : 0}

            else:
                mongo_data.update_one({"Submission ID": data["Submission ID"]},{"$set": {"Print Status": {"status" : "Printed", "Frequency" : 1}}})

                # Failure = "message :Sorry, we couldn't verify your data; Time: %s" %(time)

                # enrollee_phone = data["Phone Number"]

                # sms(message= Failure, phone_number=enrollee_phone)
                # return see
                return {"message": "Card Printed", "status": True}, 200

api.add_resource(Printed,'/print/one')



class Reprint(Resource):
    
    # @require_appkey
    def put(self):
        
        mongo_data = mongo.db.Approved
        
        parser = reqparse.RequestParser()

        parser.add_argument("ENRID",
                            type=str,
                            required=True,
                            help= "Submission ID field cannot be left blank")

        data = parser.parse_args()

        
        if not data["ENRID"]:
            
            return {"Error":"Field can not be blank", "status":0}
       
        records = mongo_data_1.find({"ENRID": data["ENRID"]})
        
        for record in records:

            mongo_data_1.update_one({"ENRID": data["ENRID"]},{"$inc": { "Printed Status.Frequency": 1 }})

            # Failure = "message :Sorry, we couldn't verify your data; Time: %s" %(time)

            # enrollee_phone = data["Phone Number"]

            # sms(message= Failure, phone_number=enrollee_phone)

            return {"message": "Card Printed", "status": True}, 200

        else:
            return 'not_found'

api.add_resource(Reprint,'/reprint/one')


class Print_range(Resource):
    
    parser = reqparse.RequestParser(bundle_errors=True)
    
    parser.add_argument("ENRID", action = 'append', required=True, help="this field cannot be left blank")
       
    def put(self):

        mongo_data = mongo.db.Approved


        data = Approve_many.parser.parse_args()

        enrid = data["ENRID"]

    # convert data to a dateframe and back to dictionary
        df = pd.DataFrame({"Submission ID":enrid})
        
        all_records = df.to_dict("records")
        
        # print(all_records)
        see = {}
        for x in range(len(all_records)):

            Enrid = all_records[x]["ENRID"].strip() 

            see[x] = [{"ENRID": Enrid}, {"$set": {"Print Status": {"status" : "Printed", "Frequency" : 1}}}]
            
            mongo_data_1.update_many({"ENRID": Enrid}, {"$set": {"Print Status": {"status" : "Printed", "Frequency" : 1}}})
        
        return see

api.add_resource(Print_range, '/print/range')


class Get_printed(Resource):  
    # @require_appkey
    def get(self):
        mongo_data = mongo.db.Approved
        
        output = []
        
        
        records = mongo_data.find({"Print Status.status":"Printed"})

        for record in records:
                
            q["_id"] = str(q["_id"])

            output.append(q)

            return {"result": output}


api.add_resource(Get_printed, '/all/printed')



class Query(Resource):
    
    # @require_appkey
    def put(self):
        
        mongo_data_1 = mongo.db.Not_Approved
        
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

        if not q:

            return "not_found"

        else:
            mongo_data_1.update_many({"Submission ID":data["Submission ID"]},{"$set": {"Status": "Not_Approved"}})

            # Failure = "message :Sorry, we couldn't verify your data; Time: %s" %(time)

            # enrollee_phone = data["Phone Number"]

            # sms(message= Failure, phone_number=enrollee_phone)

            return {"message": "Not Approved", "status": True}, 200   

api.add_resource(Query,'/query')



class Query_all(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("Submission ID", type=str, required=True, help="this field cannot be left blank")
    parser.add_argument("Phone Number", type=str, required=True, help="this field cannot be left blank")
       
    def put(self):

        mongo_data_1 = mongo.db.Not_Approved


        data = Approve_many.parser.parse_args()

        Sid = data["Submission ID"].split(",")

        phon = data["Phone Number"].split(",")
        

       

    # convert data to a dateframe and back to dictionary
        df = pd.DataFrame({"Submission ID":Sid, "Phone Number" : phon})
        
        all_records = df.to_dict("records")
        
        # print(all_records)
        see = {}
        for x in range(len(all_records)):

            sid = all_records[x]["Submission ID"].strip()

            phone = all_records[x]["Phone"].strip()

            

            see[x] = [{"Submission ID": sid}, {"$set": {"Status" : "Not_Approved" }}]
            mongo_data_1.update_many({"Submission ID": sid }, {"$set": {"Status" : "Not_Approve"}})
        
        return see    

api.add_resource(Query_all, '/query_all')


class Get_notApproved_count(Resource):  
    # @require_appkey
    def get(self):
        mongo_data_1 = mongo.db.Approved
        
        output = mongo_data_1.count({"Status":"Not_Approved"})

        return {"result": output}


api.add_resource(Get_notApproved_count, '/count_notApproved')

class Get_notApproved(Resource):  
    # @require_appkey
    def get(self):
        mongo_data_1 = mongo.db.Not_Approved
        
        output = []
        
        
        for q in mongo_data_1.find({"Status":"Not_Approved"}):

            q["_id"] = str(q["_id"])   

            output.append(q)            

        return {"result": output}

api.add_resource(Get_notApproved, '/all/query/enrollments')



class Get_pending(Resource):  
    # @require_appkey
    def get(self):
        mongo_data_1 = mongo.db.Not_Approved
        
        output = []
        
        
        for q in mongo_data_1.find({"Status":"Pending"}) :
            
            q["_id"] = str(q["_id"])
            
            output.append(q)

        return {"result": output}



api.add_resource(Get_pending, '/get_pending')

class Get_pending_count(Resource):  
    # @require_appkey
    def get(self):
        mongo_data_1 = mongo.db.Not_Approved
        
        output = mongo_data_1.count({"Status":"Pending"})

        return {"result": output}


api.add_resource(Get_pending_count, '/count_pending')


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
