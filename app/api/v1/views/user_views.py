from flask import Blueprint, request, jsonify
import datetime
from app.api.v1.models.models import Users

time_now = datetime.datetime.now()

v1_mod = Blueprint('apiv1', __name__)


@v1_mod.route("/signup", methods=["POST"])
def user_signup():
    try:
        user_data = request.get_json()
        if not user_data:
            return jsonify({"status": 204, "error": "No data found"}), 204

        try:
            if not user_data["firstName"] or not user_data["lastName"] or not user_data["userName"] or not user_data["email"] or not user_data["phone"] or not user_data["password"]:
                return jsonify({"status": 422, "error": "all fields are required(firstName,lastName,password,userName,phone and email)"}), 422

        except:
            return jsonify({"status": 400, "error": "a key field is missing"}), 400

        new_user = {}
        for key in user_data:
            new_user[key] = user_data[key]

        try:
            latest = Users[-1]
            for user in Users:
                if user["userName"] == user_data["userName"]:
                    return jsonify({"status": 409, "error": "user with that name already exists"}), 409

            id = latest["id"]
            id = id + 1
            new_user["id"] = id
            new_user["isAdmin"] = False
        except:
            new_user["id"] = 1
            new_user["isAdmin"] = True

        new_user["regDate"] = time_now.strftime("%D")

        Users.append(new_user)
        return jsonify({"status": 201, "data": new_user}), 201

    except:
        return jsonify({"status": 400, "error": "signup data is required"}), 400
