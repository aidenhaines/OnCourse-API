class ReportCard:
    def __init__(self, report: dict, active_profile, request_session):
         self.classes = self.__getClasses(report) 
    def __getClasses(self, report):
        classes = []
        for rows in report.get("report_cards")[0].get("rows"):
            for classname in rows:
                if classname.get("type") == 'class':
                    classes.append(classname.get("class"))
        return classes