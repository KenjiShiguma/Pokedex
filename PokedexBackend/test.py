from flask import Flask
from flask_cors import CORS
from flask import jsonify
from flask import request
app = Flask(__name__)
CORS(app)


@app.route("/")
def pokedex():
    if request.method == 'GET':
        h = "hello world"
        return jsonify(h)
    if request.method == 'POST':
        data = request.get_json()
        #get image from frontend

        #do hog and pcm of single image

        #predict image
        h = "pikachu"
        return jsonify(h)
if __name__ == "__main__":
    app.run()
