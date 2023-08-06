import cv2
import numpy as np
import time



def convolution(image, kernel):
    """
    This function executes the convolution between `img` and `kernel` using a self-written solution.
    """

    #  Implement your own convolution method
    print("[{ img_conv }]/tRunning self implemented convolution...")

    #Calc half kernel
    offset = kernel.shape[0] // 2;

    image_height = image.shape[1]
    image_width = image.shape[0]


    output = image.copy()
    
    for y in range(offset, image_height - offset):
        for x in range(offset, image_width - offset):
            for k in range(image.shape[2]):
                #Copy pixel coverd by kernel
               mat = image[x - offset:x + offset + 1,
                           y - offset:y + offset + 1,
                           k]

                #Calc and save kernel * partOfImage
               output[x,y,k] = np.sum(kernel * mat) 
            
    return output



def convolution_with_opencv(image, kernel):
    """
    This function executes the convolution between `img` and `kernel` using OpenCV.
    """

    print("[{}]/tRunning OpenCV (filter2D) implementation of a convolution...")

    # Flip the kernel as opencv filter2D function is
    # a correlation not a convolution
    kernel = cv2.flip(kernel, -1)
    # When ddepth=-1, the output image will have the same depth as the source.
    ddepth = -1
    output = cv2.filter2D(image, ddepth, kernel)
    
    return output


def getMSE(I1, I2):
    """
    Get the mean squared error between two images `I1` and `I2`.
    """
    difference_img = np.zeros_like(I1)
    # Convert the images from unsigned 8-bit integers to floats in order to have clearer results
    # Take difference between the images' pixel intensities, square it up and take the sum of all
    error = np.sum((I1.astype('float') - I2.astype('float')) ** 2)
    # Divide the sum of squares by total number of pixels in the image to get the mean of the mean squared error
    error /= float(I1.shape[0] * I2.shape[0])

    for y in range(difference_img.shape[1]):
        for x in range(difference_img.shape[0]):
            for k in range(difference_img.shape[2]):
                difference_img[x, y, k] = (I1[x, y, k] - I2[x, y, k]) **2

    return error, difference_img


def main():
    # Find an appropriate image
    image_name = "./src/surfer.jpg"

    # Load the image.
    image = cv2.imread(image_name, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (500, 400))
    original_image = image.copy()

    
    # Use OpenCV functions to create Gaussian kernel
    kernel_size = 5
    sigma = 7

    kernel1D = cv2.getGaussianKernel(kernel_size, sigma)
    kernel = np.transpose(kernel1D) * kernel1D

    methods = (convolution, convolution_with_opencv)
    results = []

    for method in methods:
        # Start time to calculate computation duration
        start = time.time()
        # Run all methods and store resulting images in an array
        results.append(method(image, kernel))
        # End time after computation
        end = time.time()
        print(
            f"""
        Computing the convolution of '{image_name}' with a resolution of {image.shape[0]} x {image.shape[1]} and a
        kernel size of {kernel.shape[0]} x {kernel.shape[1]} ({end - start}s)
        """,
        )

    # Compare the resulting images
    # Display both images and the difference image
    error_value, difference_img = getMSE(results[0], results[1])
    show_results = np.concatenate((results[0], difference_img, results[1]), axis=1)
    cv2.imshow('left: own convolution method | center: MSE visualized (MSE value: ' + str(round(error_value, 2)) + ') | right: opencv convolution method', show_results)
    cv2.imshow('original image', original_image)

    # print MSE result
    print("MSE:", error_value)

    # Keep windows open until key is pressed and then destroy all windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# This is the default Python style for programs
if __name__ == "__main__":
    main()
