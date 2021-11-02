from .student import Student
from typing import List, Union


class ActiveProfile:
    def __init__(self, active_profile: dict, requestSession):
        self.requestSession = requestSession
        self.active_profile = active_profile
        self.full_name = active_profile.get("fullName")
        self.features = active_profile.get("features")
        self.permissions = active_profile.get("permissions")
        self.students: dict = active_profile.get("students")
        """Please use 'student' unless you are doing this on purpose"""
        self.active_student: dict = active_profile.get("activeStudent")
        """Please use 'student' unless you are doing this on purpose"""
        self.theme = active_profile.get("theme")
        self.enforce_classroom_hw = active_profile.get("enforceClassroomHw")
        self.user_type = active_profile.get("userType")
        self.classroom_todo_start_date_span: int = active_profile.get("classroomTodoStartDateSpan")
        self.classroom_todo_start_date_span_type = active_profile.get("classroomTodoStartDateSpanType")

    @property
    def student(self) -> Union[List["Student"], Student]:
        """
        Gets the student data.

        returns:
            Returns 'Student' if there is 1 student on the account\n
            Returns a list of 'Student' if multiple students per account. (Normally Guardian Accounts)

        """
        url = "https://www.oncourseconnect.com/api/classroom/dashboard/get_student_information?studentId={student_id}"
        if len(self.students) == 1:
            student = self.students[0]
            retrieved_student = self.requestSession.get(url.format(student_id=student["id"])).json()["ReturnValue"]

            return Student(retrieved_student, student["schoolId"], student["schoolYearId"], self, self.requestSession)
        else:
            students = []
            for student in self.students:
                retrieved_student = self.requestSession.get(url.format(student_id=student["id"])).json()["ReturnValue"]
                students.append(
                    Student(
                        retrieved_student,
                        student["schoolId"],
                        student["schoolYearId"],
                        self,
                        self.requestSession,
                    )
                )
            return students
