from flask import Flask
from flask_cors import CORS
from flask import jsonify
from flask import request
import numpy as np
import flask
import cv2
import json
app = Flask(__name__)
CORS(app)


@app.route("/", methods=['POST', 'GET'])
def pokedex():
    #get image from frontend
    imagefile = json.loads(request.data)
    #do hog and pca of single image

    #predict image

    #console.log(h)
    return jsonify(imagefile)
if __name__ == "__main__":
    app.run()
