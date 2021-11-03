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
        grades = []
        gradelist = classes.dict.get("report_cards")[0].get("rows")
        for item in gradelist:
            foo = 0
            for item2 in gradelist:
                if item2.get("grade") == "": 
                    foo = foo - 1 
                    grades.append(item[foo].get("grade"))
                    break
                foo = foo + 1 
        return grades