from painter import *

class BotRoss():
    """
    Bot Ross Object
    """

    def __init__(self):
        pos = (0, 0, 0)
        
def cmd_sender(logger: str):
    with open('./logs/painting-simulator-logger.txt', 'r') as file:
        lines = f.readlines()
    cmd = ""
    for line in lines:
        if line.startswith('Painting Segment'):
            continue
        if line == '\n':
            break
        

def main(Args=None):
    # test_image = cv2.imread("./assets/images/test/image.png")
    # test_image = text_to_image()
    test_image = np.array([[0, 0, 1, 0, 1],
                            [0, 0, 1, 1, 0],
                            [1, 0, 1, 1, 1],
                            [0, 1, 1, 1, 1],
                            [1, 1, 1, 1, 0]])
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
    #                        [1, 0, 0, 0, 1],
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
    # test_image = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #                        [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
    #                        [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    #                        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    #                        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    #                        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    #                        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    #                        [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    #                        [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
    #                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
    algorithm(test_image)

if __name__ == "__main__":
    main()