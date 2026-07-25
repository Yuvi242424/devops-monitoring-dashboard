from flask import Flask, render_template, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import psutil
import time

app = Flask(__name__, template_folder="../templates")

# -------------------------
# Metrics
# -------------------------

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of requests"
)

ERROR_COUNT = Counter(
    "app_errors_total",
    "Total number of simulated errors"
)

REQUEST_TIME = Histogram(
    "app_request_duration_seconds",
    "Request processing time"
)

# -------------------------
# Dashboard Variables
# -------------------------

request_counter = 0
error_counter = 0


@app.route("/")
def home():

    global request_counter

    start = time.time()

    request_counter += 1
    REQUEST_COUNT.inc()

    cpu = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory().percent

    REQUEST_TIME.observe(time.time() - start)

    return render_template(
        "index.html",
        status="Running",
        requests=request_counter,
        errors=error_counter,
        cpu=cpu,
        memory=memory
    )


@app.route("/generate-load")
def generate_load():

    total = 0

    for i in range(500000):
        total += i * i

    REQUEST_COUNT.inc()

    return jsonify(
        {
            "message": "Load Generated"
        }
    )


@app.route("/generate-error")
def generate_error():

    global error_counter

    error_counter += 1

    ERROR_COUNT.inc()

    return jsonify(
        {
            "message": "Error Generated"
        }
    )


@app.route("/health")
def health():

    return jsonify(
        {
            "status": "healthy"
        }
    )


@app.route("/metrics")
def metrics():

    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )