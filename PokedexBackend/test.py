from flask import Flask
from flask_cors import CORS
from flask import jsonify
app = Flask(__name__)
CORS(app)

@app.route("/")
def helloWorld():
    h = "hello world"
    return jsonify(h)


if __name__ == "__main__":
    app.run()
