from attr import define
import attr
from oncourse_api.models.base import OncourseObject
from .student import Student
from typing import List, Union


@define
class ActiveProfile(OncourseObject):
    requestSession = attr.ib(default=None)
    full_name = attr.ib(default=None)
    features = attr.ib(default=None)
    permissions = attr.ib(default=None)
    _students = attr.ib(default=None)
    """Please use 'student' unless you are doing this on purpose"""
    _active_student = attr.ib(default=None)
    """Please use 'student' unless you are doing this on purpose"""
    theme = attr.ib(default=None)
    enforce_classroom_hw = attr.ib(default=None)
    user_type = attr.ib(default=None)
    classroom_todo_start_date_span = attr.ib(default=None)
    classroom_todo_start_date_span_type = attr.ib(default=None)

    @property
    def student(self) -> Union[List["Student"], Student]:
        """
        Gets the student data.

        returns:
            Returns 'Student' if there is 1 student on the account\n
            Returns a list of 'Student' if multiple students per account. (Normally Guardian Accounts)

        """
        url = "https://www.oncourseconnect.com/api/classroom/dashboard/get_student_information?studentID={student_id}"
        if len(self._students) == 1:
            student = self._students[0]
            retrieved_student = self.requestSession.get(url.format(student_id=student["id"])).json()["ReturnValue"]
            return Student.from_dict(retrieved_student, self)
        else:
            students = []
            for student in self._students:
                retrieved_student = self.requestSession.get(url.format(student_id=student["id"])).json()["ReturnValue"]
                students.append(Student.from_dict(retrieved_student, self))
            return students
