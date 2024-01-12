import numpy as np
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageDraw, ImageFont
from queue import Queue
from itertools import product

class BotRoss():
    """
    Bot Ross Object
    """
    def __init__(self):
        pass

Board_Size = [300, 200] # 30cm × 20cm (In BRPixel format)

def Integrator(input_image, output_size=Board_Size):
    """
    Integrates the image
        Image types and sizesare different.
        This function receives different types of image and return unique type and size.
    Args:
        input_image: Image in grayscale
    Returns:
        Integrated image
    """
    
    if isinstance(input_image, str):
        image = cv2.imread(input_image)
    elif isinstance(input_image, np.ndarray):
        if len(input_image.shape) == 2:
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

    if image.shape <= (100, 100):
        return image

    print(f'Image size before: {image.shape}')
    # Fit to Board_Size
    if image.shape[0] >= output_size[1] and image.shape[1] <= output_size[0]:
        scale = output_size[1] / image.shape[0]
    elif image.shape[1] >= output_size[0] and image.shape[0] <= output_size[1]:
        scale = output_size[0] / image.shape[1]
    elif image.shape[1] <= output_size[0] and image.shape[0] <= output_size[1]:
        scale = min(output_size[0] / image.shape[1], output_size[1] / image.shape[0])
    else:
        scale = min(image.shape[0] / output_size[1], image.shape[1] / output_size[0])
    print(f'Scaling Ratio: {scale}')
    final_image = cv2.resize(image, None, fx=scale, fy=scale, interpolation= cv2.INTER_NEAREST) 
    # Fill in Board_Size
    # final_image = cv2.resize(image, (output_size[0], output_size[1]), fx=1, fy=1, interpolation= cv2.INTER_NEAREST) 
    print(f'Image size AFTER: {final_image.shape}') 
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

    if 60 < len(txt):
        print('Text is too long')
        txt = txt[:60]
    if 15 < len(txt) <= 30:
        for i in range(15, len(txt)):
            if txt[i] == ' ':
                txt = txt[:i] + '\n' + txt[i+1:]
    if 30 < len(txt) <= 60:
        for i in range(30, len(txt)):
            if txt[i] == ' ':
                txt = txt[:i] + '\n' + txt[i+1:]
    img = Image.new('RGB', (Board_Size[0], Board_Size[1]), (255, 255, 255))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("./assets/fonts/Seven Segment.ttf", int(Board_Size[1]/5))
    d.text((int(Board_Size[0]/100), int(Board_Size[1]/150)), txt, font=font, fill=(0,0,0))
    img = np.array(img)

    return img

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
            if bin_img[x, y] == 0:
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        if is_valid(i, j) and bin_img[i, j] == 0 and (i != x or j != y):
                            add_edge(x, y, i, j)

    print(graph)

    return graph

def find_spanning_trees(graph, by='bfs'):
    """
    Finds spanning trees for each connected component in the graph
    Args:
        graph: Graph (dictionary)
    Returns:
        List of spanning trees (subgraphs) with edges
    """

    visited = set()
    spanning_trees = []

    if by == 'dfs':
        def dfs(node, spanning_tree):
            visited.add(node)
            spanning_tree['nodes'].add(node)
            for neighbor in sorted(graph.get(node, [])):
                if neighbor not in visited:
                    spanning_tree['edges'].append((node, neighbor))
                    dfs(neighbor, spanning_tree)

        for node in graph:
            if node not in visited:
                spanning_tree = {'nodes': set(), 'edges': []}
                dfs(node, spanning_tree)
                spanning_trees.append(spanning_tree)
        print(spanning_trees)

    elif by == 'bfs':
        def bfs(start, spanning_tree):
            visited.add(start)
            queue = Queue()
            queue.put(start)

            while not queue.empty():
                current_node = queue.get()
                spanning_tree['nodes'].add(current_node)

                for neighbor in graph.get(current_node, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.put(neighbor)
                        spanning_tree['edges'].append((current_node, neighbor))
        
        for node in graph:
            if node not in visited:
                spanning_tree = {'nodes': set(), 'edges': []}
                bfs(node, spanning_tree)
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

    robot_position = [0, 0]
    graph = image_to_graph(bin_img)
    spanning_trees = find_spanning_trees(graph, 'bfs')

    with open(output_file, 'w') as file:
        for idx, spanning_tree in enumerate(spanning_trees):
            file.write(f"Painting Segment {idx + 1}:\n")

            nodes = spanning_tree['nodes']
            edges = spanning_tree['edges']

            nodes = [list(map(int, node[1:].split('_'))) for node in nodes]
            nearest_node = find_nearest_node(robot_position, nodes)

            x, y = nearest_node
            file.write(f"Move to ({x}, {y})\n")
            robot_position = nearest_node

            for edge in edges:
                start, end = edge
                x_start, y_start = map(int, start[1:].split('_'))
                x_end, y_end = map(int, end[1:].split('_'))
                file.write(f"Draw from ({x_start}, {y_start}) to ({x_end}, {y_end})\n")
                robot_position = [x_end, y_end]

def main(Args=None):

    def algorithm_tester():
        
        # test_image = cv2.imread("./assets/images/test/test-img.png")
        # test_image = text_to_image()
        # test_image = np.array([[1, 0, 1, 0],
        #                        [1, 0, 0, 1],
        #                        [1, 1, 1, 1],
        #                        [0, 0, 1, 1]])
        # test_image = np.array([[0, 1, 0, 1, 0],
        #                        [0, 1, 0, 1, 0],
        #                        [0, 1, 0, 1, 0],
        #                        [0, 1, 0, 1, 0],
        #                        [0, 1, 0, 1, 0]])
        # test_image = np.array([[1, 1, 1, 1, 1],
        #                        [1, 0, 0, 0, 1],
        #                        [1, 0, 0, 0, 1],
        #                        [1, 0, 0, 0, 1],
        #                        [1, 1, 1, 1, 1]])
        test_image = np.array([[1, 1, 1, 1, 1, 1],
                               [0, 0, 0, 0, 0, 0],
                               [1, 1, 1, 1, 1, 1],
                               [0, 0, 0, 0, 0, 0],
                               [1, 1, 1, 1, 1, 1],
                               [0, 0, 0, 0, 0, 0]])

        Integrated_test_image = Integrator(test_image)
        binary_test_image = convert_to_binary(Integrated_test_image)
        painter(binary_test_image, output_file='./logs/painting-simulator-logger.txt')
        plt.imshow(cv2.cvtColor(binary_test_image, cv2.COLOR_BGR2RGB))
        plt.show()

    algorithm_tester()

if __name__ == "__main__":
    main()
