import numpy as np
import cv2

# global variables
initial_pos = []  # initial position of image that will be moved to math the other one perfectly
target_pos = []  # target pos on the other image


def high_pass_filter(img, kernel_size = 21, sigma = 3):
    return img - cv2.GaussianBlur(img, (kernel_size, kernel_size), sigma) + 125  # add a number between 100 and 150 to change the color values to gray

def low_pass_filter(img, kernel_size = 21, sigma = 3):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), sigma)


# create hybrid using high and lowpass filter on 2 images
def create_hybrid_img(hp_img, lp_img, gamma, weight = 0.5):
    return cv2.addWeighted(high_pass_filter(hp_img), weight, low_pass_filter(lp_img), 1-weight, gamma)  # using weight to define which image is displayd stronger



def click_high_pass_img(event, x, y, flags, param):
    global initial_pos
    #work on new image
    curr_img = param.copy()
    if event == cv2.EVENT_LBUTTONDOWN: 
        # if the left mouse button was clicked, save selected point on img in the array
        pos = len(initial_pos)
        if(pos == 0):
            initial_pos = [(x, y)]
        else:
            initial_pos.append((x, y))
        #draw and show circle around picked point 
        cv2.circle(curr_img, (x,y), 10, 255, 5)
        cv2.imshow('original_01', curr_img)
     
def click_low_pass_img(event, x, y, flags, param):
    global target_pos
    #work on new image
    curr_img = param.copy()
    if event == cv2.EVENT_LBUTTONDOWN: 
        # if the left mouse button was clicked, save selected point on img in the array
        pos = len(target_pos)
        if(pos == 0):
            target_pos = [(x, y)]
        else:
            target_pos.append((x, y))
        #draw and show circle around picked point 
        cv2.circle(curr_img, (x,y), 10, 255, 5)
        cv2.imshow('original_02', curr_img)
      


def translate_high_pass_img(img):
    global target_pos, initial_pos
    # reference: Tutorial 12 
    # warp the high_pass_img to fit the low_pass_img according to the selected points
    T_translation = cv2.getAffineTransform(np.float32(initial_pos), np.float32(target_pos))
    return cv2.warpAffine(img, T_translation, (img.shape[1], img.shape[0])) 




def main():
    global target_pos, initial_pos

    # load images
    low_pass_img = cv2.imread('src/tiger.jpg')
    high_pass_img = cv2.imread('src/cat.jpg')
    # low_pass_img = cv2.imread('src/f.jpg')
    # high_pass_img = cv2.imread('src/m.jpg')
    # low_pass_img = cv2.imread('src/joe_biden.jpg')
    # high_pass_img = cv2.imread('src/barack_obama.jpg')
    # low_pass_img = cv2.imread('src/mona_lisa.jpg')
    # high_pass_img = cv2.imread('src/girl_with_pearl_earring.jpg')
    
    # resize images
    low_pass_img = cv2.resize(low_pass_img, (600,600)) 
    high_pass_img = cv2.resize(high_pass_img, (600,600))

    print("Pick exactly three points on each picture. For the best result, select eyes and mouth on each face")
    # show original images
    cv2.imshow('original_01', high_pass_img)
    cv2.setMouseCallback('original_01', click_high_pass_img, param = high_pass_img)   # callbacks beeing used to select translation between images
    cv2.imshow('original_02', low_pass_img)
    cv2.setMouseCallback('original_02', click_low_pass_img, param = low_pass_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # check if there are exactly three points in each array. If not, return out of the main function
    if(len(target_pos) != 3 & len(initial_pos) != 3):
        target_pos = []
        initial_pos = []
        print("Too few or too many points selected, please restart the program and try again")
        return

    # translate the image that is going to be filtered by a high pass filter
    high_pass_img = translate_high_pass_img(high_pass_img)
    
    # show result (hybrid) image 
    cv2.imshow('hybrid image', create_hybrid_img(high_pass_img, low_pass_img, 1))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()