from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def root():
    return "Welcome to simple webapp"


@app.get("/healthz")
def healthz():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)  # nosec B104
