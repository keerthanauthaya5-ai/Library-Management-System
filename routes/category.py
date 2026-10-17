from flask import Flask,request,jsonify
from models import db,CATEGORY
def register_category_routes(app):

    @app.route("/categorys",methods=["POST"])
    def add_category():
        try:
            data=request.get_json()
            new_category=[]
            for item in data:
                category=CATEGORY(Name=item["Name"])
                new_category.append(category)
            db.session.add_all(new_category)
            db.session.commit()
            return jsonify({"message":"category added successfuly"}),201
        except Exception as e:
            return jsonify({"message":str(e)})
        
        
        
    @app.route("/get_categorys",methods=["GET"])
    def Get_category():
        try:
            categorys=CATEGORY.query.all()
            result=[]
            for c in categorys:
                result.append({
                    "Name":c.Name
                })
            return jsonify(result),200
        except Exception as e:
            return jsonify({"Message":str(e)})


            
        
        
        