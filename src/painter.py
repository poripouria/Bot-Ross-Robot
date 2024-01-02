import numpy as np
import cv2

# A function for Integration and assimilation of inputs
def Integrator(image):
    """
    Integrates the image
    Image types are different for example some of them have 3 channels, some of them are simple 2D arrays with 0-255 values, and so many other types.
    This function receives different types of image and return unique type.

    Args:
        image: Image in grayscale

    Returns:
        Integrated image
    """
    # Convert input image to a common format
    if isinstance(input_image, str):
        # Assuming input is a file path
        image = cv2.imread(input_image)
    elif isinstance(input_image, np.ndarray):
        # Assuming input is a NumPy array
        image = input_image
    else:
        raise ValueError("Unsupported image input type")

    # Ensure image is in the correct format (e.g., 3 channels)
    if len(image.shape) == 2:
        # Convert grayscale to 3 channels
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    elif image.shape[2] == 1:
        # Convert single-channel to 3 channels
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    return image


def convert_to_binary(image):
    """
    Converts the image to binary

    Args:
        image: Image in grayscale

    Returns:
        Binary image
    """
    
    # If the image is a 3D array, convert it to grayscale
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    return binary_image

def otsu_threshold(image):
    """
    Applies the Otsu's method for image thresholding

    Args:
        image: Image in grayscale

    Returns:
        Binary image
    """

    hist, bins = np.histogram(image, bins=256, range=(0, 256))
    total = np.sum(hist)
    w0 = np.sum(hist[:round((total / 2))])
    w1 = total - w0

    mu0 = np.sum((i * hist[i]) / w0 for i in range(1, 256))
    mu1 = np.sum((i * hist[i]) / w1 for i in range(1, 256))

    var0 = np.sum((i - mu0)**2 * hist[i] for i in range(1, 256))
    var1 = np.sum((i - mu1)**2 * hist[i] for i in range(1, 256))

    thresh = (w0 * var0 + w1 * var1) / (w0 + w1)

    binary_image = image > thresh

    return binary_image

def painter(bin_img):
    # Create a white image (oneslike matrix) with the same size as bin_img
    white_img = np.ones_like(bin_img) * 255

def algorithm_tester():
    test_image = cv2.imread("./assets/test/test-img.png")
    binary_test_image = convert_to_binary(test_image)
    painter(binary_test_image)

algorithm_tester()
