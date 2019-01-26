from flask import Flask,render_template,redirect,request,jsonify,g
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
import Users


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/ashwinchandlapur/Desktop/StrictREST/todo.db'


db_sqlite  = SQLAlchemy(app)


@app.route("/user",methods=['GET'])
def get_all_users():
    return "Should return all users"

# Here user_id is dynamic.
@app.route("/user/<public_id>",methods=['GET'])
def get_one_users(public_id):
    user = Users.User.query.filter_by(public_id = public_id).first();
    if not user:
        return jsonify({'message':"No User Found"})
    else:
        return jsonify({'message':user.name})

@app.route("/user",methods=['POST'])
def createUser():
    userDetails = request.get_json()
    hashedPassword = str(generate_password_hash(userDetails["password"],method='sha256'))

    new_user = Users.User(public_id=str(uuid.uuid4()),name=userDetails["name"],password=hashedPassword,admin=True)
    db_sqlite.session.add(new_user)
    db_sqlite.create_all()
    db_sqlite.session.commit()

    return jsonify({'message':'New User Created'})

# Here user_id is dynamic.
@app.route("/user/<user_id>",methods=['PUT'])
def promote_user ():
    return "Promote User to Admin"

@app.route("/user/<user_id>", methods = ['DELETE'])
def delete_user():
    return "Delete a User"

@app.route("/")
def home():
    return "Home_Page"

if __name__ == "__main__":
    app.run(debug = True)