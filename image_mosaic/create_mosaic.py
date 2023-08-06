import GDV_ImageRetrieval
import cv2
import numpy as np


src_img = cv2.imread("images/buddha.jpg", cv2.IMREAD_COLOR)
cv2.imshow("source image", src_img)

name_for_saved_img = "mosaic"

# values for interating over image
# size of tiles of source image (for every tile, a fitting image will be searched)
src_img_tile_size = 2
# size of tiles on the mosaic image (for small images it is better to enlargen the tiles for the mosaic image)
mosaic_img_tile_size = 4
# how much bigger is the mosaic image compared to the source image
mosaic_img_scale = int(mosaic_img_tile_size / src_img_tile_size)

# counter used for showing the progress
counter = 0

number_of_steps = (src_img.shape[1] / src_img_tile_size) * (
    src_img.shape[0] / src_img_tile_size
)

mosaic_image = np.zeros(
    (src_img.shape[0] * mosaic_img_scale, src_img.shape[1] * mosaic_img_scale, 3),
    np.uint8,
)


# gives visual feedback for the computation progress
def progress_bar(progress, total):
    percent = 100 * (progress / total)
    bar = "$" * int(percent) + "-" * (100 - int(percent))
    if percent > 100:
        percent = 100
    print(f"\r|{bar}| {percent:.2f}%", end="\r")


# resizes the passed image to the size of the tiles in the mosaic and puts it at the current position of the loop
def addImageToMosaic(img, mosaic_x, mosaic_y):
    cutout = mosaic_image[
        mosaic_y : mosaic_y + mosaic_img_tile_size,
        mosaic_x : mosaic_x + mosaic_img_tile_size,
    ]

    img_resized = cv2.resize(
        img, [cutout.shape[1], cutout.shape[0]], interpolation=cv2.INTER_AREA
    )
    mosaic_image[
        mosaic_y : mosaic_y + cutout.shape[0], mosaic_x : mosaic_x + cutout.shape[1]
    ] = img_resized


lastImg = src_img
allImgs = []

# checks if given image is already neighbor
def noNeighbor(fitting, pos):

    return not (
        (
            fitting.shape == allImgs[pos - 1].shape
            and not (np.bitwise_xor(fitting, allImgs[pos - 1]).any())
        )
        or (
            pos >= src_img.shape[0] / src_img_tile_size
            and fitting.shape
            == allImgs[pos - int(src_img.shape[0] / src_img_tile_size)].shape
            and not (
                np.bitwise_xor(
                    fitting, allImgs[pos - int(src_img.shape[0] / src_img_tile_size)]
                ).any()
            )
        )
    )


# intitalize progress bar
progress_bar(0, number_of_steps)

# iterate over image with the steps being equal to the tile_size
# for each step a tile gets taken from the src_img, the best fitting image is found in GDV_ImageRetrieval and is added to the mosaic
# the second index is for the mosaic image tiles, as they have a different size as the tiles of the src image

pos = 0
for x, m_x in zip(
    range(0, src_img.shape[1], src_img_tile_size),
    range(0, mosaic_image.shape[1], mosaic_img_tile_size),
):

    for y, m_y in zip(
        range(0, src_img.shape[0], src_img_tile_size),
        range(0, mosaic_image.shape[0], mosaic_img_tile_size),
    ):
        partOfImg = src_img[y : y + src_img_tile_size, x : x + src_img_tile_size]
        choice = 0
        fitting = GDV_ImageRetrieval.search_fitting_img(partOfImg, choice)
        if x > 0 or y > 0:

            while not noNeighbor(fitting, pos):
                fitting = GDV_ImageRetrieval.search_fitting_img(partOfImg, choice)
                choice += 1

        allImgs.append(fitting)

        addImageToMosaic(fitting, m_x, m_y)
        pos += 1
        counter += 1
        progress_bar(counter, number_of_steps)


cv2.imshow("result", mosaic_image)
cv2.imwrite("output/{}.jpg".format(name_for_saved_img), mosaic_image)
print("finished")
cv2.waitKey(0)
