class ReportCard:
    def __init__(self, report: dict, active_profile, request_session):
        self.classes = __getClasses(report)
    
    def __getClasses(report):
        classes = []
        for rows in report.get("report_cards").get("rows"):
            for classname in rows:
                if classname.get("type") == 'class':
                    classes.append(classname.get("class"))