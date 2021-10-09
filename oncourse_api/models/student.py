from datetime import date

class Student:
    """ Make the orginazation better for student """
    def __init__(self, student: dict, school_id: int, school_year_id: int, request_session):
        self.first_name = student["first_name"]
        self.last_name = student["last_name"]
        self.email = student["email"]
        self.phone = student["phone"]
        self.street_address1 = student["street_address1"]
        self.street_address2 = student["street_address2"]
        self.city = student["city"]
        self.state = student["state"]
        self.postal_code = student["postal_code"]
        self.grade_level = student["grade_level"]
        self.school_name = student["school"]
        self.id = student["id"]
        self.school_id = school_id
        self.school_year_id = school_year_id
        self.requestSession = request_session
        self.classes = self.getClasses()
        self.assignments = self.getAssignments()
        

        self.studen_potriat = f"https://www.oncourseconnect.com/json.axd/file/image?app=STUDENT_PORTRAITS&id={self.id}"
        self.reportCard = self.reportCard()
        

    def reportCard(self) -> dict:
        url = f"https://www.oncourseconnect.com/api/classroom/grades/report_cards?schoolId={self.school_id}&schoolYearId={self.school_year_id}&studentId={self.id}"
        report_card = (self.requestSession.get(url)).json()
        return report_card

    def getAttendence(self) -> dict:
        url = f"https://www.oncourseconnect.com/api/classroom/attendance/attendance_summary?schoolId={self.school_id}&schoolYearId={self.school_year_id}&studentId={self.id}"
        attendance = (self.requestSession.get(url)).json()
        return attendance

    def getClasses(self) -> dict:
        url = f"https://www.oncourseconnect.com/json.axd/classroom/lms/classes/list_student_groups?showAll=N&studentId={self.id}"
        classes = (self.requestSession.get(url)).json()
        return classes

    def getAssignments(self) -> dict:
        today = date.today()
        startDate:str = today.strftime("%m/%d/%Y")
        endDate:str = str(today.month) + "/" + str(today.day) + "/" + str(today.year + 1)
        url = f"https://www.oncourseconnect.com/json.axd/classroom/lms/assignments/get_student_work_due?endDate={endDate}&startDate={startDate}&studentId={self.id}"
        assignments = (self.requestSession.get(url)).json()
        return assignments




