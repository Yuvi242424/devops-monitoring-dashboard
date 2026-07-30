from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter("app_requests_total", "Total number of requests")

ERROR_COUNT = Counter("app_errors_total", "Total number of simulated errors")

REQUEST_TIME = Histogram("app_request_duration_seconds", "Request processing time")


def record_request():
    REQUEST_COUNT.inc()


def record_error():
    ERROR_COUNT.inc()


def record_response_time(duration):
    REQUEST_TIME.observe(duration)
