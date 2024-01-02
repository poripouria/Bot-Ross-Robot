import numpy as np
import cv2
from PIL import Image

# A function for Integration and assimilation of inputs
def Integrator(input_image, output_size=[3508, 2480]):
    """
    Integrates the image
        Image types are different for example some of them have 3 channels, some of them are simple 2D arrays with 0-255 values, and so many other types.
        Also They may have different sizes
        This function receives different types of image and return unique type and size.
    Args:
        image: Image in grayscale
    Returns:
        Integrated image
    """
    
    if isinstance(input_image, str):
        image = cv2.imread(input_image)
    elif isinstance(input_image, np.ndarray):
        image = input_image
    elif isinstance(input_image, Image.Image):
        image = np.array(input_image)
    elif input_image is None:
        raise ValueError("Image not found")
    else:
        raise ValueError("Unsupported image input type")

    # Fit image in output_size rectangle
    ratio = min(output_size[0] / image.shape[0], output_size[1] / image.shape[1])
    print(ratio)
    print(image.shape)
    image = cv2.resize(image, (0, 0), fx=ratio, fy=ratio)
    print(image.shape)

    return image


def convert_to_binary(img):
    """
    Converts the image to binary
    Args:
        image: Image in grayscale
    Returns:
        Binary image
    """
    
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)[1]

    # # Check if black_pixels > white_pixels reverse them
    # black_pixels = cv2.countNonZero(binary_image)
    # total_pixels = binary_image.shape[0] * binary_image.shape[1]
    # white_pixels = total_pixels - black_pixels
    # if black_pixels > white_pixels:
    #     binary_image = cv2.bitwise_not(binary_image)
    
    return binary_image

def painter(bin_img):

    # Create a white image (oneslike matrix) with the same size as bin_img
    white_img = np.ones_like(bin_img) * 255

def algorithm_tester():

    test_image = cv2.imread("./assets/images/test/test-img.png") # text-art.jpg
    Integrated_test_image = Integrator(test_image)
    binary_test_image = convert_to_binary(test_image)
    painter(binary_test_image)

    cv2.imshow("Binary Image", binary_test_image)
    cv2.waitKey(0)

algorithm_tester()
