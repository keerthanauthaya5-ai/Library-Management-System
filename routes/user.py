from flask import Flask,request,jsonify
from models import db, USER,LIBRARIAN,BOOK,AUTHUR
def register_user_routes(app):
    
    
    
    
    @app.route("/users",methods=["post"])
    def add_user():
        try:
            data=request.get_json()
            new_user=[]
            for item in data:
                user=USER(Name=item["Name"],
                          Library_No=item["Library_No"],
                        Ph_No=item["Ph_No"],
                        Email=item["Email"]
                        
                    )
                new_user.append(user)
            db.session.add_all(new_user)
            db.session.commit()
            return jsonify({"Message":"user added successcfylly"})
        except Exception as e:
            return jsonify({"Message":str(e)})
        


    @app.route("/users_get",methods=["Get"])
    def get_user():
        try:
            users=USER.query.all()
            result=[]
            for u in users:
                result.append({
                    "Name":u.Name,
                    "Library_No":u.Library_No,
                    "Email":u.Email,
                    "Ph_No":u.Ph_No
                    
                })
            return jsonify(result),200
        except Exception as e:
            return jsonify({"message":str(e)})
        


    @app.route("/user_get/<string:Library_No>",methods=["Get"])
    def get_By_ID(Library_No):
        try:
            users=USER.query.filter_by(Library_No=Library_No).first()
            librarians=LIBRARIAN.query.filter_by(Library_No =Library_No).all()
            result=[]
            for l in librarians:
                
                books=BOOK.query.get(l.Book_ID)
                authurs=AUTHUR.query.get(books.Authur_ID) if books else None
                result.append({
                
                "Book_Name":books.Title,
                "Authur_Name":authurs.Name,
                "Issue_Date":l.Issue_Date.strftime("%Y-%m-%d")if l.Issue_Date else None,
                "Return_Date":l.Return_Date.strftime("%Y-%m-%d")if l.Return_Date else None,
                 "Fine":l.Fine       }),200
                
                
            r={
                "User_Name": users.Name,
                "Email":users.Email,
                "Ph_No":users.Ph_No,
                "Book_Details":result
            }
            return jsonify(r)
                
        except Exception as e:
            return jsonify({"Message":str(e)})    
        
        
        
    @app.route("/user_delete/<int:users_ID>",methods=["Delete"])
    def delet_user(users_ID):
        users=USER.query.all(users_ID)
        db.session.delete(users)
        db.session.commit()
        return jsonify({"Message":f"USer with ID {users_ID} deleted successfullyy"})

        