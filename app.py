from flask import Flask,render_template,redirect,request,jsonify,g,make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
import Users
import jwt
import datetime


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
    current_db_sessions = dbsession.object_session(new_user)
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

@app.route("/login")
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Could Not Verify, Should Sign in",401,{'WWW-Authenticate':'Basic realm="Login Require"'})

    user = Users.User.query.filter_by(name = auth.username).first()

    if not user:
        return make_response("Could Not Verify,No user", 401, {'WWW-Authenticate': 'Basic realm="Login Require"'})

    if check_password_hash(user.password,auth.password):
        token = jwt.encode({'publid_id':user.public_id,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        return jsonify({"token":token.decode("UTF-8")})

    return make_response("Could Not Verify, No data", 401, {'WWW-Authenticate': 'Basic realm="Incorrect Password"'})

@app.route("/")
def home():
    return "Home_Page"

if __name__ == "__main__":
    app.run(debug = True)