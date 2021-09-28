from json import loads
import requests
from re import MULTILINE, search


class OnCourse:
    def __init__(self, username: str, password: str):
        self.requestSession = requests.Session()
        """ Start the request session """
        self.username: str = username
        """ Login Username """
        self.password = password
        """ Login Password """
        self.cookie: str = self.getCookie()
        """ Returns OnCourse auth cookie """
        self.active_profile: dict = self.activeProfile()
        """ Returns OnCourse active user Info """
        self.id: int = self.activeProfile["id"]
        """ Returns OnCourse User ID """
        self.name: int = self.activeProfile["name"]
        """ Returns Student Name """
        self.school_id: int = self.activeProfile["schoolId"]
        """ Returns School ID """
        self.school_year_id: int = self.activeProfile["schoolYearId"]
        """ Returns School Year ID """
        self.school_name: str = self.activeProfile["schoolName"]
        """ Returns School Name """
        self.report_card: str = self.reportCard()
        """ Returns Report Card """
        self.studen_potriat = f"https://www.oncourseconnect.com/json.axd/file/image?app=STUDENT_PORTRAITS&id={self.id}"
        

    def getCookie(self) -> bool:
        print("Getting Cookie")
        url = "https://www.oncourseconnect.com/account/login"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"Username": self.username, "Password": self.password}
        self.requestSession.post(url, headers=headers, data=data)
        oncourse_cookie = self.requestSession.cookies["_occauth"]
        self.requestSession.headers.update({"Cookie": f"_occauth={oncourse_cookie}"})
        return oncourse_cookie

    def activeProfile(self) -> int:
        url = "https://www.oncourseconnect.com/#/studentdata"
        source = (self.requestSession.get(url)).text
        regex = r"window.activeProfile = {(.*)}"
        windowActiveProfile = search(regex, source, MULTILINE)
        activeProfile = "{" + windowActiveProfile.group(1) + "}"
        return loads(activeProfile)["activeStudent"]

    def reportCard(self) -> dict:
        url = f"https://www.oncourseconnect.com/api/classroom/grades/report_cards?schoolId={self.schoolId}&schoolYearId={self.schoolYearId}&studentId={self.id}"
        report_card = self.requestSession.get(url)
        return report_card.json()

