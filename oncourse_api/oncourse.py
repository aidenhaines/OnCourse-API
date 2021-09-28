from json import loads
import requests
from re import MULTILINE, DOTALL, search


class OnCourse:
    def __init__(self, username: str, password: str):
        self.username:str = username
        """ Login Username """
        self.password = password
        """ Login Password """
        self.cookie: str = self.getCookie()
        """ Returns OnCourse auth cookie """
        self.activeProfile: dict = self.activeProfile()
        """ Returns OnCourse active user Info """
        self.id: int = self.activeProfile["id"]
        """ Returns OnCourse User ID """
        self.name: int = self.activeProfile["name"]
        """ Returns Student Name """
        self.schoolId: int = self.activeProfile["schoolId"]
        """ Returns School ID """
        self.schoolYearId: int = self.activeProfile["schoolYearId"]
        """ Returns School Year ID """
        self.schoolName: str = self.activeProfile["schoolName"]
        """ Returns School Name """
        self.reportCard: str = self.reportCard()
        """ Returns Report Card """

    def getCookie(self) -> str:
        url = "https://www.oncourseconnect.com/account/login"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"Username": self.username, "Password": self.password}
        session = requests.Session()
        session.post(url, headers=headers, data=data)
        oncourse_cookie = session.cookies["_occauth"]
        return oncourse_cookie

    def activeProfile(self) -> int:
        url = "https://www.oncourseconnect.com/#/studentdata"
        headers = {"Cookie": f"_occauth={self.cookie}"}
        source = (requests.get(url, headers=headers)).text
        regex = r"window.activeProfile = {(.*)}"
        windowActiveProfile = search(regex, source, MULTILINE)
        activeProfile = "{" + windowActiveProfile.group(1) + "}"
        return loads(activeProfile)["activeStudent"]

    def reportCard(self) -> dict:
        url = f"https://www.oncourseconnect.com/api/classroom/grades/report_cards?schoolId={self.schoolId}&schoolYearId={self.schoolYearId}&studentId={self.id}"
        headers = {"Cookie": f"_occauth={self.cookie}"}
        report_card = requests.get(url, headers=headers)
        return report_card.json()
