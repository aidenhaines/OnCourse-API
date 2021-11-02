from datetime import datetime, timedelta
from typing import List

from .assignment import OverviewAssignment
from .group import Class


class Student:
    """Make the organization better for student"""

    def __init__(self, student: dict, school_id: int, school_year_id: int, request_session):
        self.first_name: str = student["first_name"]
        self.last_name: str = student["last_name"]
        self.email: str = student["email"]
        self.phone: str = student["phone"]
        self.street_address1 = student["street_address1"] if student["street_address1"] != "" else None
        self.street_address2 = student["street_address2"] if student["street_address2"] != "" else None
        self.city = student["city"] if student["city"] != "" else None
        self.state = student["state"] if student["state"] != "" else None
        self.postal_code = student["postal_code"] if student["postal_code"] != "" else None
        self.grade_level = student["grade_level"] if student["grade_level"] != "" else None
        self.school_name = student["school"] if student["school"] != "" else None
        self.id: int = student["id"]
        self.school_id = school_id
        self.school_year_id = school_year_id
        self.requestSession = request_session
        """ Returns Assignments in a list. Going back 7 days """
        self.student_portrait = (
            f"https://www.oncourseconnect.com/json.axd/file/image?app=STUDENT_PORTRAITS&id={self.id}"
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    def getReportCard(self) -> dict:
        # TODO Make model
        url = f"https://www.oncourseconnect.com/api/classroom/grades/report_cards?schoolId={self.school_id}&schoolYearId={self.school_year_id}&studentId={self.id}"
        report_card = (self.requestSession.get(url)).json()
        return report_card

    def getAttendance(self) -> dict:
        # TODO Make model
        url = f"https://www.oncourseconnect.com/api/classroom/attendance/attendance_summary?schoolId={self.school_id}&schoolYearId={self.school_year_id}&studentId={self.id}"
        attendance = (self.requestSession.get(url)).json()
        return attendance

    def getClasses(self) -> List["Class"]:
        """Returns a list of Class objects"""
        url = f"https://www.oncourseconnect.com/json.axd/classroom/lms/classes/list_student_groups?showAll=N&studentId={self.id}"
        classes = (self.requestSession.get(url)).json()
        return [Class(c, self.id, self.requestSession) for c in classes]

    def getAssignments(self) -> List["OverviewAssignment"]:
        """Returns list of overview assignments"""
        day = datetime.now()
        start_time = datetime.strftime(day - timedelta(days=7), "%m/%d/%Y")  # start date is 1 week back
        end_time = datetime.strftime(day + timedelta(days=365), "%m/%d/%Y")  # add 1 year in future
        url = f"https://www.oncourseconnect.com/json.axd/classroom/lms/assignments/get_student_work_due?endDate={end_time}&startDate={start_time}&studentId={self.id}"
        assignments = (self.requestSession.get(url)).json()
        return [OverviewAssignment(a, self.requestSession) for a in assignments]
