class ReportCard:
    def __init__(self, report: dict, active_profile, request_session):
         self.classes = self.__getClasses(report) 
         self.current_grades = self.__getCurrentGrade(report)
         self.json = report

    def __getClasses(self, report):
        classes = []
        for rows in report.get("report_cards")[0].get("rows"):
            for classname in rows:
                if classname.get("type") == 'class':
                    classes.append(classname.get("class"))
        return classes
    
    def __getCurrentGrade(self, report):
        grades = {}
        foo = 0 
        gradelist = report.get("report_cards")[0].get("rows")
        for item in gradelist:
            foo = 0 
            for item2 in item:
                if item2.get("grade") == "": 
                    foo = foo - 1 
                    grades[item[0].get('class')] = item[foo].get("grade")
                    #grades.append(item[foo].get("grade"))
                    break
                foo = foo + 1 
        if grades == {}: 
            for item in gradelist:
                grade = item[-1].get("grade")
                classname = item[0].get('class')
                grades[classname] = grade
        return grades