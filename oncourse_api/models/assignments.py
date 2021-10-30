from datetime import date

class Assignments:
    def __init__(self, student: dict, classid: int, school_id: int, school_year_id: int, request_session):
        self.names = self.getAssignments("formatted")
        
        self.id = student["id"]
        self.school_id = school_id
        self.school_year_id = school_year_id
        self.requestSession = request_session
        self.classes = self.getClasses()
        self.classid = classid
        #TODO: self.class_id = class['class_id']??
        self.assignments = self.getAssignments()
        #self.attendance = self.getAttendance()

        self.student_portrait = f"https://www.oncourseconnect.com/json.axd/file/image?app=STUDENT_PORTRAITS&id={self.id}"
        
    # def getAttendance(self) -> dict:
    #     url = f"https://www.oncourseconnect.com/api/classroom/attendance/attendance_summary?schoolID={self.school_id}&schoolYearID={self.school_year_id}&studentID={self.id}"
    #     attendance = (self.requestSession.get(url)).json()
    #     #TODO: implement a for loop to find the results that match a given class id, becuase I'm assuming this assignments model is per class, so will be a child method of the assignments model. BTW, I have no idea what I'm talking about, but this is fun
    #     return attendance

    def getAssignments(self, formatted=None) -> dict:
        #So, this is a different endpoint, which lists assignments in a class, but requires a group id. In the class model, we can pass this along.
        url = f"https://www.oncourseconnect.com/json.axd/classroom/lms/assignments/get_assignment_listing?assignmentType=A&groupId={self.classid}&studentId={self.id}"
        assignments = (self.requestSession.get(url)).json()
        if formatted:
            titles = []
            for item in assignments:
                titles.append(item.get("assignment_name"))
            return titles
        else:
            return assignments

    def getDetailedInfo(self, description=None) -> dict:
        #This gets the description of an assignment, not sure how we would implement this as a method.
        url = f"https://www.oncourseconnect.com/json.axd/classroom/lms/assignments/get_assignment?assignment_id={self.assignmentid}&studentId={self.id}"
        details = (self.requestSession.get(url)).json()
        if description:
            details = details.get("assignment_description")
            return details
        else:
            return details
