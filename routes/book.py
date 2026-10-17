from flask import Flask,request,jsonify
from models import db,BOOK,USER,LIBRARIAN,AUTHUR,CATEGORY
def register_book_routes(app):

    @app.route("/books",methods=["Post"])
    def add_book():
        try:
            data=request.get_json()
            new_book=[]
            for item in data:
                book=BOOK(Title=item["Title"],
                        Authur_ID=item["Authur_ID"],
                        Category_ID=item["Category_ID"],
                        Available_Copies=item["Available_Copies"]
                        
                )
                new_book.append(book)
            db.session.add_all(new_book)
            db.session.commit()
            return jsonify({"message":"book added succesfully"})
        except Exception as e:
            return jsonify({"message":str(e)})
        
        
        
    @app.route("/get_books",methods=["Get"])
    def get_books():
        try:
            books=BOOK.query.all()
            result=[]
            for b in books:
                result.append({
                    "Title":b.Title,
                    "Authur_ID":b.Authur_ID,
                    "Category_ID":b.Category_ID,
                    "Available_Copies":b.Available_Copies
                   
                    
                    
                })
            return jsonify(result),200
        except Exception as e:
            return jsonify({"message":str(e)})
        

        
        
    @app.route("/get_book/<int:book_ID>",methods=["Get"])
    def get_by_books_ID(book_ID):
        try:
            library = LIBRARIAN.query.filter_by(Book_ID=book_ID).all()
            result=[]
            for u in library:
                books=BOOK.query.get(u.Book_ID)
                authurs=AUTHUR.query.get(books.Authur_ID)
                categorys=CATEGORY.query.get(books.Category_ID)
                users = USER.query.filter_by(Library_No=u.Library_No).first()

                result.append({
                    
                    "Library_No":u.Library_No,
                    "User_Name":users.Name if users else None,
                    "Issue_Date":u.Issue_Date.strftime("%Y-%m-%d")if u.Issue_Date else None,
                    "Return_Date":u.Return_Date.strftime("%Y-%m-%d")if u.Return_Date else None
                    
                })
            r={
                "Book_Name":books.Title ,
                    "Authur_Name":authurs.Name if authurs else None,
                    "category_Name":categorys.Name if categorys else None,
                    "issued_users":result
            }
                
            return jsonify(r)
        except Exception as e:
            return jsonify({"message":str(e)})
        
            
    @app.route("/delete_book", methods=["DELETE"])
    def delete_books():
        try:
            books_id = request.json.get("books_id") 

            if not books_id:
                return {"error": "No book IDs provided"}, 400

            BOOK.query.filter(BOOK.ID.in_(books_id)).delete(synchronize_session=False)
            db.session.commit()

            return {"message": "Books deleted successfully"},200
        
        except Exception as e:
            return jsonify({"Message":str(e)})
        
            