import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

class BotRoss():
    """
    Bot Ross Object
    """
    def __init__(self):
        pass

A3_paper_size = [3508, 2480]

# A function for Integration and assimilation of inputs
def Integrator(input_image, output_size=A3_paper_size):
    """
    Integrates the image
        Image types are different for example some of them have 3 channels, some of them are simple 2D arrays with 0-255 values, and so many other types.
        Also They may have different sizes
        This function receives different types of image and return unique type and size.
    Args:
        input_image: Image in grayscale
    Returns:
        Integrated image
    """
    
    # Handle Input
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
    final_image = cv2.resize(image, (0, 0), fx=ratio, fy=ratio)

    return final_image


def convert_to_binary(img):
    """
    Converts the image to binary
    Args:
        img: Image in grayscale
    Returns:
        Binary image
    """
    
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)[1]
    
    return binary_image

def text_to_image(txt="Hello, I am Bot Ross."):
    """
    Converts text to image
    Args:
        txt: Text
    Returns:
        Image
    """
    img = Image.new('RGB', (A3_paper_size[0], A3_paper_size[1]), (255, 255, 255))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("./assets/fonts/Seven Segment.ttf", 300)
    d.text((100,100), txt, font=font, fill=(0,0,0))

    return np.array(img)
    

def painter(bin_img):
    """
    Paints the image on whiteboard
    Args:
        bin_img: Image in binary
    Returns:
        Nothig (Paint)
    """

    # Create a white image (oneslike matrix) with the same size as bin_img
    white_img = np.ones_like(bin_img) * 255

def main(Args=None):

    def algorithm_tester():

        # test_image = cv2.imread("./assets/images/test/test-img.png")
        test_image = text_to_image()
        Integrated_test_image = Integrator(test_image)
        binary_test_image = convert_to_binary(Integrated_test_image)
        painter(binary_test_image)

        plt.imshow(Integrated_test_image)
        plt.show()

    algorithm_tester()

if __name__ == "__main__":
    main()
