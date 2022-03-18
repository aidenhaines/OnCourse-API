from datetime import datetime
from typing import TYPE_CHECKING

from attr import define
import attr

from oncourse_api.utils.converters import timestamp_converter

from oncourse_api.models.base import OncourseObject

if TYPE_CHECKING:
    from oncourse_api.models.active_profile import ActiveProfile


@define
class OverviewAssignment(OncourseObject):
    """A basic form of assignment with miscellaneous info"""

    type: str = attr.ib(default=None)
    assignment_id: int = attr.ib(default=None)
    assignment_name: str = attr.ib(default=None)
    group_id: int = attr.ib(default=None)
    group_name: str = attr.ib(default=None)
    due_date: datetime = attr.ib(default=None, converter=timestamp_converter)
    late_assignment_mode: str = attr.ib(default=None)
    rrule: str = attr.ib(default=None)
    recurrence_end: str = attr.ib(default=None)
    is_missing: bool = attr.ib(default=None)
    is_late: bool = attr.ib(default=None)
    color: str = attr.ib(default=None)
    color_hex: str = attr.ib(default=None)

    @classmethod
    def _process_dict(cls, data: dict, active_profile: "ActiveProfile") -> "OverviewAssignment":
        if data.get("is_missing") == "Y":
            data["is_missing"] = True
        else:
            data["is_missing"] = False

        data["is_late"] = True if timestamp_converter(data.get("due_date")) < datetime.now() else False

        return data

    def __str__(self) -> str:
        return (
            f"OverviewAssignment(type={self.type}, assignment_id={self.assignment_id},"
            f" assignment_name={self.assignment_name}, group_id={self.group_id}, group_name={self.group_name},"
            f" due_date={self.due_date}, late_assignment_mode={self.late_assignment_mode}, rrule={self.rrule},"
            f" recurrence_end={self.recurrence_end}, is_missing={self.is_missing}, color={self.color},"
            f" color_hex={self.color_hex}, is_late={self.is_late})"
        )

    def __repr__(self):
        return f"{self.name}"


@define
class ClassAssignment(OncourseObject):
    """This assignment comes from a class/group and returns more data about the assignment"""

    lms_assign_id: int = attr.ib(default=None)
    assignment_name: str = attr.ib(default=None)
    group_name: str = attr.ib(default=None)
    assignment_description: str = attr.ib(default=None)
    due_date: datetime = attr.ib(default=None, converter=timestamp_converter)
    weight: str = attr.ib(default=None)
    external_guid: str = attr.ib(default=None)
    allow_resume: str = attr.ib(default=None)
    question_count: int = attr.ib(default=None)
    grade_column: str = attr.ib(default=None)
    is_missing: bool = attr.ib(default=None)

    @classmethod
    def _process_dict(cls, data: dict, active_profile: "ActiveProfile") -> "ClassAssignment":

        if data.get("is_missing") == "Y":
            data["is_missing"] = True
        else:
            data["is_missing"] = False

        return data

    def __str__(self):
        return (
            f"ClassAssignment(id={self.id}, name={self.name}, class_name={self.class_name},"
            f" description={self.description}, due_date={self.due_date}, weight={self.weight},"
            f" external_guid={self.external_guid}, allow_resume={self.allow_resume},"
            f" question_count={self.question_count})"
        )

    def __repr__(self):
        return f"{self.name}"

    @property
    def link(self) -> str:
        """Returns the link to the assignment"""
        print()
        return f"https://www.oncourseconnect.com/#/lms/assignments/{self._active_profile}/{self.id}"
