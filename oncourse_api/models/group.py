# [{"id":"C8145218","name":"Careers & College Exploration","unread_messages":0,"marking_period_name":"MP1","current_grade":"103  A+","teacher_name":"Mr. Tracey","teacher_id":11331014,"color":7,"color_hex":"#8D5F35","active":"Y"},{"id":"C8145234","name":"Digital Photography","unread_messages":0,"marking_period_name":"MP1","current_grade":"99  A+","teacher_name":"Mr. George, Mr. Nevitt","teacher_id":14529478,"color":10,"color_hex":"#0274F6","active":"Y"},{"id":"C8145061","name":"English IV (CP)","unread_messages":6,"marking_period_name":"MP1","current_grade":"79  C+","teacher_name":"Mrs. Patchel, Mrs. Reisinger","teacher_id":11331037,"color":6,"color_hex":"#2AA7E0","active":"Y"},{"id":"C8144842","name":"Nutrition","unread_messages":1,"marking_period_name":"MP1","current_grade":"88  ","teacher_name":"Mr. Papenberg","teacher_id":11331047,"color":2,"color_hex":"#E65EA1","active":"Y"},{"id":"C8145222","name":"PE IV","unread_messages":3,"marking_period_name":"MP1","current_grade":"97  A+","teacher_name":"Mr. Papenberg","teacher_id":11331047,"color":8,"color_hex":"#71BC70","active":"Y"},{"id":"C8144871","name":"Sociology","unread_messages":0,"marking_period_name":"MP1","current_grade":"100  A+","teacher_name":"Mr. Sheel","teacher_id":13267016,"color":4,"color_hex":"#8970A6","active":"Y"},{"id":"G123303","name":"Class of 2022 - Advisor Updates Etc","unread_messages":5,"marking_period_name":"","current_grade":"","teacher_name":"","teacher_id":"","color":11,"color_hex":"#7523D3","active":"Y"},{"id":"G48165","name":"Class of 2022 Guidance Information","unread_messages":27,"marking_period_name":"","current_grade":"","teacher_name":"","teacher_id":"","color":3,"color_hex":"#FBD16D","active":"Y"},{"id":"G77061","name":"Yearbook- 12","unread_messages":22,"marking_period_name":"","current_grade":"","teacher_name":"","teacher_id":"","color":12,"color_hex":"#F2075A","active":"Y"}]
from datetime import date
from typing import List
from oncourse_api.errors import NoAssignments

from .assignment import ClassAssignment
class Class:
    def __init__(self, class_dict, student_id, request_session):
        self.requestSession = request_session
        self.__student_id = student_id
        self.id = class_dict['id']
        self.name = class_dict['name']
        self.unread_messages = class_dict['unread_messages']
        self.marking_period_name = class_dict['marking_period_name']
        self.current_grade = class_dict['current_grade']
        self.teacher_name = class_dict['teacher_name']
        self.teacher_id = class_dict['teacher_id']
        # self.color = class_dict['color']
        self.color_hex = class_dict['color_hex']
        self.active = class_dict['active']

    def __str__(self):
        return f"Class(id={self.id}, name={self.name}, marking_period_name={self.marking_period_name}, current_grade={self.current_grade}, teacher_name={self.teacher_name}, teacher_id={self.teacher_id}, color_hex={self.color_hex}, active={self.active})"

    def __repr__(self):
        return f"{self.name}"

    def getAssignments(self) -> List['ClassAssignment']:
        #print(f"Getting assignments for class {self.name}")
        #^ I guess unneccesary? This function returns objects, not output so I don't think the announcement is necessary
        url = f"https://www.oncourseconnect.com/json.axd/classroom/lms/assignments/get_assignment_listing?assignmentType=A&groupId={self.id}&studentId={self.__student_id}"
        assignments = (self.requestSession.get(url)).json()
        if len(assignments) == 0:
            raise NoAssignments(f"No assignments found for {self.name}")
        return [ClassAssignment(a, self.requestSession) for a in assignments]
