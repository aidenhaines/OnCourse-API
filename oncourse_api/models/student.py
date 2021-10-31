from datetime import date
from typing import List

from .assignment import OverviewAssignment
from .group import Class

class Student:
    """ Make the organization better for student """
    def __init__(self, student: dict, school_id: int, school_year_id: int, request_session):
        self.first_name = student["first_name"]
        self.last_name = student["last_name"]
        self.email = student["email"]
        self.phone = student["phone"]
        self.street_address1 = student["street_address1"]
        self.street_address2 = student["street_address2"]
        self.city = student["city"]
        self.state = student["state"]
        self.postal_code = student["postal_code"]
        self.grade_level = student["grade_level"]
        self.school_name = student["school"]
        self.id = student["id"]
        self.school_id = school_id
        self.school_year_id = school_year_id
        self.requestSession = request_session
        self.classes = self.__getClasses()
        self.assignments = self.__getAssignments()
        """ Returns Assignments in a list. Going back 7 days """
        self.student_portrait = f"https://www.oncourseconnect.com/json.axd/file/image?app=STUDENT_PORTRAITS&id={self.id}"
        self.reportCard = self.reportCard()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        

    def reportCard(self) -> dict:
        url = f"https://www.oncourseconnect.com/api/classroom/grades/report_cards?schoolId={self.school_id}&schoolYearId={self.school_year_id}&studentId={self.id}"
        report_card = (self.requestSession.get(url)).json()
        return report_card

    def getAttendence(self) -> dict:
        url = f"https://www.oncourseconnect.com/api/classroom/attendance/attendance_summary?schoolId={self.school_id}&schoolYearId={self.school_year_id}&studentId={self.id}"
        attendance = (self.requestSession.get(url)).json()
        return attendance

    def __getClasses(self) -> List['Class']:
        url = f"https://www.oncourseconnect.com/json.axd/classroom/lms/classes/list_student_groups?showAll=N&studentId={self.id}"
        classes = (self.requestSession.get(url)).json()
        return [Class(c, self.id, self.requestSession) for c in classes]

    def __getAssignments(self) -> List['OverviewAssignment']:
        today = date.today()
        startDate:str = str(today.month) + "/" + str(today.day - 7) + "/" + str(today.year)
        endDate:str = str(today.month) + "/" + str(today.day) + "/" + str(today.year + 1)
        url = f"https://www.oncourseconnect.com/json.axd/classroom/lms/assignments/get_student_work_due?endDate={endDate}&startDate={startDate}&studentId={self.id}"
        assignments = (self.requestSession.get(url)).json()
        return [OverviewAssignment(a, self.requestSession) for a in assignments]
