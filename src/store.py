from flask import Blueprint, jsonify, request
from datetime import datetime
from src.modules.mongodb import mongo


store =  Blueprint("store", __name__, url_prefix="/api/v1/store")


@store.route("/products/", methods =["POST","GET"])
def products():

    # init db 
    db = mongo.EcoTopia

    # initialize return data
    data = {}
    status = False
    message = ""
    
# for admin use only
    if request.method == "POST":

        # get request body from request
        description = request.json.get("Description","")
        title = request.json.get("Title","")
        category = request.json.get("Category","")
        price = request.json.get("Price","")
        quantity = request.json.get("Quantity","")
        img_url = request.json.get("ImgUrl","")
        date = datetime.now()

        # strip slashes
        description = description.strip()
        category = category.strip()
        title =title.strip()
        img_url = img_url.strip()

        # check for empty fields
        if description == "":
            message = "Empty description field"
            return jsonify({"status":status, "message":message, "data":data})
        if category == "":
            message = "Empty category field"
            return jsonify({"status":status, "message":message, "data":data})
        if price == "":
            message = "Empty price field"
            return jsonify({"status":status, "message":message, "data":data})
        if quantity == "":
            message = "Empty quantity field"
            return jsonify({"status":status, "message":message, "data":data})
        if title == "":
            message = "Empty title field"
            return jsonify({"status":status, "message":message, "data":data})
        if img_url == "":
            message = "Empty image url field"
            return jsonify({"status":status, "message":message, "data":data})
        
        try:

            db.store.insert_one({"Description":description, "Category":category,"Title":title, "Price":price, "Quantity": quantity, "ImgUrl":img_url,"Created_at":date})

            data = {"Description":description, "Category":category, "Price":price, "Title":title, "Quantity": quantity, "ImgUrl":img_url,"Created_at":date}

            status = True
        except:
            message ="an error occurred"

# users end 
    else:
        # get db items
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page",10,type=int)
        items = db.store.find()
        data = []
        for item in items:
            itemdata = {"Id": str(item["_id"]), "Description":item["Description"], "Category":item["Category"], "Price":item["Price"], "Title":item["Title"], "Quantity": item["Quantity"], "ImgUrl":item["ImgUrl"],"Created_at":item["Created_at"]}
            data.append(itemdata)
        status = True

    return jsonify({"status":status,"message":message,"data":data})


