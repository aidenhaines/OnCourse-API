# active_profile = {
#     "fullName": "Maureen Haines",
#     "features": {
#         "ieP_ELEMENTS": True,
#         "curriculuM_UNIT": True,
#         "walkmE_SESSION_RECORDING": False,
#         "classmanager": False,
#         "gradinG_IN_PROGRESS": False,
#         "gradebooK_UPGRADE_BUTTON": False,
#         "reporT_UI_UPGRADE": False,
#         "scP_IMAGE_DOWNLOAD": False,
#         "tinymcE_4": False,
#         "blender": True,
#         "learnositY_ITEM_REGRADING": True,
#         "curR_UNIT_UPGRADE_BUTTON": True,
#         "domO_PUBLISH": False,
#         "supporT_SCREENRECORDER": False,
#         "analysiS_BY_ITEM": False,
#         "gradebooK_UPGRADE": False,
#         "planneR_UPGRADE": False,
#         "reporT_UI_UPGRADE_BUTTON": False,
#     },
#     "permissions": [
#         "dashboard",
#         "lms",
#         "calendar",
#         "announcements",
#         "academichistory",
#         "schedule",
#         "attendance",
#         "discipline",
#         "studentdata",
#         "notifications",
#         "profile",
#         "change_request",
#         "latest_grades",
#     ],
#     "students": [
#         {
#             "id": 11350268,
#             "name": "Haines, Aiden R.",
#             "schoolId": 20775,
#             "schoolYearId": 40081,
#             "active": True,
#             "studentActiveInSystem": True,
#             "schoolName": "Palmyra High School",
#             "lmsAccess": True,
#             "lmsMinAge": 5,
#             "showLmsNotification": False,
#             "districtHasPlanner": True,
#             "healthScreeningStatus": None,
#         },
#         {
#             "id": 11349573,
#             "name": "Haines, Danica G.",
#             "schoolId": 20775,
#             "schoolYearId": 40081,
#             "active": False,
#             "studentActiveInSystem": True,
#             "schoolName": "Palmyra High School",
#             "lmsAccess": True,
#             "lmsMinAge": 5,
#             "showLmsNotification": False,
#             "districtHasPlanner": True,
#             "healthScreeningStatus": None,
#         },
#         {
#             "id": 11552387,
#             "name": "Haines, Deakon T.",
#             "schoolId": 32108,
#             "schoolYearId": 40081,
#             "active": False,
#             "studentActiveInSystem": True,
#             "schoolName": "Palmyra Middle School",
#             "lmsAccess": True,
#             "lmsMinAge": 5,
#             "showLmsNotification": False,
#             "districtHasPlanner": True,
#             "healthScreeningStatus": None,
#         },
#     ],
#     "activeStudent": {
#         "id": 11350268,
#         "name": "Haines, Aiden R.",
#         "schoolId": 20775,
#         "schoolYearId": 40081,
#         "active": True,
#         "studentActiveInSystem": True,
#         "schoolName": "Palmyra High School",
#         "lmsAccess": True,
#         "lmsMinAge": 5,
#         "showLmsNotification": False,
#         "districtHasPlanner": True,
#         "healthScreeningStatus": None,
#     },
#     "theme": {"id": "paper", "name": "Paper", "sidebarColumns": 1},
#     "enforceClassroomHw": False,
#     "userType": "G",
#     "classroomTodoStartDateSpan": 7,
#     "classroomTodoStartDateSpanType": "days",
# }

from .student import Student
from typing import List, Union


class ActiveProfile:
    def __init__(self, active_profile:dict):
        self.active_profile = active_profile
        self.full_name = active_profile.get('fullName')
        self.features = active_profile.get('features')
        self.permissions = active_profile.get('permissions')
        self.students = active_profile.get('students')
        self.active_student = active_profile.get('activeStudent')
        self.theme = active_profile.get('theme')
        self.enforce_classroom_hw = active_profile.get('enforceClassroomHw')
        self.user_type = active_profile.get('userType')
        self.classroom_todo_start_date_span = active_profile.get('classroomTodoStartDateSpan')
        self.classroom_todo_start_date_span_type = active_profile.get('classroomTodoStartDateSpanType')
        self.student = self.__getStudents()
        """Provides a list is more than 1 Student, else just Student"""

    def __getStudents(self) -> Union[List["Student"], Student]:
        """Provides a list is more than 1 Student, else just Student"""
        url = "https://www.oncourseconnect.com/api/classroom/dashboard/get_student_information?studentId={student_id}"
        if len(self.students) == 1:
            student = self.active_profile["students"][0]
            retrieved_student = self.requestSession.get(url.format(student_id=student["id"])).json()["ReturnValue"]

            return Student(retrieved_student, student["schoolId"], student["schoolYearId"], self.requestSession)
        else:
            students = []
            for student in self.active_profile["students"]:
                retrieved_student = self.requestSession.get(url.format(student_id=student["id"])).json()["ReturnValue"]
                students.append(
                    Student(
                        retrieved_student,
                        student["schoolId"],
                        student["schoolYearId"],
                        self.requestSession,
                    )
                )
            return students
