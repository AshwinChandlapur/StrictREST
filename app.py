from flask import Flask,render_template,redirect,request,jsonify,g
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
import Users


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/ashwinchandlapur/Desktop/StrictREST/todo.db'


db_sqlite  = SQLAlchemy(app)
dbsession = db_sqlite.session

@app.route("/user",methods=['GET'])
def get_all_users():
    allUsers = Users.User.query.all();
    list = []
    for user in allUsers:
        list.append(user.public_id)
    return jsonify({"users":list})

# Here user_id is dynamic.
@app.route("/user/<public_id>",methods=['GET'])
def get_one_users(public_id):
    user = Users.User.query.filter_by(public_id = public_id).first();
    if not user:
        return jsonify({'message':"No User Found"})
    else:
        return jsonify({'username':user.name})

@app.route("/user",methods=['POST'])
def createUser():
    userDetails = request.get_json()
    hashedPassword = str(generate_password_hash(userDetails["password"],method='sha256'))
    adminStatus = userDetails['admin']

    new_user = Users.User(public_id=str(uuid.uuid4()),name=userDetails["name"],password=hashedPassword,admin=adminStatus)
    dbsession.add(new_user)
    db_sqlite.create_all()
    dbsession.commit()

    return jsonify({'message':'New User Created'})

# Here user_id is dynamic.
@app.route("/user/<public_id>",methods=['PUT'])
def promote_user (public_id):
    user = Users.User.query.filter_by(public_id = public_id).first()
    if user:
        user.admin = 1
        current_db_sessions = dbsession.object_session(user)

        dbsession.commit()
        current_db_sessions.commit()
        return jsonify({"message":"Privileges Updated"})
    else:
        return jsonify({"message":"No Such Users"})

@app.route("/user/<public_id>", methods = ['DELETE'])
def delete_user(public_id):
    user = Users.User.query.filter_by(public_id = public_id).first()
    if user:
        current_db_sessions = dbsession.object_session(user)
        current_db_sessions.delete(user)
        dbsession.commit()
        current_db_sessions.commit()
        dbsession.flush
        return jsonify({"message":"Deleted User Succesfullt"})
    else:
        return jsonify({"message":"Delete a User Failed"})

@app.route("/")
def home():
    return "Home_Page"

if __name__ == "__main__":
    app.run(debug = True)