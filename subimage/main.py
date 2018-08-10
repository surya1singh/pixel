import itertools as it
from math import sqrt
import numpy as np
from option_parser import OptParser
from PIL import Image, ImageChops
from skimage.feature import match_template

RMS_THRESHOLD = 50


def match_image(parent_image, child_image):
    if parent_image.size[0] >=  child_image.size[0] and parent_image.size[1] >=  child_image.size[1]: # child image should always be smaller or equal
        parent_array = np.array(parent_image.convert(mode = 'L'))
        print('parent_array')
        child_array = np.array(child_image.convert(mode = 'L'))
        print('child_array')
        match_array = match_template(parent_array, child_array)
        match_index = np.unravel_index(np.argmax(match_array), match_array.shape)
        print(match_index)
        # get matching subsection from Parent image (using RGB mode)
        parent_sub_array = np.array(parent_image)[match_index[0]:match_index[0] + child_image.size[0],
                                             match_index[1]:match_index[1] + child_image.size[1]]
        parent_sub_image = Image.fromarray(parent_sub_array, mode = 'RGB')
        # calculate the root-mean-square difference between parent_sub_image and child_image
        h_diff = ImageChops.difference(parent_sub_image, child_image).histogram()
        sum_of_squares = sum(value * ((idx % 256) ** 2) for idx, value in enumerate(h_diff))
        rms = sqrt(sum_of_squares/float(child_image.size[0]*child_image.size[1]))
        print(rms)
        if RMS_THRESHOLD > rms: # add matches to table
            print(f"{kwargs['child']} is subset of {kwargs['parent']}")

def main():
    kwargs = OptParser.parseopts()
    directory = Image.open(kwargs['directory'])
    parent_image = Image.open(kwargs['parent'])
    child_image = Image.open(kwargs['child'])
    print(parent_image.size)
    print(child_image.size)

    if parent_image and not os.path.exists(parent_image):
        print(f'{parent_image} does not exists')
    if child_image and not os.path.exists(child_image):
        print(f'{child_image} does not exists')
    if directory and not os.path.isdir(directory):
        print(f'{directory} does not exists')

    if os.path.exists(parent_image) and os.path.exists(child_image):
        match_image(parent_image, child_image)
    elif os.path.exists(parent_image) and os.path.isdir(directory):
        for dir_child in os.listdir(directory):
            match_image(parent_image, dir_child)
    elif os.path.isdir(directory) and os.path.exists(child_image):
        for dir_parent in os.listdir(directory):
            match_image(dir_parent, child_image)
    elif os.path.isdir(directory):
        for x,y in it.combinations(os.listdir(directory),2):
            if x == y:
                continue
            match_image(x, y)
            match_image(y, x)




if __name__=='__main__':
    main()
