from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Dict, List

from attr import define

from oncourse_api.models.base import OncourseObject

import attr
from .assignment import OverviewAssignment
from .group import Class
from .reportcard import ReportCard

if TYPE_CHECKING:
    from oncourse_api.models.active_profile import ActiveProfile


@define()
class Student(OncourseObject):
    """Make the organization better for student"""

    first_name: str = attr.ib(default=None)
    last_name: str = attr.ib(default=None)
    email: str = attr.ib(default=None)
    phone: str = attr.ib(default=None)
    street_address1: str = attr.ib(default=None)
    street_address2: str = attr.ib(default=None)
    city: str = attr.ib(default=None)
    state: str = attr.ib(default=None)
    postal_code: str = attr.ib(default=None)
    grade_level: str = attr.ib(default=None)
    school_name: str = attr.ib(default=None)
    id: int = attr.ib(default=None)
    school_id: int = attr.ib(default=None)
    school_year_id: int = attr.ib(default=None)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    def getReportCard(self) -> ReportCard:
        # TODO Make model
        url = f"https://www.oncourseconnect.com/api/classroom/grades/report_cards?schoolId={self.school_id}&schoolYearId={self.school_year_id}&studentId={self.id}"
        report_card = (self.requestSession.get(url)).json()
        return ReportCard(report_card, self.__active_profile, self.requestSession)
        # return report_card

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
        start_time = datetime.strftime(day - timedelta(days=7), "%m/%d/%Y")  # start date is 1 week back
        end_time = datetime.strftime(day + timedelta(days=365), "%m/%d/%Y")  # add 1 year in future
        url = f"https://www.oncourseconnect.com/json.axd/classroom/lms/assignments/get_student_work_due?endDate={end_time}&startDate={start_time}&studentId={self.id}"
        assignments = (self._active_profile.requestSession.get(url)).json()
        return OverviewAssignment.from_list(assignments, self._active_profile)

    @property
    def other_student_data(self) -> List["OtherStudentData"]:
        url = f"https://www.oncourseconnect.com/api/classroom/dataelement/student_data_elements?studentId={self.id}"
        other_student_data = (self._active_profile.requestSession.get(url)).json()
        return OtherStudentData.from_list(other_student_data.get("data"), self._active_profile)


@define
class OtherStudentData(OncourseObject):
    label = attr.ib(default=None)
    sort_pos = attr.ib(default=None)
    data_val = attr.ib(default=None)
    last_modified_date = attr.ib(default=None)
    column = attr.ib(default=None)

    def __repr__(self):
        return f"{self.label}:{self.data_val}"

    def __str__(self):
        return f"{self.label}:{self.data_val}"
