from datetime import datetime, timedelta
from typing import List

from .assignment import OverviewAssignment
from .group import Class


class Student:
    """Make the organization better for student"""

    def __init__(self, student: dict, school_id: int, school_year_id: int, active_profile, request_session):
        self.__active_profile = active_profile
        self.first_name: str = student.get("first_name")
        self.last_name: str = student.get("last_name")
        self.email: str = student.get("email")
        self.phone: str = student.get("phone")
        self.street_address1 = student.get("street_address1") if student.get("street_address1") != "" else None
        self.street_address2 = student.get("street_address2") if student.get("street_address2") != "" else None
        self.city = student.get("city") if student.get("city") != "" else None
        self.state = student.get("state") if student.get("state") != "" else None
        self.postal_code = student.get("postal_code") if student.get("postal_code") != "" else None
        self.grade_level = student.get("grade_level") if student.get("grade_level") != "" else None
        self.school_name = student.get("school") if student.get("school") != "" else None
        self.id: int = student.get("id")
        self.school_id = school_id
        self.school_year_id = school_year_id
        self.requestSession = request_session
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

    @property
    def attendance(self) -> dict:
        # TODO Make model
        url = f"https://www.oncourseconnect.com/api/classroom/attendance/attendance_summary?schoolId={self.school_id}&schoolYearId={self.school_year_id}&studentId={self.id}"
        attendance = (self.requestSession.get(url)).json()
        return attendance

    @property
    def classes(self) -> List["Class"]:
        """Returns a list of Class objects"""
        url = f"https://www.oncourseconnect.com/json.axd/classroom/lms/classes/list_student_groups?showAll=N&studentId={self.id}"
        classes = (self.requestSession.get(url)).json()
        return [Class(c, self.id, self.requestSession) for c in classes]

    @property
    def assignments(self) -> List["OverviewAssignment"]:
        """Returns list of overview assignments"""
        day = datetime.now()
        start_time = datetime.strftime(
            day - timedelta(days=self.__active_profile.classroom_todo_start_date_span), "%m/%d/%Y"
        )  # start date is 1 week back
        end_time = datetime.strftime(day + timedelta(days=365), "%m/%d/%Y")  # add 1 year in future
        url = f"https://www.oncourseconnect.com/json.axd/classroom/lms/assignments/get_student_work_due?endDate={end_time}&startDate={start_time}&studentId={self.id}"
        assignments = (self.requestSession.get(url)).json()
        return [OverviewAssignment(a, self.requestSession) for a in assignments]

    @property
    def other_student_data(self) -> List["OtherStudentData"]:
        url = f"https://www.oncourseconnect.com/api/classroom/dataelement/student_data_elements?studentId={self.id}"
        other_student_data = (self.requestSession.get(url)).json()

        return [self.OtherStudentData(d) for d in other_student_data.get("data")]

    class OtherStudentData:
        def __init__(self, other_student_data: dict):
            self.label = other_student_data.get("label")
            self.sort_pos = other_student_data.get("sort_pos")
            self.data_val = other_student_data.get("data_val")
            self.last_modified_date = other_student_data.get("last_modified_date")
            self.column = other_student_data.get("column")

        def __repr__(self):
            return f"{self.label}:{self.data_val}"

        def __str__(self):
            return f"{self.label}:{self.data_val}"
