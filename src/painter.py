import numpy as np
import cv2
from scipy.spatial.distance import euclidean
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
        # Handle Image channels
        if len(input_image.shape) == 2:
            # image = np.reshape(input_image, (input_image.shape[0], input_image.shape[1], 3))
            if input_image.dtype == 'int32':
                input_image = cv2.convertScaleAbs(input_image) 
            image = cv2.cvtColor(input_image, cv2.COLOR_GRAY2RGB)
        else:
            image = input_image
    elif isinstance(input_image, Image.Image):
        image = np.array(input_image)
    elif input_image is None:
        raise ValueError("Image not found")
    else:
        raise ValueError("Unsupported image input type")

    # Fit image in output_size rectangle
    min_threshold = 200
    if image.shape[0] < min_threshold or image.shape[1] < min_threshold:
        return image
    else:
        ratio = min(output_size[0] / image.shape[0], output_size[1] / image.shape[1])
        print(ratio)
        final_image = cv2.resize(image, (0, 0), fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)

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
        v1 = f'v{x1}_{y1}'
        v2 = f'v{x2}_{y2}'
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
    print(graph)

    return graph

def find_spanning_trees(graph):
    """
    Finds spanning trees for each connected component in the graph
    Args:
        graph: Graph (dictionary)
    Returns:
        List of spanning trees (subgraphs) with edges
    """
    visited = set()
    spanning_trees = []

    def dfs(node, spanning_tree):
        visited.add(node)
        spanning_tree['nodes'].add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                spanning_tree['edges'].append((node, neighbor))
                dfs(neighbor, spanning_tree)

    for node in graph:
        if node not in visited:
            spanning_tree = {'nodes': set(), 'edges': []}
            dfs(node, spanning_tree)
            spanning_trees.append(spanning_tree)
    print(spanning_trees)

    return spanning_trees

def painter(bin_img, output_file='botross-painting-simulator.txt'):
    """
    Paints the image on a whiteboard using a simulated cable-driven painter robot
    Args:
        bin_img: Image in binary
        output_file: File to save the simulation output
    Returns:
        Nothing (Writes the sequence of (x, y, z) points to a file)
    """

    def find_nearest_node(robot_position, nodes):
        return min(nodes, key=lambda node: euclidean(robot_position, node))

    # Find the spanning trees
    graph = image_to_graph(bin_img)
    spanning_trees = find_spanning_trees(graph)

    # Initial position of the robot
    robot_position = [0, 0]

    # Simulate the painting process for each spanning tree
    with open(output_file, 'w') as file:
        for idx, spanning_tree in enumerate(spanning_trees):
            file.write(f"Painting Segment {idx + 1}:\n")

            # Get the nodes and edges for the current spanning tree
            nodes = spanning_tree['nodes']
            edges = spanning_tree['edges']

            # Find the nearest node and move to it
            nodes = [list(map(int, node[1:].split('_'))) for node in nodes]
            nearest_node = find_nearest_node(robot_position, nodes)
            x, y = nearest_node
            z = 0 if bin_img[x, y] == 0 else 1
            file.write(f"Move to ({x}, {y}, {z})\n")

            # Update the robot's position
            robot_position = nearest_node

            # Simulate the robot's drawing along the edges
            for edge in edges:
                start, end = edge
                x_start, y_start = map(int, start[1:].split('_'))
                x_end, y_end = map(int, end[1:].split('_'))
                file.write(f"Draw from ({x_start}, {y_start}) to ({x_end}, {y_end})\n")

def main(Args=None):

    def algorithm_tester():
        test_image = cv2.imread("./assets/images/test/test-img.png")
        test_image = text_to_image()
        # test_image = np.array([[1, 0, 1, 0],
        #                        [1, 0, 0, 1],
        #                        [1, 1, 1, 1],
        #                        [0, 0, 1, 1]])
        # test_image = np.array([[0, 1, 0, 1, 0],
        #                        [0, 1, 0, 1, 0],
        #                        [0, 1, 0, 1, 0],
        #                        [0, 1, 0, 1, 0],
        #                        [0, 1, 0, 1, 0]])
        test_image = np.array([[1, 1, 1, 1, 1],
                               [1, 0, 0, 0, 1],
                               [1, 0, 0, 0, 1],
                               [1, 0, 0, 0, 1],
                               [1, 1, 1, 1, 1]])
        Integrated_test_image = Integrator(test_image)
        binary_test_image = convert_to_binary(Integrated_test_image)
        plt.imshow(cv2.cvtColor(binary_test_image, cv2.COLOR_BGR2RGB))
        plt.show()
        painter(binary_test_image, output_file='.\logs\painting-simulator-logger.txt')

    algorithm_tester()

if __name__ == "__main__":
    main()
