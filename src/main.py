from painter import *
import time
import re

class BotRoss():
    """
    Bot Ross Object
    """

    def __init__(self):
        pos = (0, 0, 0)
        
def cmd_sender(simulator='./logs/painting-simulator-logger.txt'):
    """
    Generator function to read the logger file and yield the commands for ino server
    """
    pattern = re.compile(r' fr \((\d+), (\d+)\) to \((\d+), (\d+)\)')

    with open(simulator, 'r') as file:
        lines = file.readlines()

    for line in lines:
        cmd = ""
        if line.startswith('Painting Segment'):
            continue
        if line.startswith('EOF'):
            yield "000"
            break
        elif line.startswith('Mv') or line.startswith('Dr'):

            if line.startswith('Dr'):
                cmd += "1"
            if line.startswith('Mv'):
                cmd += "0"

            x1, y1, x2, y2 = map(int, pattern.search(line).groups())
            # print(x1, x2, y1, y2)
            dx = x2 - x1
            dy = y2 - y1
            if dx < 0:
                cmd += "+"
            elif dx > 0:
                cmd += "-"
            else:
                cmd += "0"
            if dy < 0:
                cmd += "+"
            elif dy > 0:
                cmd += "-"
            else:
                cmd += "0"
        else:
            raise ValueError("Something went wrong in simulator file!")

        # milliseconds = 100
        # time.sleep(milliseconds / 1000.0)
        yield cmd
        
def main(Args=None):
    test_image = cv2.imread("./assets/images/test/circle2.png")
    # test_image = text_to_image()
    # test_image = np.array([[0, 1, 0, 1, 0, 1],
    #                        [0, 0, 0, 1, 0, 1],
    #                        [0, 0, 0, 1, 0, 1],
    #                        [0, 1, 0, 1, 0, 1],
    #                        [0, 1, 0, 1, 0, 1]])

    algorithm(test_image)
    commands = list(cmd_sender())
    # print(commands)
    with open('./logs/commands-logger.txt', 'w') as f:
        f.write(f'char str[{len(commands)}][4] =' + ' {')
        for i, cmd in enumerate(commands):
            f.write(f'\"{cmd}\", ') if i < len(commands)-1 else f.write(f'\"{cmd}\"' + '};')

    #TODO: Add Pruning function to Prune the Graph which is extracted feom binary image

if __name__ == "__main__":
    main()