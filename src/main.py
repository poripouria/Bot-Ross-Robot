from painter import *
import re
import sys
import time
from pySerialTransfer import pySerialTransfer as txfer
        
sys.setrecursionlimit(2000)
        
def cmd_logger(simulator='./logs/painting-simulator-logger.txt'):
    """
    Generator function to read the logger file
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

        yield cmd
        
def cmd_sender(commands):
    """
    yield the commands for ino server
    """

    link = txfer.SerialTransfer('COM3')
    link.open()
    time.sleep(2) # allow some time for the Arduino to completely reset

    for cmd in commands:
        send_size = 0   
        str_size = link.tx_obj(cmd, send_size) - send_size
        send_size += str_size

        link.send(str_size)

        while not link.available():
            if link.status < 0:
                if link.status == txfer.CRC_ERROR:
                    print('ERROR: CRC_ERROR')
                elif link.status == txfer.PAYLOAD_ERROR:
                    print('ERROR: PAYLOAD_ERROR')
                elif link.status == txfer.STOP_BYTE_ERROR:
                    print('ERROR: STOP_BYTE_ERROR')
                else:
                    print('ERROR: {}'.format(link.status))

        rec_cmd   = link.rx_obj(obj_type=type(cmd),
                                obj_byte_size=str_size,
                                start_pos=0)


def main(Args=None):
    test_image = cv2.imread("./assets/images/test/text-art.jpg")
    # test_image = text_to_image("K-P")
    # test_image = np.array([[0, 1, 0, 1, 0, 1],
    #                        [0, 0, 0, 1, 0, 1],
    #                        [0, 0, 0, 1, 0, 1],
    #                        [0, 1, 0, 1, 0, 1],
    #                        [0, 1, 0, 1, 0, 1]])

    algorithm(test_image)

    commands = list(cmd_logger())
    # cmd_sender(commands)

    with open('./logs/commands-logger.txt', 'w') as f:
        f.write(f'char str[{len(commands)}][4] =' + ' {')
        for i, cmd in enumerate(commands):
            f.write(f'\"{cmd}\", ') if i < len(commands)-1 else f.write(f'\"{cmd}\"' + '};')

if __name__ == "__main__":
    main()
