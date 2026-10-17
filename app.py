from flask import Flask
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:keerthana2003@localhost/library_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():
    db.create_all()



from routes.authur import register_authur_routes
from routes.book import register_book_routes
from routes.category import register_category_routes
from routes.librarian import register_librarian_routes

from routes.user import register_user_routes



register_authur_routes(app)
register_book_routes(app)
register_category_routes(app)
register_librarian_routes(app)
register_user_routes(app)



if __name__ == "__main__":
    app.run(debug=True)
