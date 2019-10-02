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


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     last_frame = get_current_frame()
#


def run_mouse_tracking_program(User_name, objetive, ):


begin = time.time()

user_name = 'Anderson Nelson'
survey_objective = 'True'

x_coord = []
y_coord = []

name_list = []
time_list = []

survey_objective_list = []

time_since_list = []

while True:
    new_frame = get_current_frame()
    x_value = new_frame.position[0]
    y_value = new_frame.position[1]

    x_coord.append(x_value)
    y_coord.append(y_value)

    name_list.append(user_name)
    survey_objective_list.append(survey_objective)

    print('Compiled new coordinate mouse coordinate.....')

    time.sleep(0.5)
    print('Appended mouse coordinates to mouse_tracking data....')

mouse_tracking = pd.DataFrame(
    {'User Name': name_list,
     'Survey Object': survey_objective_list,
     'x_coord': x_coord,
     'y_coord': y_coord
     }
)

# save as a csv
mouse_tracking.to_csv('mouse_tracking_anderson.csv')
