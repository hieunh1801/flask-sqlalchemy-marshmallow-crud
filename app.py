from flask import Flask, request, jsonify
from db_config import db, ma
from user import UserModel, UserSchema, UserCRUD
import datetime
from collections import defaultdict

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['JSON_AS_ASCII'] = False

db.init_app(app)
with app.app_context():
    db.create_all()
ma.init_app(app)


@app.route("/")
def hello_world():
    return "Hello World"


@app.route("/users", methods=["GET", "POST"])
def users():
    method = request.method
    if method == "GET":
        page_size = request.args.get("page_size")
        page_number = request.args.get("page_number")
        list_user, total = UserCRUD().get_all(
            page_size=page_size, page_number=page_number)
        return jsonify({"data": list_user, "total": total})
    if method == "POST":
        payload = {}
        payload["username"] = request.json.get("username")
        payload["password"] = request.json.get("password")
        date_of_bird = request.json.get("date_of_bird")
        if date_of_bird:
            time_format = "%Y-%m-%d"
            payload["date_of_bird"] = datetime.datetime.strptime(
                date_of_bird, time_format)
        user = UserCRUD().create(payload)
        return jsonify(user)


@app.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"])
def user(user_id):
    method = request.method
    if method == "GET":
        user = UserCRUD().get_by_id(user_id)
        return jsonify(user)
    if method == "PUT":
        payload = {}
        payload["username"] = request.json.get("username")
        payload["password"] = request.json.get("password")
        date_of_bird = request.json.get("date_of_bird")
        if date_of_bird:
            time_format = "%Y-%m-%d"
            payload["date_of_bird"] = datetime.datetime.strptime(
                date_of_bird, time_format)
        user = UserCRUD().update(user_id, payload)
        return jsonify(user)
    if method == "DELETE":
        user = UserCRUD().delete(user_id)
        print("delete user", user)
        return jsonify(user)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
