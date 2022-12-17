from flask import Blueprint, request, jsonify, redirect, url_for
from src.constants.http_status_code import HTTP_400_BAD_REQUEST
from src.modules.mongodb import mongo
from datetime import datetime
from bson import ObjectId

cart = Blueprint("cart",__name__,url_prefix="/api/v1/cart")



@cart.route("/add/", methods = ["POST"])
def add_cart():
    # init db
    db = mongo.EcoTopia

    # initialize return data
    data = {}
    status = False
    message = ""

    if request.method == "POST":
        # get post data from json
        user_address = request.json.get("UserAddress","")
        quantity = request.json.get("Quantity",0)
        itemid = request.json.get("Item_id","")

        # check if address exit
        chk_user = db.users.find_one({"Address":user_address})
        # print(chk_user)
        
        if chk_user is None:
            message = "invalid address... check address"
            return jsonify({"status":status, "message":message, "data":data}), HTTP_400_BAD_REQUEST

        # chck if item already in cart
        # 1) fetcch all items
        # 2) search in cart for item id

        # get user cart
        cartlist = chk_user["Cart"]

        # check if cart is empty

        if len(cartlist) > 0:
            # check if item already in cart
            for item in cartlist:

                # if id already in cart
                if item["Item"] == itemid:
                    item["Qantity"] = item["Qantity"] + quantity
                    break

                 # update the new cart
            
            else:
                # append the new item to the cart
                cartlist.append({"Item":itemid,"Qantity":quantity})      
        else:
            # append the new item to the cart
            cartlist.append({"Item":itemid,"Qantity":quantity})
                    
        # upload change 
        try:
           

            # update users db cart
            db.users.update_one({"Address":user_address}, {"$set":{"Cart":cartlist}})

            # refresh users 
            user = db.users.find_one({"Address":user_address})

            data = {"Address": user["Address"],"Cart":user["Cart"],"Name":user["Name"],"Email":user["Email"],"Phone":user["Phone"],"Username":user["Username"]}
            status = True 

            # return users data here


        except:
            # incorrect method
            message = "an error was encountered and process terminated"



    else:
        message = "The method is not allowed for the requested URL."



    

    return jsonify({"status":status,"message":message,"data":data})






@cart.route("/checkout/", methods = ["POST"])
def checkout():
    db = mongo.EcoTopia

    # initialize return data
    data = {}
    status = False
    message = ""
    price = 0


    if request.method == "POST":
        # get post data from json
        user_address = request.json.get("Address","")
        user_address = user_address.strip()

        # check if user exit
        user_data = db.users.find_one({"Address":user_address})

        if user_data is None:
            message = "invalid address... check address"
            return jsonify({"status":status, "message":message, "data":data}), HTTP_400_BAD_REQUEST

        # create empty list for the items
        items = []

        for item in user_data["Cart"]:
            itemid = ObjectId(item["Item"])
            store_item = db.store.find_one({"_id":itemid})

            # add prices 
            price += store_item["Price"] * item["Qantity"]

            # get all item data and store in a dictionay 
            itemdata = {"Id": str(store_item["_id"]), "Description":store_item["Description"], "Category":store_item["Category"], "Price":store_item["Price"] * item["Qantity"], "Title":store_item["Title"], "Quantity": item["Qantity"], "ImgUrl":store_item["ImgUrl"],"Created_at":store_item["Created_at"]}
            items.append(itemdata)

        data = items
        # print(data)
        status =  True
        
        # deducte the money and clear user's cart
        

    else:
        message = "methode not allowed, check documentation"


    return jsonify({"status":status,"price":price,"message":message,"data":data})






@cart.route("/payment/", methods = ["POST"])
def payment():
    # db instance
    db = mongo.EcoTopia

    # initialize return data
    data = {}
    status = False
    message = ""
    price = 0

    if request.method == "POST":
        # get post data from json
        user_address = request.json.get("Address","")
        token = request.json.get("Token","")
        user_address = user_address.strip()

        # print(token)


        # check if it's a duplicate transaction
        chk_transaction = db.transactions.find_one({"Token":token})
        if chk_transaction is not None:
            message = "Duplicate transation"
            return jsonify({"status":status, "message":message, "data":data}), HTTP_400_BAD_REQUEST

        # check if user exit
        user_data = db.users.find_one({"Address":user_address})
        if user_data is None:
            message = "invalid address... check address"
            return jsonify({"status":status, "message":message, "data":data}), HTTP_400_BAD_REQUEST

        # gat all cart items 
        for item in user_data["Cart"]:
            itemid = ObjectId(item["Item"])
            store_item = db.store.find_one({"_id":itemid})

            # add prices 
            price += store_item["Price"] * item["Qantity"]


        # check if user have enough money
        balace = user_data["Balance"]

        if balace < price:
            message = "insufficient balance"
            return jsonify({"status":status,"message":message,"data":data})
        
        # subtract price to get new balance
        newbalance = balace - price

        # update users data
        # and transactions 





# update product quantity





        try:
            # update new balance and empty cart
            db.users.update_one({"Address":user_address}, {"$set":{"Balance":newbalance}})
            db.users.update_one({"Address":user_address}, {"$set":{"Cart":[]}})

            # add transaction to users transaction
            newtransacton = db.transactions.insert_one({"sender":user_address,"To":"Store","Amount":price,"Token":token,"created_at":datetime.now()})

            # get user transactions
            transactions = user_data["Transactions"]
            # add transaction to transactions list
            transactions.append(newtransacton.inserted_id)
            
            # update transactions
    # ===========================================
            db.users.update_one({"Address":user_address},{"$set":{"Transactions":transactions},})

            status = True
            data = {"Amout":price,"To":user_address,"Sender":"Store","Transaction-id":str(newtransacton.inserted_id)}

        except:
            message = "an error was encountered, please try again"


    return jsonify({"status":status,"price":price,"message":message,"data":data})





@cart.route("/delete/", methods = ["POST"])
def delete_cart():
     # db instance
    db = mongo.EcoTopia

    # initialize return data
    data = {}
    status = False
    message = ""

    if request.method == "POST":
        # get post data from json
        user_address = request.json.get("Address","")
        itemid = request.json.get("Item_id","")

        user_address = user_address.strip()
        itemid = itemid.strip()


        # check if item id id empty
        if itemid == "":
            message = "empty item-id"
            return jsonify({"status":status, "message":message, "data":data}), HTTP_400_BAD_REQUEST
    

        # check if user exit
        user_data = db.users.find_one({"Address":user_address})
        if user_data is None:
            message = "invalid address... check address"
            return jsonify({"status":status, "message":message, "data":data}), HTTP_400_BAD_REQUEST


        # get all cart items 
        cartlist = user_data["Cart"]

        # iterate throught the items
        for item in cartlist:
            # get the item to be deleted
            if item["Item"] == itemid:
                # remove it from the cart
                cartlist.remove(item)
                break
        try:
            # update new balance and empty cart
            db.users.update_one({"Address":user_address}, {"$set":{"Cart":cartlist}})

# to be looked into 


            # return redirect(url_for(checkout("Address"=user_address)))

            # print(usercart["Cart"])

            status = True

        except:
            message = "an error was encountered, please reload" 


        # print(cartlist)


    return jsonify({"status":status,"message":message,"data":data})
