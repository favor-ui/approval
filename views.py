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




@app.route('/enrollees', methods=['GET'])
def get_enrollees():
    # try:
    mongo_data = mongo.db.enrollee
    output = []
    for q in mongo_data.find({}):
        output.append({"name":q["name"]})
    
    return jsonify({"result": output})
    # except Exception:
    #     return jsonify({"Message":"Something went wrong Please check"})

@app.route('/enrollee', methods=['GET'])
def get_one_enrollee():
    # try:
    mongo_data = mongo.db.enrollee
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



# @app.errorhandler(400)
# def bad_request__error(exception):
#     return jsonify(
#         {
#             "Message": "Sorry you entered wrong values kindly check and resend!"
#         },
#         {
#             "status":400
#         }
#     )


# @app.errorhandler(401)
# def internal_error(error):
#     return jsonify(
#         {
#             "Message": "Acess denied ! please register and login to generate API KEY"
#         },
#         {
#             "status": 401
#         }
#     )



# @app.errorhandler(404)
# def not_found_error(error):
#     return jsonify(
#         {
#             "Message":"Sorry the page your are looking for is not here kindly go back"
#         },
#         {
#             "status": 404
#         }
#     )





# @app.errorhandler(405)
# def methodNotallowes(error):
#     return jsonify(
#         {
#             "Message": "Sorry the requested method is not allowed kindly check and resend !"
#         },
#         {
#             "status": 405
#         }
#     )

# @app.errorhandler(500)
# def method_not_allowed(error):
#     return jsonify(
#         {
#             "Message": "Bad request please check your input and resend !"
#         },
#         {
#             "status": 500
#         }
#     )

# if __name__=='__main__':
#     app.run(debug=True)
