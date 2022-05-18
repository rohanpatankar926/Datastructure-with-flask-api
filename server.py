from flask import Flask,jsonify,request,render_template
from sqlite3 import Connection as SQLite3Connection
from sqlalchemy import event
import sqlalchemy
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import linked_list

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=0

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

db=SQLAlchemy(app)
now=datetime.now()

class User(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(60))
    email=db.Column(db.String(60))
    adress=db.Column(db.String(100))
    phone=db.Column(db.String(15))
    posts=db.relationship("Blogpost")
    
class Blogpost(db.Model):
    __tablename__="blogpost"
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(60))
    body=db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    
#routes
@app.route("/",methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/user",methods=["POST"])
def create_user():
    data=request.get_json()
    add_user=User(name=data["name"],email=data["email"],adress=data["address"],phone=data["phone"])
    db.session.add(add_user)
    db.session.commit()
    return jsonify({"message":"User created successfully"}),200

@app.route("/user/descending_id",methods=["GET"])
def get_all_user_descending():
    users=User.query.all()
    all_users_ll=linked_list.LinkedList()
    for user in users:
        all_users_ll.insert_beginning({"id":user.id,"name":user.name,"email":user.email,"adress":user.adress,"phone":user.phone})
    return jsonify(all_users_ll.to_list()),200

@app.route("/user/ascending_id",methods=["GET"])
def get_all_user_ascending():
    pass

@app.route("/user/<user_id>",methods=["GET"])
def get_one_user(user_id):
    pass

@app.route("/user/<user_id>",methods=["DELETE"])
def delete_user(user_id):
    pass

@app.route("/user/<user_id>",methods=["POST"])
def create_blog_post(user_id):
    pass

@app.route("/user/<user_id>",methods=["GET"])
def get_all_blog_post(user_id):
    pass

@app.route("/blog_post/<blog_post_id>",methods=["GET"])
def get_one_blog_post(blog_post_id):
    pass

@app.route("/blog_post/<blog_post_id>",methods=["DELETE"])
def delete_blog_post(user_id):
    pass

if __name__=="__main__":
    app.run(debug=True,port=5000)
