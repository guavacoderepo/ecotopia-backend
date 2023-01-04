from flask import Flask, Blueprint, request, jsonify
from src.modules.mongodb import mongo
from datetime import datetime


payment = Blueprint("payment", __name__, url_prefix="/api/v1/payment")

@payment.route("/checkout/", methods = ["POST", "GET"])
def checkout():
     # init db 
    db = mongo.EcoTopia

    # initialize return data
    data = {}
    status = False
    message = "" 

    # check post request
    if request.method == "POST":
        bank = request.json.get("Bank", "")
        amount = request.json.get("Amount", 0)
        name = request.json.get("Name", "")
        token = request.json.get("Token", "")
        address = request.json.get("Address", "")


         # check if token already exit
        duplicate = db.transactions.find_one({"Token":token})
        if duplicate is not  None:
            message = "duplicate transaction"
            return jsonify({"status":status,"message":message,"data":data})

        # check bank length
        if bank == "":
            message = "empty bank selected"
            return jsonify({"status":status,"message":message,"data":data})

        # check name
        if name == "":
            message = "empty name field"
            return jsonify({"status":status,"message":message,"data":data})

        # check address
        if address == "":
            message = "empty address"
            return jsonify({"status":status,"message":message,"data":data})

        # check if address exit
        user = db.users.find_one({"Address":address})
        if user is None:
            message = "invalid address"
            return jsonify({"status":status,"message":message,"data":data})
        
        balance = user["Balance"]

        # check if amount avaible 
        if amount > balance:
            message = "insuffient balance"
            return jsonify({"status":status,"message":message,"data":data})

        try:
              
            # minus the money from the wallet 
            newBalance = balance - amount
            
            # update balance in users
            db.users.update_one({"Address": address}, {"$set": {"Balance": newBalance }})
            # add to transactions
            newtransacton = db.transactions.insert_one({"sender":user["Address"],"To":bank,"Amount":amount,"Token":token,"created_at":datetime.now()})
            
            # get user transactions
            transactions = user["Transactions"]

            # add transaction to transactions list
            transactions.append(newtransacton.inserted_id)
            
            # update transactons
            db.users.update_one({"Address":address},{"$set":{"Transactions":transactions},})
            
            # set returen param
            data = {"Amout":amount,"To":bank,"Sender":user["Address"],"Transaction-id":str(newtransacton.inserted_id)}
            status = True
        except:
            message = "an error occured.... please try again"
       


    # check if request is a get
    else:
        message = "This method is not allowed for the requested URL."


    return jsonify({"status":status,"message":message,"data":data})
