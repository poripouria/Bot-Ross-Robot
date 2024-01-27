import numpy as np
from scipy.spatial.distance import euclidean, cityblock
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageDraw, ImageFont
from queue import Queue, PriorityQueue
import heapq
from itertools import product, permutations

class BotRoss():
    """
    Bot Ross Object
    """

    def __init__(self):
        pass

Board_Size = [200, 200] # 20cm × 20cm (In BRPixel format)

def Integrator(input_image, output_size, method='fit'):
    """
    Integrates the image
        Image types and sizesare different.
        This function receives different types of image and return unique type and size.
    Args:
        input_image: Image in grayscale
        output_size: Size of the board
        method: Fit or Fill for resizing
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

    threshold = (100, 100)
    if image.shape <= threshold:
        return image

    print(f'Image size before: {image.shape}')
    if method == 'fit':
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
    elif method == 'fill':
        final_image = cv2.resize(image, (output_size[0], output_size[1]), fx=1, fy=1, interpolation= cv2.INTER_NEAREST) 
    else:
        raise ValueError("Invalid method for resizing Image")
    print(f'Image size AFTER: {final_image.shape}') 
    return final_image

def convert_to_binary(img):
    """
    Converts the image to binary
    Args:
        img: Image
    Returns:
        Binary image
    """
    
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]
    
    return binary_image

def text_to_image(txt="Hello, I am Bot Ross.", fnt='./assets/fonts/Seven Segment.ttf'):
    """
    Converts text to image
    Args:
        txt: Text to be converted
        fnt: Font of Text
    Returns:
        Image
    """

    if 60 < len(txt):
        print('Text is too long')
        txt = txt[:60] + " ..."
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
    font = ImageFont.truetype(fnt, int(Board_Size[1]/5))
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

    def add_node(x, y):
        v = f'v{x}_{y}'
        if v not in graph:
            graph[v] = set()

    def add_edge(x1, y1, x2, y2):
        v1 = f'v{x1}_{y1}'
        v2 = f'v{x2}_{y2}'
        if v1 not in graph:
            graph[v1] = set()
        if v2 not in graph:
            graph[v2] = set()
        graph[v1].add(v2)
        graph[v2].add(v1)

    rows, cols = bin_img.shape
    graph = {}

    for x in range(rows):
        for y in range(cols):
            if bin_img[x, y] == 0:
                add_node(x, y)
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        if 0 <= i < rows and 0 <= j < cols and bin_img[i, j] == 0:
                            if i != x or j != y:
                                add_node(i, j)
                                add_edge(x, y, i, j)

    with open('./logs/output-graph-logger.txt', 'w') as file:
        file.write(str(graph))

    return graph

def find_spanning_trees(graph, by):
    """
    Finds spanning trees for each connected component in the graph
    Args:
        graph: Graph (dictionary)
        by: Method to find spanning trees
    Returns:
        List of spanning trees (subgraphs) with edges
    """

    def dfs(start, spanning_tree):
        stack = [start]
        while stack:
            current_node = stack.pop()
            if current_node not in visited:
                visited.add(current_node)
                spanning_tree['nodes'].add(current_node)
                for neighbor in sorted(graph.get(current_node, [])):
                    if neighbor not in visited:
                        spanning_tree['edges'].append((current_node, neighbor))
                        stack.append(neighbor)

            # current_node = stack.pop()
            # spanning_tree['nodes'].add(current_node)
            # for neighbor in sorted(graph.get(current_node, [])):
            #     if neighbor not in visited:
            #         visited.add(neighbor)
            #         stack.append(neighbor)
            #         spanning_tree['edges'].append((current_node, neighbor))

    def recursive_dfs(start, spanning_tree):
        visited.add(start)
        spanning_tree['nodes'].add(start)
        for neighbor in sorted(graph.get(start, [])):
            if neighbor not in visited:
                spanning_tree['edges'].append((start, neighbor))
                recursive_dfs(neighbor, spanning_tree)

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

    def tsp(start, spanning_tree):
        stack = [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                spanning_tree['nodes'].add(node)
                for neighbor in graph.get(node, []):
                    if neighbor not in visited:
                        stack.append(neighbor)
                        spanning_tree['edges'].append((node, neighbor))

    def astar(start, spanning_tree):
        priority_queue = [(0, start)]
        while priority_queue:
            _, current_node = heapq.heappop(priority_queue)
            if current_node not in spanning_tree['nodes']:
                visited.add(current_node)
                spanning_tree['nodes'].add(current_node)
                neighbors = [(neighbor, cityblock(list(map(int, current_node[1:].split('_'))), list(map(int, neighbor[1:].split('_'))))) for neighbor in graph.get(current_node, [])]
                for neighbor, distance in neighbors:
                    if neighbor not in spanning_tree['nodes']:
                        heapq.heappush(priority_queue, (distance, neighbor))
                        spanning_tree['edges'].append((current_node, neighbor))

    methods = {'dfs': dfs,
               'recursive_dfs': recursive_dfs,
               'bfs': bfs,
               'tsp': tsp,
               'astar': astar}
    visited = set()
    spanning_trees = []
    for node in graph:
        if node not in visited:
            spanning_tree = {'nodes': set(), 'edges': []}
            try:
                method = methods[by]
                method(node, spanning_tree)
            except KeyError:
                raise ValueError('Invalid method of find_spanning_trees')
            spanning_trees.append(spanning_tree)
    with open('./logs/output-graph-st-logger.txt', 'w') as file:
        file.write(str(spanning_trees))

    return spanning_trees

def painter(bin_img):
    """
    Paints the image on a whiteboard using a simulated cable-driven painter robot
    Args:
        bin_img: Image in binary
    Returns:
        Nothing (Draw and Writes the sequence of (x, y, z) points to a file)
    """

    graph = image_to_graph(bin_img)
    spanning_trees = find_spanning_trees(graph, 'recursive_dfs')
    init_pos = [0, 0]

    with open('./logs/painting-simulator-logger.txt', 'w') as file:
        robot_position = init_pos
        for idx, spanning_tree in enumerate(spanning_trees):
            file.write(f"Painting Segment {idx + 1}:\n")

            nodes = spanning_tree['nodes']
            nodes = [list(map(int, node[1:].split('_'))) for node in nodes]
            nearest_node = min(nodes, key=lambda node: cityblock(robot_position, node))
            x, y = nearest_node
            file.write(f"Mv to ({x}, {y})\n")
            robot_position = nearest_node

            edges = spanning_tree['edges']
            if not edges:
                file.write(f"Dr fr ({x}, {y}) to ({x}, {y})\n")
            for edge in edges:
                x_start, y_start = map(int, edge[0][1:].split('_'))
                x_end, y_end = map(int, edge[1][1:].split('_'))
                if robot_position != [x_start, y_start]:
                    file.write(f"Mv to ({x_start}, {y_start})\n")
                file.write(f"Dr fr ({x_start}, {y_start}) to ({x_end}, {y_end})\n")
                robot_position = [x_end, y_end]

def main(Args=None):

    def algorithm_tester():
        # test_image = cv2.imread("./assets/images/test/image.png")
        # test_image = text_to_image("Pouria")
        # test_image = np.array([[0, 0, 1, 0, 1],
        #                        [0, 0, 1, 1, 0],
        #                        [1, 0, 1, 1, 1],
        #                        [0, 1, 1, 1, 1],
        #                        [1, 1, 1, 1, 0]])
        # test_image = np.array([[0, 1, 1, 1, 1],
        #                        [1, 0, 1, 1, 1],
        #                        [1, 1, 0, 1, 1],
        #                        [1, 1, 1, 0, 1],
        #                        [1, 1, 1, 1, 0]])
        # test_image = np.array([[0, 1, 0, 1, 0],
        #                        [0, 1, 0, 1, 0],
        #                        [0, 1, 0, 1, 0],
        #                        [0, 1, 0, 1, 0],
        #                        [0, 1, 0, 1, 0]])
        # test_image = np.array([[1, 1, 1, 1, 1],
        #                        [1, 0, 0, 0, 1],
        #                        [1, 0, 1, 0, 1],
        #                        [1, 0, 0, 0, 1],
        #                        [1, 1, 1, 1, 1]])
        # test_image = np.array([[0, 0, 0, 0, 1, 1],
        #                        [1, 0, 0, 0, 1, 1],
        #                        [0, 0, 0, 0, 0, 0],
        #                        [1, 1, 1, 1, 1, 1],
        #                        [0, 0, 0, 0, 0, 0],
        #                        [1, 1, 0, 1, 1, 1],
        #                        [0, 0, 0, 0, 0, 0]])
        # test_image = np.array([[1, 1, 1, 1, 1, 1],
        #                        [1, 0, 0, 0, 0, 1],
        #                        [1, 0, 1, 1, 0, 1],
        #                        [1, 0, 0, 0, 0, 1],
        #                        [1, 0, 0, 1, 1, 1],
        #                        [1, 0, 1, 0, 1, 1],
        #                        [1, 0, 1, 1, 0, 1]])
        test_image = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
                               [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
                               [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                               [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                               [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                               [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                               [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
                               [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
        Integrated_test_image = Integrator(test_image, Board_Size, method='fit')
        binary_test_image = convert_to_binary(Integrated_test_image)

        painter(binary_test_image)
        plt.imshow(cv2.cvtColor(binary_test_image, cv2.COLOR_BGR2RGB))
        plt.show()

    algorithm_tester()

if __name__ == "__main__":
    main()
