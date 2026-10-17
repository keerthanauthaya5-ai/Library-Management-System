from flask import Flask,request,jsonify
from models import db,LIBRARIAN,BOOK,USER
from datetime import datetime
def register_librarian_routes(app):



    @app.route("/librarians",methods=["post"])
    def add_librarians():
        try:
            data=request.get_json()
            new_librarian=[]
            for item in data:
                issue_date = datetime.strptime(item["Issue_Date"],"%Y-%m-%d")
                due_date=datetime.strptime(item["Due_Date"],"%Y-%m-%d")

                
                book = BOOK.query.get(item["Book_ID"])
                if not book:
                    return jsonify({"message": f"Book_ID {item['Book_ID']} not found"}), 404

                if book.Available_Copies < 1:
                    return jsonify({"message": f"Book_ID {item['Book_ID']} is not available"}), 404

                book.Available_Copies -= 1

                    
                librarian=LIBRARIAN(Book_ID=item["Book_ID"],
                            Library_No=item["Library_No"],
                            Issue_Date=issue_date,
                            Due_Date=due_date, 
                            Return_Date=None,                     
                            Fine=None
                        )
                new_librarian.append(librarian)
            db.session.add_all(new_librarian)
            db.session.commit()
            return jsonify({"message":"Book issued Successfully"}),200
        except Exception as e:
            return jsonify({"message":str(e)}),500
        
        
        
    @app.route("/librarians/<string:Library_No>/<int:Book_ID>",methods=["Put"])
    def return_book(Library_No,Book_ID):
        try:
            library=LIBRARIAN.query.filter_by(Library_No=Library_No,Book_ID=Book_ID).first()
            data=request.get_json()
            
            return_date=datetime.strptime(data["Return_Date"],"%Y-%m-%d")
            library.Return_Date=return_date
            
            fine=0
            if return_date > library.Due_Date:
                late_days=(return_date - library.Due_Date).days
                fine=late_days*5
            library.Fine=fine
            
            book=BOOK.query.get(library.Book_ID)
            if book:
                book.Available_Copies+=1
            db.session.commit()
            return jsonify({"Message":"Book returned successfully","fine":fine}),200
        except Exception as e:
            return jsonify({"Message":str(e)}),500
        
    @app.route("/get_librarians",methods=["Get"])
    def get_librarians():
        try:
            librarian=LIBRARIAN.query.all()
            result=[]
            for i in librarian:
                result.append({
                    "Book_ID":i.Book_ID,
                    "Library_No":i.Library_No,
                    "Issue_Date":i.Issue_Date.strftime("%Y-%m-%d")if i.Issue_Date else None, 
                    "Return_Date":i.Return_Date.strftime("%Y-%m-%d")if i.Return_Date else None,
                    "Due_Date":i.Due_Date.strftime("%Y-%m-%d")if i.Due_Date else None,
                    "Fine":i.Fine
                })
            return jsonify(result),200


        except Exception as e:
            return jsonify({"Message":str(e)}),500


    @app.route("/Library/<string:start>/<string:end>",methods=["Get"])
    def date_by_range(start,end):
        try:    
            start_date=datetime.strptime(start,"%Y-%m-%d").date()
            end_date=datetime.strptime(end,"%Y-%m-%d").date()
            library=LIBRARIAN.query.filter(
                LIBRARIAN.Issue_Date >= start_date,
                LIBRARIAN.Issue_Date <= end_date
            ).all()
            
            
            result=[]
            for l in library:
                
                user = USER.query.filter_by(Library_No=l.Library_No).first()
                book=BOOK.query.get(l.Book_ID)
                result.append({
                    "user_Name":user.Name if user else None,
                    "Library_No":l.Library_No,
                     "Issue_Date":l.Issue_Date.strftime("%Y-%m-%d"),
                     "Return_Date":l.Return_Date.strftime("%Y-%m-%d") if l.Return_Date else None,
                     "Title":book.Title  
                })
                
            return jsonify(result),200
        except Exception as e:
            return jsonify({"message":str(e)}),500


        
        
            
            