from GDV_TrainingSet import Descriptor, TrainingSet
import cv2
import numpy as np


def findBestMatch(trainData, sample, choice):
    # do the matching with FLANN
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(trainData.trainData, sample, k=1)
    # Sort by their distance.
    matches = sorted(matches, key=lambda x: x[0].distance)
    bestMatch = matches[choice][0]
    return bestMatch.queryIdx


""" Define and compute or load the training data """
root_path = "./data/101_ObjectCategories/"  # adjust this path if you have the files in some other folder
# root_path = './data/temp/'  # you can use a smaller subset of the training data during development to save time
file_name = "./data/data.npz"
trainData = TrainingSet(root_path)

trainData.loadTrainingData(file_name)


def search_fitting_img(img, choice):
    # assure that the same descriptor is used by reading it from the training data set
    assert isinstance(trainData.descriptor, Descriptor)
    descr = trainData.descriptor
    newcomer = np.ndarray(
        shape=(1, descr.getSize()),
        buffer=np.float32(descr.compute(img)),
        dtype=np.float32,
    )
    idx = findBestMatch(trainData, newcomer, choice)
    best_matching_img = cv2.imread(
        trainData.getFilenameFromIndex(idx), cv2.IMREAD_COLOR
    )

    return best_matching_img
