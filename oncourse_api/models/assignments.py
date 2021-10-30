
from datetime import datetime


class Assignment:
    """ Assignment """
    def __init__(self, assignment_dict, request_session):
        self.requestSession = request_session
        self.type = assignment_dict['assignment_type']
        self.id = assignment_dict['assignment_id']
        self.name = assignment_dict['assignment_name']
        self.class_id = assignment_dict['group_id']
        self.class_name = assignment_dict['group_name']
        self.due_date = assignment_dict['due_date']
        # self.due_date_utc = assignment_dict['due_date_utc']
        self.late_assignment_mode = assignment_dict['late_assignment_mode']
        self.rrule = assignment_dict['rrule']
        self.recurrence_end = assignment_dict['recurrence_end']
        self.is_missing = assignment_dict['is_missing']
        self.color = assignment_dict['color']
        self.color_hex = assignment_dict['color_hex']
        self.is_late = self.__is_late()

    def __is_late(self) -> bool:
        """
        Returns True if assignment is late
        """
        due_date = datetime.strptime(self.due_date, '%m/%d/%Y %I:%M:%S %p')
        now = datetime.now()
        if due_date < now:
            return True
        else:
            return False
        