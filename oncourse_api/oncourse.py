from json import loads
import requests
from re import MULTILINE, search

from oncourse_api.errors import InvalidCredentials, InvalidPassword, LockedOut
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
        self.cookie: str = self.__getCookie()
        """ Returns OnCourse auth cookie """

        # Active Profile
        self.active_profile: dict = self.__getActiveProfile()
        """ Returns OnCourse active user Info """

        # Student of active profile
        self.student: Student = self.__getStudent()
        """ Returns OnCourse Active Ids """

    def __getCookie(self) -> bool:
        url = "https://www.oncourseconnect.com/account/login"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"Username": self.username, "Password": self.password}
        resp = self.requestSession.post(url, headers=headers, data=data)

        # Check for invalid credentials

        if "Invalid username or password." in resp.text:  # Incorrect username
            raise InvalidCredentials(f"No user '{self.username}' was found.")

        elif "Username or password was invalid." in resp.text:  # Incorrect password
            locked_out = r"(\d+) attempts remaining before your account will be temporarily locked out for (\d+)"
            locked_out = search(locked_out, resp.text, MULTILINE)
            if locked_out.group(1) and locked_out.group(2):
                raise InvalidPassword(
                    f"Password incorrect. {locked_out.group()} minute(s)"
                )

        elif "Due to numerous incorrect attempts" in resp.text:  # Locked out
            duration = r"temporarily locked out for (\d+)"
            duration = search(duration, resp.text, MULTILINE)
            raise LockedOut(
                f"The account has been locked out for {duration.group(1)} minute(s). Too many invalid login attempts"
            )

        # -------------------------------------

        oncourse_cookie = self.requestSession.cookies["_occauth"]
        self.requestSession.headers.update({"Cookie": f"_occauth={oncourse_cookie}"})
        return oncourse_cookie

    def __getActiveProfile(self) -> int:
        url = "https://www.oncourseconnect.com/#/studentdata"
        source = (self.requestSession.get(url)).text
        regex = r"window.activeProfile = {(.*)}"
        windowActiveProfile = search(regex, source, MULTILINE)
        active_profile = "{" + windowActiveProfile.group(1) + "}"
        active_profile = loads(active_profile)["activeStudent"]
        return active_profile

    def __getStudent(self) -> Student:
        url = f"https://www.oncourseconnect.com/api/classroom/dashboard/get_student_information?studentId={self.active_profile['id']}"
        student = self.requestSession.get(url)
        return Student(
            student.json()["ReturnValue"],
            self.active_profile["schoolId"],
            self.active_profile["schoolYearId"],
            self.requestSession,
        )
