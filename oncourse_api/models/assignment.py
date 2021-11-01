
from datetime import datetime



class OverviewAssignment:
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

    def __str__(self) -> str:
        return f"OverviewAssignment(type={self.type}, id={self.id}, name={self.name}, class_id={self.class_id}, class_name={self.class_name}, due_date={self.due_date}, late_assignment_mode={self.late_assignment_mode}, rrule={self.rrule}, recurrence_end={self.recurrence_end}, is_missing={self.is_missing}, color={self.color}, color_hex={self.color_hex}, is_late={self.is_late})"

    def __repr__(self):
        return f"{self.name}"

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

class ClassAssignment:
    def __init__(self, assignment_dict, request_session):
        self.requestSession = request_session
        self.id = assignment_dict['lms_assign_id']
        self.name = assignment_dict['assignment_name']
        self.class_name = assignment_dict['group_name']
        self.description = assignment_dict['assignment_description']
        self.due_date = assignment_dict['due_date']
        self.weight = assignment_dict['weight']
        self.external_guid = assignment_dict['external_guid']
        self.allow_resume = assignment_dict['allow_resume']
        self.question_count = assignment_dict['question_count']
        
    def __str__(self):
        return f"ClassAssignment(id={self.id}, name={self.name}, class_name={self.class_name}, description={self.description}, due_date={self.due_date}, weight={self.weight}, external_guid={self.external_guid}, allow_resume={self.allow_resume}, question_count={self.question_count})"
    
    def __repr__(self):
        return f"{self.name}"
