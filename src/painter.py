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
        Image types and sizesare different.
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
    binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]
    
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

def image_to_graph(bin_img):
    """
    Converts an image to the graph data structure
    Args:
        bin_img: Image in binary
    Returns:
        Graph
    """
    rows, cols = bin_img.shape
    graph = {}

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols

    def add_edge(x1, y1, x2, y2):
        v1 = f'v{x1}{y1}'
        v2 = f'v{x2}{y2}'
        if v1 not in graph:
            graph[v1] = set()
        graph[v1].add(v2)

    for x in range(rows):
        for y in range(cols):
            if bin_img[x, y] == 0:  # Black pixel
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        if is_valid(i, j) and bin_img[i, j] == 0 and (i != x or j != y):
                            add_edge(x, y, i, j)

    return graph

# Example Usage:
import numpy as np

# Assuming bin_img is a binary image represented as a NumPy array
bin_img = np.array([[1, 1, 0, 0],
                    [0, 0, 1, 1],
                    [1, 1, 1, 1],
                    [0, 0, 1, 1]])

graph = image_to_graph(bin_img)
print(graph)

def find_spanning_trees(graph):
    """
    Finds spanning trees for each connected component in the graph
    Args:
        graph: Graph (dictionary)
    Returns:
        List of spanning trees (subgraphs)
    """
    visited = set()
    spanning_trees = []

    def dfs(node, spanning_tree):
        visited.add(node)
        spanning_tree.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, spanning_tree)

    for node in graph:
        if node not in visited:
            spanning_tree = set()
            dfs(node, spanning_tree)
            spanning_trees.append(sorted(spanning_tree))

    return spanning_trees

# Example Usage:
spanning_trees = find_spanning_trees(graph)
print(spanning_trees)

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

        plt.imshow(binary_test_image)
        plt.show()

    algorithm_tester()

if __name__ == "__main__":
    main()
