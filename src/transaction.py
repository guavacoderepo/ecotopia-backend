from flask import jsonify, request, Blueprint
from src.modules.mongodb import mongo
from datetime import datetime

transaction = Blueprint("transactions", __name__, url_prefix="/api/v1/transactions")




# fundind a wallet
@transaction.route("send/coin", methods=["POST","GET"])
def send_coin():

    # init db 
    db = mongo.EcoTopia

    # initialize return data
    data = {}
    status = False
    message = ""

    if request.method == "POST":
        # get json post data
        sender = request.json.get("Sender","")
        to = request.json.get("To","")
        amount = request.json.get("Amount","")
        token = request.json.get("Token","")
        created_at = datetime.now()

        # strip white spaces
        sender = sender.strip()
        to = to.strip()
        token = token.strip()

        
        # check if a duplicate transaction
        chk_transaction = db.transactions.find_one({"Token":token})
        if chk_transaction is not None:
            message = "Duplicate transation"
            return jsonify({"status":status, "message":message, "data":data})
        
        # check if username exit 
        validate_user = db.users.find_one({"Username":to})
        if validate_user is None:
            message = "check username.... incorrect username"
            return jsonify({"status":status, "message":message, "data":data})


        # check senders balance 
# ===================================================

        # sender_wallet = db.users.find_one({"Address":sender})
        # if sender_wallet["Amount"] < amount:
        #     message = "insufficent funds"
        #     return jsonify({"status":status, "message":message, "data":data})
        
# ===================================================

        # deduct coin fron sender 
        # sender_wallet["Amount"] - amount


        # add to receiver wallet
        try:
            # get wallet 
            to_wallet = db.users.find_one({"Address":to})
            # add coin to the wallet balance
            newbal = to_wallet["Balance"]+amount
            # create a transaction
            newtransacton = db.transactions.insert_one({"sender":sender,"To":to,"Amount":amount,"Token":token,"created_at":created_at})

            # get user transactions
            transactions = to_wallet["Transactions"]
            # add transaction to transactions list
            transactions.append(newtransacton.inserted_id)
            
            # update new balance
    # ===========================================
            db.users.update_one({"Address":to},{"$set":{"Balance":newbal}})
            db.users.update_one({"Address":to},{"$set":{"Transactions":transactions},})
    # ===========================================
            data = {"Amout":amount,"To":to,"Sender":sender,"Transaction-id":str(newtransacton.inserted_id)}
            status = True
        # catch exception
        except:
            message = "an error was encountered and process terminated"

    # check if request is a get
    else:
        message = "The method is not allowed for the requested URL."


    return jsonify({"status":status,"message":message,"data":data})



# @transaction.route("wallet/validate:<username>", methods=["GET"])
# def wallet_validate(username):

#     if request.method == "GET":
#         dd
#     else:
#         message = "The method is not allowed for the requested URL."
