from json import loads
import requests
from re import MULTILINE, search
from .models.student import Student


class OnCourse:
    def __init__(self, username: str, password: str):
        # Start requests session
        self.requestSession = requests.Session()
        """ Start the request session """

        # Login Info
        self.username: str = username
        """ Login Username """
        self.password = password
        """ Login Password """
        self.cookie: str = self.getCookie()
        """ Returns OnCourse auth cookie """

        # Active Profile
        self.active_profile: dict = self.getActiveProfile()
        """ Returns OnCourse active user Info """

        # Student of active profile
        self.student: Student = self.getStudent()
        """ Returns OnCourse Active Ids """


    def getCookie(self) -> bool:
        url = "https://www.oncourseconnect.com/account/login"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"Username": self.username, "Password": self.password}
        self.requestSession.post(url, headers=headers, data=data)
        oncourse_cookie = self.requestSession.cookies["_occauth"]
        self.requestSession.headers.update({"Cookie": f"_occauth={oncourse_cookie}"})
        return oncourse_cookie

    def getActiveProfile(self) -> int:
        url = "https://www.oncourseconnect.com/#/studentdata"
        source = (self.requestSession.get(url)).text
        regex = r"window.activeProfile = {(.*)}"
        windowActiveProfile = search(regex, source, MULTILINE)
        active_profile = "{" + windowActiveProfile.group(1) + "}"
        active_profile = loads(active_profile)["activeStudent"]
        return active_profile

    def getStudent(self) -> Student:
        url = f"https://www.oncourseconnect.com/api/classroom/dashboard/get_student_information?studentId={self.active_profile['id']}"
        student = self.requestSession.get(url)
        return Student(student.json()["ReturnValue"], self.active_profile["schoolId"],  self.active_profile["schoolYearId"], self.requestSession)