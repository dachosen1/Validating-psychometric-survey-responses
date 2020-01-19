import math
import sys
import time
from datetime import date

import pandas as pd
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication


def distance(x1, y1, x2, y2):
    """
    Calculates the euclidean distance between two vectors.

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


class Frame:
    """
    The purpose of this class is to replicate the mouse movement done by the Dotin team in oder to discover patterns in
    user who are falsely filling out survey questions.

    The document contains  a series of function to return coordinates, speed, and direction of mouse movements.

    """

    def __init__(self, position, time_):
        self.position = position
        self.time = time_

    def speed(self, frame):
        """
        Calculates  the speed from a coordinate

        :param frame: coordinate arrays
        :return: single value that represents the speed of the
        """

        d = distance(*self.position, *frame.position)
        time_delta = abs(frame.time - self.time)
        if time_delta == 0:
            return None
        else:
            return d / time_delta


""""
Mouse movement tracker 
The purpose of program is to track the mouse movements of team alpha taking the dotin survey. 
Step 1: Run the below script and type your name, survey objective, and survey part 
Step 2: The program will start to record mouse movement
Step 3: Once your done taking the survey, click the stop button on jupyter notebook 
Step 4: Run the mouse tracking PD data frame, and save it as a CSV
Note: Restart the Kernel and Clear the output after each run
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)

    user_name = input('Please type your name')
    survey_objective = input('Please type the survey objective: Accurate or False')
    survey_part = input('Please indcate which part of the survey you are taking')

    x_coord = []
    y_coord = []

    name_list = []
    time_list = []

    date_today = date.today()
    survey_objective_list = []
    time_since_list = []

    begin = time.time()

    while True:
        try:
            new_frame = get_current_cursor_position()
            x_value = new_frame[0]
            y_value = new_frame[1]

            x_coord.append(x_value)
            y_coord.append(y_value)

            current_time = time.time()
            time_since = current_time - begin

            time_since_list.append(time_since)

            time.sleep(0.5)
            print('Appended mouse coordinates to mouse_tracking data....')
        except KeyboardInterrupt:
            break

    mouse_tracking = pd.DataFrame(
        {'User Name': user_name,
         'Date': date_today,
         'Survey Object': survey_objective,
         'x_coord': x_coord,
         'y_coord': y_coord,
         'Time Since': time_since_list,
         'Survey Part': survey_part
         }
    )

    # save as a csv
    mouse_tracking.to_csv(f'../Data/Team Survey Data/mouse_tracking_{user_name}_{survey_objective}_{survey_part}.csv')
