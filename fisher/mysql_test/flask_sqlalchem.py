# from tokenize import String

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Boolean, DateTime, Integer, String
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost:3306/news_test2?charset=utf8'
# db = SQLAlchemy(app)


# class News(db.Model):
#     __tablename__ = 'news'
#     id = db.Column(Integer, primary_key=True)
#     title = db.Column(String(200), nullable=False)
#     content = db.Column(String(2000), nullable=False)
#     types = db.Column(String(10), nullable=False)
#     image = db.Column(String(3000),)
#     author = db.Column(String(20),)
#     view_count = db.Column(Integer)
#     create_at = db.Column(DateTime)
#     is_valid = db.Column(Boolean)


# @app.route('/helle')
# def hello_word():
#     return 'Hello world hello!'


# if __name__ == '__main__':
# app.run()