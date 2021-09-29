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

        self.studen_potriat = f"https://www.oncourseconnect.com/json.axd/file/image?app=STUDENT_PORTRAITS&id={self.id}"
        self.reportCard = self.reportCard()
        

    def reportCard(self) -> dict:
        url = f"https://www.oncourseconnect.com/api/classroom/grades/report_cards?schoolId={self.school_id}&schoolYearId={self.school_year_id}&studentId={self.id}"
        report_card = self.requestSession.get(url)
        return report_card.json()

    def getAttendence(self) -> dict:
        url = f"https://www.oncourseconnect.com/api/classroom/attendance/attendance_summary?schoolId={self.school_id}&schoolYearId={self.school_year_id}&studentId={self.id}"
        attendance = (self.requestSession.get(url)).json()
        return attendance




