from flask import request, Blueprint, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST 
from src.modules.mongodb import mongo

profile =  Blueprint("profile",__name__,url_prefix="/api/v1/profile")


@profile.route("/",methods = ["POST", "GET"])
def users():
    # init methods
    message = ""
    data = {}
    status = False
    db = mongo.EcoTopia
    if request.method == "POST":
        address = request.json.get("Address","")

        if address == "":
            message = "empty address"
            return jsonify({"status":status,"message":message,"data":data}),HTTP_400_BAD_REQUEST

        user = db.users.find_one({"Address":address})

        data = {"Name":user["Name"],"Email":user["Email"],"Phone":user["Phone"],"Username":user["Username"], "Address":user["Address"], "_id":str(user["_id"]), "Cart":user["Cart"],"Balance":user["Balance"]}
        status = True
        # print(data)
    
    return jsonify({"status":status,"message":"","data":data}),HTTP_200_OK