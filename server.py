from flask import Flask, Response,request,jsonify
import pymongo
import json
from bson.objectid import ObjectId
app =  Flask(__name__)

  # mongoDB Connectivity

try:
    mongo = pymongo.MongoClient(
        host = "localhost",
        port = 27017,
        serverSelectionTimeoutMS = 1000         
    )
    db = mongo.company
    mongo.server_info()
except : 
    print("Error - Cannot connect to db")

##############################

#create user API

@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = { "name" : request.form["name"], "email" : request.form["email"],"pwd" : request.form["pwd"]}
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        return Response(response = json.dumps({"message" : "user created","id" : f"{dbResponse.inserted_id}"}),status = 200,    
                        mimetype = "application/json")                     
    except Exception as ex:
        print(ex)
##############################

#reading a user API

@app.route("/users", methods = ["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])                                 # i have to replace _id with ID?
        return Response(response = json.dumps(data),status = 500,    
                        mimetype = "application/json") 
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : "cannot read users" }),status = 500,    
                        mimetype = "application/json") 
##############################

#updating a user API

@app.route("/users/<id>",methods = ["PUT"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set":{"name": request.form["name"]}}
        )
        #for attr in dir(dbResponse):
        #    print(f"***{attr}***")
        if dbResponse.modified_count == 1:
            return Response(response = json.dumps({"message" : "user updated" }),status = 200,    
                        mimetype = "application/json") 
        else:
            return Response(response = json.dumps({"message" : "nothing to update" }),status = 200,    
                        mimetype = "application/json")
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : "sorry cannot update user" }),status = 500,    
                        mimetype = "application/json") 
##############################

#delete a user

@app.route("/users/<id>", methods = ["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(response = json.dumps({"message" : "user deleted","id":f"{id}" }),status = 200,    
                        mimetype = "application/json")
        else:
            return Response(response = json.dumps({"message" : "user not found","id":f"{id}" }),status = 200,    
                        mimetype = "application/json")
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : "sorry cannot delete user" }),status = 500,    
                        mimetype = "application/json")

##############################

# diplaying users by specifying an ID

@app.route("/users/<id>", methods = ["GET"])
def displaying_users(id):
    try:
        print(id)
        data =  list(db.users.find({"_id":ObjectId(id)}))               
        #print("absc*****************************************************")
        #print((data[0]))
        del data[0]['_id']
        return jsonify(data[0])
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : "sorry user does not exist" }),status = 500,    
                        mimetype = "application/json")
##############################

##############################
if __name__ == "__main__":
    app.run(port = 80, debug = True)