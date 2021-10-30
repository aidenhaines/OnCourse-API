
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

#{"lms_assign_id":2124527,"assignment_name":"CLASSWORK: Aperture Practice","group_name":"Digital Photography 04","assignment_description":"Complete both Aperture Tasks<br /><br />Put the photos in separate folders in your Shared Photo Folder<br /><br />Label them:<br /><br />Aperture Task 1<br />Aperture Task 2<br /><br />Mark as Done in On Course and they will be checked for credit.","due_date":"10/29/2021 11:59:00 PM","weight":"","external_guid":"a7827916-e84e-abe7-db73-42dcb608aa38","allow_resume":"Y","question_count":0,"late_assignment_mode":"M","grade_column":"","non_calculated":"N","view_column":"Allow_Submission","assessment_session":"","lms_lti_tool_id":"","lms_lti_tool_icon":"","lms_lti_tool_name":"","lms_lti_tool_embeddable":"","is_missing":"N","student_section_entry_date":"9/7/2021"}
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
        