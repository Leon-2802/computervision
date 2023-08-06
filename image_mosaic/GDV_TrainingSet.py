import cv2
import numpy as np
from pathlib import Path
import glob
from enum import Enum
import pickle


class Descriptor(Enum):
    """Define available descriptors"""

    TINY_GRAY4, TINY_GRAY8, TINY_COLOR4, TINY_COLOR8, COLOR32 = range(5)

    """ Compute the descriptor vector """

    def compute(self, img):
        if self is Descriptor.TINY_GRAY4:
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return np.ravel(cv2.resize(img_gray, (4, 4)))

        if self is Descriptor.TINY_GRAY8:
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return np.ravel(cv2.resize(img_gray, (8, 8)))

        if self is Descriptor.TINY_COLOR4:
            return np.ravel(cv2.resize(img, (4, 4)))

        if self is Descriptor.TINY_COLOR8:
            return np.ravel(cv2.resize(img, (8, 8)))

        if self is Descriptor.COLOR32:
            return np.ravel(cv2.resize(img, (32, 32)))

    """ Get the length of the descriptor vector """

    def getSize(self):
        if self is Descriptor.TINY_GRAY4:
            return 4 * 4

        if self is Descriptor.TINY_GRAY8:
            return 8 * 8

        if self is Descriptor.TINY_COLOR4:
            return 4 * 4 * 3

        if self is Descriptor.TINY_COLOR8:
            return 8 * 8 * 3

        if self is Descriptor.COLOR32:
            return 32 * 32 * 3


class TrainingSet:
    """Create and manage the image data set used as training data"""

    def __init__(self, root_path) -> None:
        self.root_path = root_path

    # compute a descriptor for all images and store the data
    def createTrainingData(self, descriptor=Descriptor.TINY_GRAY4):
        print("Start creating the training data:")
        if isinstance(descriptor, Descriptor):
            print("Used descriptor: ", descriptor.name)
            self.descriptor = descriptor
        else:
            print("ERROR: No correct descriptor set. Pick one:")
            for d in Descriptor:
                print(d.name)
            return

        self.categories = []
        self.img_files = []
        self.responses = []
        self.num_training_images = 0
        tempData = []
        tempResponses = []
        category_index = 0.0
        # read all available categories
        print("Found categories:")
        for path in Path(self.root_path).iterdir():
            if path.is_dir():
                self.categories.append(path.name)
                category_index += 1.0
                # for each category
            num_files_in_category = 0
            for file in glob.glob(str(path) + "/*.jpg"):
                # print(file)
                # create response array
                tempResponses.append([category_index])
                # load image
                img = cv2.imread(file, cv2.IMREAD_COLOR)
                # compute image descriptors and store them
                tempData.append(self.descriptor.compute(img))
                self.num_training_images += 1
                num_files_in_category += 1
                self.img_files.append(file)
            print("Found %d files in %s" % (num_files_in_category, path.name))

        self.trainData = np.ndarray(
            shape=(self.num_training_images, self.descriptor.getSize()),
            buffer=np.float32(np.array(np.ravel(tempData))),
            dtype=np.float32,
        )
        self.responses = np.ndarray(
            shape=(self.num_training_images, 1),
            buffer=np.float32(np.ravel(tempResponses)),
            dtype=np.float32,
        )
        print(
            "Training succeeded: computed descriptors for %d images"
            % self.num_training_images
        )

    # save the training data to a file
    def saveTrainingData(self, file_name):
        self.file_name = file_name
        np.savez(
            file_name,
            categories=self.categories,
            num_images=self.num_training_images,
            responses=self.responses,
            trainData=self.trainData,
            img_files=self.img_files,
            descriptor=self.descriptor.name,
        )
        print("Saved training data to file:", self.file_name)
        print("Number of images: ", self.num_training_images)
        print("Used descriptor:", self.descriptor)

    # load the training data from a file
    def loadTrainingData(self, file_name):
        data = np.load(file_name, allow_pickle=True)
        self.responses = data["responses"]
        self.trainData = data["trainData"]
        self.categories = data["categories"]
        self.img_files = data["img_files"]
        self.num_training_images = data["num_images"]
        descriptor_name = data["descriptor"]
        if str(descriptor_name) == "TINY_GRAY4":
            self.descriptor = Descriptor.TINY_GRAY4
        elif str(descriptor_name) == "TINY_GRAY8":
            self.descriptor = Descriptor.TINY_GRAY8
        elif str(descriptor_name) == "TINY_COLOR4":
            self.descriptor = Descriptor.TINY_COLOR4
        elif str(descriptor_name) == "TINY_COLOR8":
            self.descriptor = Descriptor.TINY_COLOR8
        elif str(descriptor_name) == "COLOR32":
            self.descriptor = Descriptor.COLOR32
        else:
            print("ERROR: Unknown descriptor")
        print("Loaded training data:")
        print("Number of images: ", self.num_training_images)
        print("Used descriptor:", self.descriptor)

    def getFilenameFromIndex(self, index):
        return self.img_files[index]

    def loadCifar10(self, batch_file, meta_file):
        with open(meta_file, "rb") as fo:
            meta_data = pickle.load(fo, encoding="bytes")
        self.categories = meta_data[b"label_names"]
        self.num_training_images = meta_data[b"num_cases_per_batch"]
        with open(batch_file, "rb") as fo:
            dict = pickle.load(fo, encoding="bytes")
        self.descriptor = Descriptor.COLOR32
        tempData = dict[b"data"]
        tempResponses = np.array(dict[b"labels"])
        self.trainData = np.ndarray(
            shape=(self.num_training_images, self.descriptor.getSize()),
            buffer=np.float32(np.array(np.ravel(tempData))),
            dtype=np.float32,
        )
        self.responses = np.ndarray(
            shape=(self.num_training_images, 1),
            buffer=np.float32(np.ravel(tempResponses)),
            dtype=np.float32,
        )
        self.img_files = dict[b"filenames"]
        print("Loaded CIFAR-10 training data:")
        print("Number of images: ", self.num_training_images)
        print("Used descriptor:", self.descriptor)
        print("Categories:", self.categories)

    def loadCifar10all(self, batch_files, meta_file):
        num_batches = len(batch_files)
        with open(meta_file, "rb") as fo:
            meta_data = pickle.load(fo, encoding="bytes")
        self.categories = meta_data[b"label_names"]
        self.num_training_images = meta_data[b"num_cases_per_batch"] * num_batches

        # initialize trainData and responses
        tempData = []
        tempResponses = []
        self.img_files = []
        # go through each batch
        for batch_file in batch_files:
            with open(batch_file, "rb") as fo:
                dict = pickle.load(fo, encoding="bytes")
            self.descriptor = Descriptor.COLOR32
            tempData.append(dict[b"data"])
            tempResponses.append(np.array(dict[b"labels"]))
            self.img_files.append(dict[b"filenames"])

        self.trainData = np.ndarray(
            shape=(self.num_training_images, self.descriptor.getSize()),
            buffer=np.float32(np.array(np.ravel(tempData))),
            dtype=np.float32,
        )
        self.responses = np.ndarray(
            shape=(self.num_training_images, 1),
            buffer=np.float32(np.ravel(tempResponses)),
            dtype=np.float32,
        )
        print("Loaded CIFAR-10 training data:")
        print("Number of images: ", self.num_training_images)
        print("Used descriptor:", self.descriptor)
        print("Categories:", self.categories)

    def testCifar(self, window_title, index):
        """Test visually if the data is loaded correctly"""
        test_img = np.uint8(np.reshape(self.trainData[index, 0:1024], (32, 32)))
        cv2.imshow(window_title, test_img)
        cv2.waitKey(0)

    def trainWeights(self, loss_function):
        foo = "tbd"
        # TODO initialize weight matrix W and bias b

        # TODO compute loss for whole data set or just one batch?

        # TODO compute gradients and update W
