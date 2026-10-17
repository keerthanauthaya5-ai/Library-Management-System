
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
from datetime import datetime
from sqlalchemy import BigInteger



class USER(db.Model):
    __tablename__= "users"
    ID = db.Column(db.Integer,primary_key=True)
    Library_No = db.Column(db.String(50), unique=True) 
    Name=db.Column(db.String(50),nullable=False)
    Ph_No=db.Column(db.BigInteger,nullable=False)
    Email=db.Column(db.String(90),nullable=False)
    
    librarians = db.relationship("LIBRARIAN", backref="user", lazy=True, cascade='all, delete')
   


  
class LIBRARIAN(db.Model):
    __tablename__="librarians"
    ID =db.Column(db.Integer,primary_key=True)
    Library_No=db.Column(db.String(50),db.ForeignKey("users.Library_No"),nullable=False)
    Book_ID = db.Column(db.Integer,db.ForeignKey("books.ID"),nullable=False)
    Issue_Date=db.Column(db.DateTime,default=datetime.utcnow)
    Due_Date=db.Column(db.DateTime,default=datetime.utcnow)
    Return_Date=db.Column(db.DateTime,default=None,nullable=True)
    Fine=db.Column(db.Integer,default=0)
    
    
    
class BOOK(db.Model):
    __tablename__="books"
    ID=db.Column(db.Integer,primary_key=True)
    Category_ID=db.Column(db.Integer,db.ForeignKey("categorys.ID"))
    Title=db.Column(db.String(50),nullable=False)
    Authur_ID=db.Column(db.Integer,db.ForeignKey("authurs.ID"))
    Available_Copies= db.Column(db.Integer, nullable=False)
    
    librarians=db.relationship("LIBRARIAN",backref="book",lazy=True,cascade='all, delete')
    
    
class AUTHUR(db.Model):
    __tablename__="authurs"
    ID=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)
    
    books=db.relationship("BOOK",backref="authur",lazy=True,cascade='all, delete')
    
    
class CATEGORY(db.Model):
    __tablename__="categorys"
    ID=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(50),nullable=False)
    
    books=db.relationship("BOOK",backref="category",lazy=True,cascade='all, delete')
    
