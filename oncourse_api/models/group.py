from typing import List
from oncourse_api.errors import NoAssignments

from .assignment import ClassAssignment


class Class:
    def __init__(self, class_dict, student_id, request_session):
        self.requestSession = request_session
        self.__student_id = student_id
        self.id: int = class_dict.get("id")
        self.name: str = class_dict.get("name")
        self.unread_messages = class_dict.get("unread_messages")
        self.marking_period_name = class_dict.get("marking_period_name")
        self.current_grade = class_dict.get("current_grade")
        self.teacher_name = class_dict.get("teacher_name")
        self.teacher_id: int = class_dict.get("teacher_id")
        self.color_hex: str = class_dict.get("color_hex")
        self.active = True if class_dict.get("active") == "Y" else False

    def __str__(self):
        return (
            f"Class(id={self.id}, name={self.name}, marking_period_name={self.marking_period_name},"
            f" current_grade={self.current_grade}, teacher_name={self.teacher_name}, teacher_id={self.teacher_id},"
            f" color_hex={self.color_hex}, active={self.active})"
        )

    def __repr__(self):
        """Returns name when printed in a list"""
        return f"{self.name}"

    @property
    def assignments(self) -> List["ClassAssignment"]:
        """Returns a list of assignements in a class"""
        url = (
            "https://www.oncourseconnect.com/json.axd/classroom/lms/assignments/get_assignment_listing"
            f"?assignmentType=A&groupId={self.id}&studentId={self.__student_id}"
        )
        assignments = (self.requestSession.get(url)).json()
        if len(assignments) == 0:
            raise NoAssignments(f"No assignments found for {self.name}")
        return [ClassAssignment(a, self.requestSession) for a in assignments]
