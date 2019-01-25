from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'todo.db'



db_sqlite  = SQLAlchemy(app)


@app.route("/")
def home():
    return "Home_Page"

if __name__ == "__main__":
    app.run(debug = True)