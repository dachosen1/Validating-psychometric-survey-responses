import math
import sys
import time
from datetime import datetime

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication


class Frame:
    """
    The purpose of this class is to replicate the mouse movement done by the Dotin team in oder to discover patterns in
    user who are falsely filling out survey questions.

    The document contains  a series of function to return coordinates, speed, and direction of mouse movements.

    """

    # TODO: document function

    def __init__(self, position, time):
        self.position = position
        self.time = time

    def speed(self, frame):
        """
        #TODO: document function
        Function that returns the speed from a coordinate

        :param frame:
        :return:
        """

        d = distance(*self.position, *frame.position)
        time_delta = abs(frame.time - self.time)
        if time_delta == 0:
            return None
        else:
            return d / time_delta


def distance(x1, y1, x2, y2):
    """
    #TODO: Document function

    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_current_cursor_position():
    # TODO: document function:
    pos = QCursor.pos()
    return pos.x(), pos.y()


def get_current_frame():
    return Frame(get_current_cursor_position(), time.time())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    last_frame = get_current_frame()
    begin = datetime.now()

    Name = input()
    Intention = input()

    while True:
        new_frame = get_current_frame()
        print(datetime.now(), new_frame.position)

        time.sleep(1)

# TODO: Write function that saves mouse movements in a csv file with users name
