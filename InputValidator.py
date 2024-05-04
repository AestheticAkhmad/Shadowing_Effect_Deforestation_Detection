from DataHolder import DataHolder

import re
from datetime import datetime

class InputValidator:
    def __init__(self) -> None:
        self.data_holder = DataHolder()
        self.roi = dict()

    def ValidateInput(self, input_roi, date_from, date_to):
        roi_valid, error_msg1 = self.ValidateROI(input_roi)
        dates_valid, error_msg2 = self.ValidateDates(date_from, date_to)

        if roi_valid and dates_valid:
            self.data_holder.date_from = date_from
            self.data_holder.date_to = date_to
            self.data_holder.roi = self.roi

            return True, error_msg1 + error_msg2

        return False, error_msg1 + error_msg2 

    def ValidateROI(self, input_roi):
        longitude_pattern_we = r'^(-?(?:180(?:\.0{1,6})?|\d{1,2}(?:\.\d{1,6})?))$'
        latitude_pattern_ns = r'^(-?(?:90(\.0{1,6})?|\b(?:[0-8]?[0-9](?:\.\d{1,6})?|90(?:\.0{1,6})?)\b))$'
        error_msg = ""
        roi_valid = True

        if not re.match(longitude_pattern_we, input_roi['west']):
            error_msg = "-> Input for [west] is invalid.\n"
            roi_valid = False
        if not re.match(latitude_pattern_ns, input_roi['south']):
            error_msg += "-> Input for [south] is invalid.\n"
            roi_valid = False
        if not re.match(longitude_pattern_we, input_roi['east']):
            error_msg += "-> Input for [east] is invalid.\n"
            roi_valid = False
        if not re.match(latitude_pattern_ns, input_roi['north']):
            error_msg += "-> Input for [north] is invalid.\n"
            roi_valid = False

        if not roi_valid:
            return False, error_msg

        west = float(input_roi['west'])
        south = float(input_roi['south'])
        east = float(input_roi['east'])
        north = float(input_roi['north'])
        if west >= east:
            error_msg += "-> [east] input must be greater than [west].\n"
            roi_valid = False
        if south >= north:
            error_msg += "-> [north] input must be greater than [south].\n"
            roi_valid = False

        if roi_valid:
            self.roi['west'] = west
            self.roi['south'] = south
            self.roi['east'] = east
            self.roi['north'] = north

            error_msg = "-> ROI input is valid.\n"
            return True, error_msg
        
        return False, error_msg

    def ValidateDates(self, date_from, date_to):
        try:
            dt1 = datetime.strptime(date_from, '%Y-%m-%d')
            dt2 = datetime.strptime(date_to, '%Y-%m-%d')

            if dt1 >= dt2:
                return False, "-> Date [from] must be before date [to].\n"

            return True, "-> All dates are valid.\n"
        
        except ValueError:
            return False, "-> Dates must be in YYYY-MM-DD format.\n"
        