from flask import Flask, render_template
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.api import api
from app.system import get_system_info
from app.metrics import (
    record_request,
    record_response_time,
)

import time

app = Flask(__name__, template_folder="../templates")

# Register API routes
app.register_blueprint(api)


@app.route("/")
def home():
    start = time.time()

    record_request()

    system = get_system_info()

    record_response_time(time.time() - start)

    return render_template(
        "index.html",
        status=system["status"],
        cpu=system["cpu"],
        memory=system["memory"],
    )


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True,
    )
