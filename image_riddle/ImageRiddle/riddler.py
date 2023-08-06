
import cv2
from random import randrange

#--------------------(image, ammount of images/abstraction ,size of copied chunk)
def change_pixel_random(_img, _repetitions, _chunk_size):

    randomised_img = _img
    img_width = _img.shape[1]
    img_height = _img.shape[0]
    size = (img_width, img_height)

    #repetitions define the amount of randomisation and images produced
    for round in range(_repetitions):
        #randomises image chunk wise
        for i in range(0,10000):

            #Chosing random x/y koords. located in the img 
            random_x = randrange(img_width - _chunk_size)
            random_y = randrange(img_height - _chunk_size)
            random_x_final = randrange(img_width - _chunk_size)
            random_y_final = randrange(img_height - _chunk_size)
            
            #copies random chunk of pixels based on randomX/randomY
            random_chunk = randomised_img[random_y:random_y + _chunk_size, random_x:random_x + _chunk_size]

            #paste random chunk at a random position (randomX2/randomY2)
            randomised_img[random_y_final:random_y_final + _chunk_size,
                           random_x_final:random_x_final + _chunk_size] = random_chunk
          
        #Saving the randomised img every repetition
        save_img(randomised_img)
           
    save_vid('random_pixel.mp4', size)



def blurr_image(_img, _end_kernel, _kernel_steps):

    img_width = _img.shape[1]
    img_height = _img.shape[0]
    size = (img_width, img_height)

    for k_size in range(1, _end_kernel, _kernel_steps):
        #GaussianBlur(img_src, size of kernel (size of area affected by blurr), sigmaX, sigmaY (both for kernel deviation in x/y direction))
        blurred_image = cv2.GaussianBlur(_img, (k_size,k_size), 0, 0)
        save_img(blurred_image)

    save_vid('blurred_image.mp4', size)



def hide_part_of_image(_img, _increment):

    img_width = _img.shape[1]
    img_height = _img.shape[0]
    size = (img_width, img_height)
    # first save the original image, so we can put i at the end of the video
    save_img(_img)

    for height in range(0, img_height, _increment):

        hidden_image = _img
        for i in range(height):
            for j in range(img_width):
                hidden_image[i][j] = [0, 0, 0]

        # only save images that cover at least 1/4 of the image in black (would be too easy to solve when less than a fourth is hidden)
        if height * 2 >= (img_height * 0.5):
            save_img(hidden_image)
        
    save_vid('hidden_image.mp4', size)
                


#reusable function to save the steps for the video as images:
count = 0
def save_img(_img):

    global count
    dest = "ImageRiddle\output\{}.jpg".format(count)
    cv2.imwrite(dest, _img)
    count += 1



#resuable function to save the videos for the diferent riddles:
def save_vid(name, size):
    out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'mp4v'), 1, size)
    # goes in reverse order through the pictures, bc all functions that change the pictures add the original first and end with the most changed picture
    # starts at count - 1, bc the count is incrmented after each saveImg iteration -> last image is one index lower the the count value
    # ends before -1, to also include index=0
    for i in range((count - 1), -1, -1):
        out.write(cv2.imread("ImageRiddle\output\{}.jpg".format(i), cv2.IMREAD_ANYCOLOR))
    out.release()




# load images and call functions:
image_1 = cv2.imread("ImageRiddle\data\C5_highlight_front_3.jpg", cv2.IMREAD_ANYCOLOR)
image_2 = cv2.imread("ImageRiddle\data\Olaf_Scholz_In_March_2022.jpg", cv2.IMREAD_ANYCOLOR)
image_3 = cv2.imread("ImageRiddle/data/tiger.jpg", cv2.IMREAD_ANYCOLOR)

# change_pixel_random(image1, 30, 3)

# blurr_image(image2, 500, 24)

# hide_part_of_image(image3, 20)
