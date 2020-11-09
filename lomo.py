"""
Author:     Cody Hawkins
Class:      CS5420
Project:    Assignment 5
File:       lomo.py
Desc:       lomography and vignette combined filter with option to save
"""
import getopt
import sys
import os
import cv2 as cv
import numpy as np
import math
from search import file_search


def help():
    print("\t\t----HELP----")
    print("Give filename to create a picture with lomography and vignette features")
    print("Press q to quit")
    print("Press s to save image")


def color(x):
    # make callback a pass so that color_callback function can return image
    pass


def halo(x):
    # make callback a pass so that halo_callback function can return window name and image
    pass


def color_callback(val, image):
    s = val / 100

    if s < 0.08:
        return image

    if s >= 0.08:
        B, G, R = cv.split(image)
        LUT = [0 for x in range(256)]
        LUT = np.array(LUT)
        R2 = np.zeros((R.shape[0], R.shape[1]), dtype="uint8")

        for i in range(256):
            # create look up table to enhance light and dark colors of red channel
            x = (i / 256)
            LUT[i] = np.round(256 * (1 / (1 + pow(math.e, -((x - 0.5) / s)))))

        # change values of original red channel from look up table
        for i in range(R.shape[0]):
            for j in range(R.shape[1]):
                R2[i][j] = LUT[R[i][j]]

        result = cv.merge((B, G, R2))
        return result


def halo_callback(val, image, name):
    radius = 100
    radius = radius - val
    output = np.copy(image)
    halo = None
    # 2d array of 32 bit floats set to 0.75 and then create a circle mask of size radius
    halo = np.full((image.shape[0], image.shape[1], 3), 0.75, dtype=np.float32)
    radius = min(image.shape[0], image.shape[1]) * (radius / 200)
    halo = cv.circle(halo, (image.shape[0] // 2, image.shape[1] // 2), int(radius), (1, 1, 1), -1)
    halo = cv.blur(halo, (int(radius), int(radius)))

    # change 8 bit channel of input image to 32 bit float
    output = output.astype(np.float32)
    # multiply image with vignette mask
    result = output * halo
    # convert result back to 8 bit image and return image and window name
    result = result.astype(np.uint8)
    return name, result


def show_image(args):
    image = args[0]
    search_directory = "C:\\Users\\codyh\\PycharmProjects\\DIP2\\test"
    image_path = file_search(image, search_directory)
    window_name = "Lomography.jpg"
    track_1 = "color"
    track_2 = "halo"

    try:
        img = cv.imread(image_path)
        cv.namedWindow(window_name)
        # create trackbars for image and fill with pass functions
        cv.createTrackbar(track_1, window_name, 1, 20, color)
        cv.createTrackbar(track_2, window_name, 0, 100, halo)
        if img is not None:
            while True:
                # get position of slider values
                slide_val_1 = cv.getTrackbarPos(track_1, window_name)
                slide_val_2 = cv.getTrackbarPos(track_2, window_name)
                # if slider value gets to 100 an error occurs so once value hits 100
                # immediately set slider value to 99
                if slide_val_2 == 100:
                    slide_val_2 = 99
                # feed image from color_callback to halo as input
                output = color_callback(slide_val_1, img)
                win_name, result = halo_callback(slide_val_2, output, window_name)
                cv.imshow(win_name, result)
                key = cv.waitKey(10)
                if key == 113:
                    print("Program has successfully exited")
                    break
                elif key == 115:
                    # save image to current working directory
                    try:
                        current = os.getcwd()
                        current = os.path.join(current, win_name)
                        cv.imwrite(current, result)
                        print(f"{win_name} has been written to {current}")
                    except cv.error as err:
                        print(f"An error has occurred when trying to save image: {err}")
                        sys.exit(1)
                    break
            cv.destroyAllWindows()
    except cv.error as err:
        print(err)
        sys.exit(1)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(1)

    for o, a in opts:
        if o in ("-h", "--help"):
            help()
            sys.exit(1)
        else:
            assert False, "Unhandled Option!"

    if len(args) == 1:
        show_image(args)
    elif len(args) == 0:
        print("Please provide image name!")
        sys.exit(1)
    elif len(args) > 1:
        print("Too many arguments passed! Only image name is needed")
        sys.exit(1)


if __name__ == "__main__":
    main()