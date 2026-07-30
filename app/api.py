from flask import Blueprint, jsonify
from system import get_system_info, get_health
from metrics import record_request, record_error

api = Blueprint("api", __name__)


@api.route("/api/health")
def health():
    record_request()
    return jsonify(get_health())


@api.route("/api/system")
def system():
    record_request()
    return jsonify(get_system_info())


@api.route("/api/load", methods=["POST"])
def generate_load():
    total = 0

    for i in range(500000):
        total += i * i

    record_request()

    return jsonify({"message": "Load Generated"})


@api.route("/api/error", methods=["POST"])
def generate_error():
    record_error()

    return jsonify({"message": "Error Generated"})
