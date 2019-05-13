# Author(s): Kermit Mitchell III, Zeke Hammond
# Start Date: 05/06/2019 5:30 PM | Last Editied: 05/12/2019 7:00 PM
# This code is assorted functions and code snippets that will help us train the SVM

import cv2 as cv # Image processing like HoG
import numpy as np # Fast matrix manipulation
from matplotlib import pyplot as plt # Graphing data
from sklearn import svm as SVM # machine learning models
from joblib import dump, load # saving and writing PCA/SVM
import os # file system access
import sys # for debugging and terminal print length
#np.set_printoptions(threshold=sys.maxsize) | toggle for full values in terminal

# These are our folders with our dataset
trainDataPath = '../_pokedex_dataset/_training_data' # absolute file path to my training data
testDataPath = '../_pokedex_dataset/_testing_data' # absolute file path to my testing data

# A vector of our labels, used below
labelVector = ["pikachu", "bulbasaur", "charmander", "squirtle"] 

# Loop through each image in the datasets, and store their filepaths in arrays

'''
for each pokemon in labelVector:
    for each file in the training data/THAT_POKEMON:
        grab the filePath and store in an array
    return an array with all of the filePaths for each image 
'''

# Returns an array all dataset image URLs
def labelTheData(dataFolder):
    labeledData = np.array([])
    for file in os.listdir(dataFolder):
        filename = os.fsdecode(file)
        #print(filename)
        labeledData = np.append(labeledData, dataFolder +'/' + filename)
    return labeledData

# Use the labelTheData function for each Pokemon, and for Train/Test
pikachuTrainingData = labelTheData(trainDataPath + '/_' + labelVector[0])
pikachuTestingData = labelTheData(testDataPath + '/_' + labelVector[0])
bulbasaurTrainingData = labelTheData(trainDataPath + '/_' + labelVector[1])
bulbasaurTestingData = labelTheData(testDataPath + '/_' + labelVector[1])
charmanderTrainingData = labelTheData(trainDataPath + '/_' + labelVector[2])
charmanderTestingData = labelTheData(testDataPath + '/_' + labelVector[2])
squirtleTrainingData = labelTheData(trainDataPath + '/_' + labelVector[3])
squirtleTestingData = labelTheData(testDataPath + '/_' + labelVector[3])

# This is our HOG Descriptor, and will be used for feature extraction
IMG_SIZE = 224 # the size of our imcoming images
winSize = (IMG_SIZE, IMG_SIZE) # same size as images
blockSize = (IMG_SIZE // 4, IMG_SIZE // 4) # (224/4)=56
blockStride = (IMG_SIZE // 8, IMG_SIZE // 8) # sliding window processes blocks by cell size
cellSize = (IMG_SIZE // 8, IMG_SIZE // 8) # same as above ^
L2HysThreshold = 0.2
nbins = 9 # angles from 0-180, increments of 20 degrees

hog = cv.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins, 1, 4, 0, 0.2, 0)
#cv.HOGDescriptor.write(hog, "pokedexHOG.xml") # Saves the HOG for later use | restore with load('')
#help(cv.HOGDescriptor())

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

'''
for each image in a training dataset
  calculate the HoG, and add that to a matrix of HoGs
run the PCA algo on that matrix of HoGs to reduce feature size
'''

def HOG_PCA_Matrix(dataset, pokemon):
  originalFeatureSize = computeHOG(dataset[0]).shape[0]
  hogMatrix = np.empty((dataset.shape[0], originalFeatureSize))
  for i in range(0, dataset.shape[0]):
    hist = computeHOG(dataset[i])
    for k in range(0, originalFeatureSize):
      hogMatrix[i][k] = hist[k][0]
  
  #Run PCA to reduce feature dimensions, and save it for future use
  mean, eigenVectors = cv.PCACompute(hogMatrix, mean=None, maxComponents=240)
  hogMatrix = cv.PCAProject(hogMatrix, mean, eigenVectors)
  PCAMeanOutput = pokemon + 'PCA_Mean.joblib'
  dump(mean, PCAMeanOutput)
  PCAEigenOutput = pokemon + 'PCA_Eigen.joblib'
  dump(eigenVectors, PCAEigenOutput)
  return hogMatrix

# Toggle to create new hogMatrix for each Pokemon
'''
hogMatrix0 = HOG_PCA_Matrix(np.concatenate((pikachuTrainingData, pikachuTestingData), axis=None), labelVector[0])
hogMatrix1 = HOG_PCA_Matrix(np.concatenate((bulbasaurTrainingData, bulbasaurTestingData), axis=None), labelVector[1])
hogMatrix2 = HOG_PCA_Matrix(np.concatenate((charmanderTrainingData, charmanderTestingData), axis=None), labelVector[2])
hogMatrix3 = HOG_PCA_Matrix(np.concatenate((squirtleTrainingData, squirtleTestingData), axis=None), labelVector[3])
'''

# Returns an array the correct labels for the dataset
def generateLabels(dataset, pokemon):
  labels = np.full((dataset.shape), pokemon)
  return labels

# These are our Support Vector Machines, and will be fed data from our HOG Descriptor
# Toggle to create SVMs from scratch, but then comment out the SVM loads
'''
svm0 = SVM.OneClassSVM(kernel="rbf", gamma=0.5)
svm1 = SVM.OneClassSVM(kernel="rbf", gamma=0.5)
svm2 = SVM.OneClassSVM(kernel="rbf", gamma=0.5)
svm3 = SVM.OneClassSVM(kernel="rbf", gamma=0.5)
'''

svm0 = load('pikachuSVM.joblib')
svm1 = load('bulbasaurSVM.joblib')
svm2 = load('charmanderSVM.joblib')
svm3 = load('squirtleSVM.joblib')

# Toggle to train the SVMs from scratch
'''
#The svm training marathon/montage begins here. Get yourself some popcorn:

svm0.fit(hogMatrix0, generateLabels(pikachuTrainingData, labelVector[0]))
svm1.fit(hogMatrix1, generateLabels(bulbasaurTrainingData, labelVector[1]))
svm2.fit(hogMatrix2, generateLabels(charmanderTrainingData, labelVector[2]))
svm3.fit(hogMatrix3, generateLabels(squirtleTrainingData, labelVector[3]))

# Save the SVMs for later use

dump(svm0, 'pikachuSVM.joblib')
dump(svm1, 'bulbasaurSVM.joblib')
dump(svm2, 'charmanderSVM.joblib')
dump(svm3, 'squirtleSVM.joblib')
'''

# Toggle to how the SVMs compare to the testing set
'''
# Testing the SVMs and viewing their results

numOfTestingData = len(hogMatrix0[240:300])

print(labelVector[0])
pikachuPredictions = svm0.predict(hogMatrix0[240:300])
pikachuScores = svm0.score_samples(hogMatrix0[240:300])
for i in range(numOfTestingData):
  print(i+1, pikachuPredictions[i], pikachuScores[i])

print(labelVector[1])
bulbasaurPredictions = svm1.predict(hogMatrix1[240:300])
bulbasaurScores = svm1.score_samples(hogMatrix1[240:300])
for i in range(numOfTestingData):
  print(i+1, bulbasaurPredictions[i], bulbasaurScores[i])

print(labelVector[2])
charmanderPredictions = svm2.predict(hogMatrix2[240:300])
charmanderScores = svm2.score_samples(hogMatrix2[240:300])
for i in range(numOfTestingData):
  print(i+1, charmanderPredictions[i], charmanderScores[i])

print(labelVector[3])
squirtlePredictions = svm3.predict(hogMatrix3[240:300])
squirtleScores = svm3.score_samples(hogMatrix3[240:300])
for i in range(numOfTestingData):
  print(i+1, squirtlePredictions[i], squirtleScores[i])

'''


# Final Test to see which Pokemon should be selected for individual images

testImgURL = "kanto_starters.jpg"
#             ^ replace with the actual test image from camera
#bulbasaurTestingData[30] <-- if you wanted to test from testing set instead

testImg = cv.imread(testImgURL)
testImg = cv.resize(testImg, (IMG_SIZE, IMG_SIZE))
cv.imshow(testImgURL, testImg)
cv.waitKey(0)
cv.destroyAllWindows()

# Run this image through HOG and PCA for each Pokemon
testImgHOG = hog.compute(testImg, winSize)
testImgHOG = testImgHOG.transpose()

# Returns the hog-pca matrix based on the input Pokemon
def pokePCA(hogMatrix, pokemon):
  PCA_Mean = load(pokemon + 'PCA_Mean.joblib')
  PCA_Eigen = load(pokemon + 'PCA_Eigen.joblib')
  pca = cv.PCAProject(hogMatrix, PCA_Mean, PCA_Eigen)
  return pca

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
  finalAnswer = "Ditto" # this means the testImg was neither class

print('Final Prediction:', finalAnswer)

