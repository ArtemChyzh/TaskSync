from flask import Flask, make_response, jsonify
from random import choice
import requests

ROOMS_SERVICE = "http://rooms_service:3000"

app = Flask(__name__)

lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
full = lowercase + uppercase + digits

def create_code(length: int):
    return ''.join(choice(full) for _ in range(length))

@app.route("/code")
def get_code():
    try:
        respond = requests.get(f"{ROOMS_SERVICE}/rooms/codes")
        respond.raise_for_status()
        codes = respond.json()

        code = create_code(6)
        while code in codes:
            code = create_code(6)
            
        return make_response(jsonify({"code": code}), 200)
    except requests.HTTPError as err:
        return make_response(jsonify({"error": f"Rooms service returned error: {str(err)}"}), err.response.status_code)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
