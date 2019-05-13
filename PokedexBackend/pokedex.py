from flask import Flask
from flask_cors import CORS
from flask import jsonify
from flask import request
import flask
import cv2
import json
import cv2 as cv # Image processing like HoG
import numpy as np # Fast matrix manipulation
from matplotlib import pyplot as plt # Graphing data
from sklearn import svm as SVM # machine learning models
from joblib import dump, load # saving and writing PCA/SVM
import os # file system access
import sys # for debugging and terminal print length
app = Flask(__name__)
CORS(app)

IMG_SIZE = 224 # the size of our imcoming images
winSize = (IMG_SIZE, IMG_SIZE) # same size as images
blockSize = (IMG_SIZE // 4, IMG_SIZE // 4) # (224/4)=56
blockStride = (IMG_SIZE // 8, IMG_SIZE // 8) # sliding window processes blocks by cell size
cellSize = (IMG_SIZE // 8, IMG_SIZE // 8) # same as above ^
L2HysThreshold = 0.2
nbins = 9 # angles from 0-180, increments of 20 degrees
labelVector = ["pikachu", "bulbasaur", "charmander", "squirtle"]

# Computes the HOG Descriptor, forcing the correct img_size
def computeHOG(img):
  im = cv.imread(img, 0)
  shape = im.shape

  if shape[0] != IMG_SIZE or shape[1] != IMG_SIZE:
    im = cv.resize(im, (IMG_SIZE, IMG_SIZE))

  #cv.imshow('Resized Image', im)
  #cv.waitKey(0)
  #cv.destroyAllWindows()

  hist = hog.compute(im, winSize)

  return hist

def pokePCA(hogMatrix, pokemon):
  PCA_Mean = load('svms/' + pokemon + 'PCA_Mean.joblib')
  PCA_Eigen = load('svms/' + pokemon + 'PCA_Eigen.joblib')
  pca = cv.PCAProject(hogMatrix, PCA_Mean, PCA_Eigen)
  return pca

@app.route("/", methods=['POST', 'GET'])
def pokedex():

    hog = cv.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins, 1, 4, 0, 0.2, 0)
    imagefile = json.loads(request.data)
    test = imagefile["data"]
    testImgURL = '../src/assets/SamplePokemon/' + test
    testImg = cv.imread(testImgURL)
    svm0 = load('svms/pikachuSVM.joblib')
    svm1 = load('svms/bulbasaurSVM.joblib')
    svm2 = load('svms/charmanderSVM.joblib')
    svm3 = load('svms/squirtleSVM.joblib')

    testImg = cv.imread(testImgURL)
    testImg = cv.resize(testImg, (IMG_SIZE, IMG_SIZE))
    #do hog and pca of single image
    testImgHOG = hog.compute(testImg, winSize)
    testImgHOG = testImgHOG.transpose()
    pikachuTestImgHOG = pokePCA(testImgHOG, labelVector[0])
    bulbasaurTestImgHOG = pokePCA(testImgHOG, labelVector[1])
    charmanderTestImgHOG = pokePCA(testImgHOG, labelVector[2])
    squirtleTestImgHOG = pokePCA(testImgHOG, labelVector[3])

    scoreScaler = 1 # used to scale the scores for readability
    predictions = np.empty((4, 2)) # the final predictions of all 4 SVMs
    predictions[0][0] = (int)(svm0.predict(pikachuTestImgHOG)[0])
    predictions[0][1] = round((svm0.score_samples(pikachuTestImgHOG))[0], 4) * scoreScaler
    predictions[1][0] = (int)(svm1.predict(bulbasaurTestImgHOG)[0])
    predictions[1][1] = round((svm1.score_samples(bulbasaurTestImgHOG))[0], 4) * scoreScaler
    predictions[2][0] = (int)(svm2.predict(charmanderTestImgHOG)[0])
    predictions[2][1] = round((svm2.score_samples(charmanderTestImgHOG))[0], 4) * scoreScaler
    predictions[3][0] = (int)(svm3.predict(squirtleTestImgHOG)[0])
    predictions[3][1] = round((svm3.score_samples(squirtleTestImgHOG))[0], 4) * scoreScaler


    # Calculate the max prediction score, and select the final result
    currentMaxIndex = -1
    currentMaxValue = sys.float_info.min
    for i in range(predictions.shape[0]):
      if(predictions[i][1] > currentMaxValue):
        currentMaxValue = predictions[i][1]
        currentMaxIndex = i

    finalAnswer = labelVector[currentMaxIndex]
    threshold = 1.0 * (10**-2) # Eliminates scores that are too low
    if(currentMaxValue < threshold or currentMaxIndex == -1):
      finalAnswer = "ditto" # this means the testImg was neither class

    return jsonify(finalAnswer)
if __name__ == "__main__":
    app.run()
