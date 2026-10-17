from flask import Flask,request,jsonify
from models import db, AUTHUR 
def register_authur_routes(app):


    @app.route("/authurs", methods=["post"])
    def add_authur():
        try:
            data=request.get_json()
            new_authur=[]
            for item in data:
                authur=AUTHUR(Name=item["Name"])
                new_authur.append(authur)
            db.session.add_all(new_authur)
            db.session.commit()        
            return jsonify({"message":"Authur added successfully"})
        except Exception as e:
            return jsonify({"message":str(e)})
        
        
        
    @app.route("/get_authurs",methods=["get"])
    def get_authur():
        try:
            
            authurs=AUTHUR.query.all()
            result=[]
            for a in authurs:
                result.append({
                "Name" :a.Name
                
                })
            return jsonify(result),200
        except Exception as e:
            return jsonify({"message":str(e)})
        