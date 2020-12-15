# Author(s): Kermit Mitchell III, Zeke Hammonds
# Start Date: 05/06/2019 5:30 PM | Last Editied: 12/15/2020 1:00 PM
# This code uses the trained Pokedex SVMs to identify the Pokemon in an given image.

# Essential Imports
import cv2 as cv # Image processing like HoG
import numpy as np # Fast matrix manipulation
from matplotlib import pyplot as plt # Graphing data
from sklearn import svm as SVM # machine learning models
import sklearn
from joblib import dump, load # saving and writing PCA/SVM
import os # file system access
import sys # for debugging and terminal print length

#print('The scikit-learn version is {}.'.format(sklearn.__version__))

## Relevant folder paths for ours SVMS, PCAs, and HOGs
svmFolderPath = './SVM/'
pcaFolderPath = './PCA/'
hogFolderPath = './HOG/'

# A vector of our labels, used below
labelVector = ["pikachu", "bulbasaur", "charmander", "squirtle", "ditto"] 

# This is our HOG Descriptor, and will be used for feature extraction
IMG_SIZE = 224 # the size of our imcoming images
winSize = (IMG_SIZE, IMG_SIZE) # same size as images
blockSize = (IMG_SIZE // 4, IMG_SIZE // 4) # (224/4)=56
blockStride = (IMG_SIZE // 8, IMG_SIZE // 8) # sliding window processes blocks by cell size
cellSize = (IMG_SIZE // 8, IMG_SIZE // 8) # same as above ^
L2HysThreshold = 0.2
nbins = 9 # angles from 0-180, increments of 20 degrees

hog = cv.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins, 1, 4, 0, 0.2, 0)

# Load in the trained Pokedex SVMs
svm0 = load(svmFolderPath + 'pikachuSVM.joblib')
svm1 = load(svmFolderPath + 'bulbasaurSVM.joblib')
svm2 = load(svmFolderPath + 'charmanderSVM.joblib')
svm3 = load(svmFolderPath + 'squirtleSVM.joblib')

# Returns the hog-pca matrix based on the input Pokemon
def pokePCA(hogMatrix, pokemon):
  PCA_Mean = load(pcaFolderPath + pokemon + 'PCA_Mean.joblib')
  PCA_Eigen = load(pcaFolderPath + pokemon + 'PCA_Eigen.joblib')
  pca = cv.PCAProject(hogMatrix, PCA_Mean, PCA_Eigen)
  return pca

# Enter in the filepath and name of the image, and predicts which Pokemon it is
def predictPokemon(testImgURL):
  #testImgURL = "pikachu_kerem.jpg"#bulbasaurTestingData[24]
  #             ^ replace with the actual test image from camera
  #bulbasaurTestingData[30] <-- if you wanted to test from testing set instead

  testImg = cv.imread(testImgURL)
  if testImg is None:
    print("Invalid file or incorrect path.")
    quit()
  testImg = cv.resize(testImg, (IMG_SIZE, IMG_SIZE))
  #cv.imshow(testImgURL, testImg)
  #cv.waitKey(0)
  #cv.destroyAllWindows()

  # Run this image through HOG and PCA for each Pokemon

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
  print(predictions)

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
    finalAnswer = "Ditto" # this means the testImg was neither class aka inconclusive

  #print('Final Prediction:', finalAnswer)
  #cv.imshow(testImgURL, testImg)
  #cv.waitKey(0)
  #cv.destroyAllWindows()

  #print(finalAnswer)
  return finalAnswer

# Tests an individual image
myImgUrl = input("Enter an image (filepath and filename) of Pikachu, Bulbasaur, Charmander, or Squirtle: ")
#"Revisions/bulbagrey.png" # This would be the filename and path
print(predictPokemon(myImgUrl))
myTestImg = cv.imread(myImgUrl)
cv.imshow(myImgUrl, myTestImg)
cv.waitKey(0)
cv.destroyAllWindows()