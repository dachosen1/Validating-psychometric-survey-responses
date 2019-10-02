import math
import time

from PyQt5.QtGui import QCursor


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
        Calculates the euclidean distance between two vectors.

        #TODO: Document function

        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return: Integer class object that represents the euclidean distance.
        """

        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def get_current_cursor_position():
        """
        Function that returns coordinates of cursor position on screen.

        :return x and y coordinate of cursor position:
        """
        pos = QCursor.pos()
        return pos.x(), pos.y()

    def get_current_frame():
        return Frame(get_current_cursor_position(), time.time())
