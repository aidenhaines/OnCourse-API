from typing import TYPE_CHECKING, Any, Dict, List
import attr
from oncourse_api.mixins.serialazation import DictSerializationMixin

if TYPE_CHECKING:
    from oncourse_api.models.active_profile import ActiveProfile


@attr.s()
class OncourseObject(DictSerializationMixin):
    _active_profile: "ActiveProfile" = attr.field(metadata={"no_export": True})

    @classmethod
    def _process_dict(cls, data: Dict[str, Any], active_profile: "ActiveProfile") -> Dict[str, Any]:
        return super()._process_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], active_profile: "ActiveProfile"):
        data = cls._process_dict(data, active_profile)
        return cls(active_profile=active_profile, **cls._filter_kwargs(data, cls._get_init_keys()))

    @classmethod
    def from_list(cls, datas: List[Dict[str, Any]], active_profile: "ActiveProfile"):
        return [cls.from_dict(data, active_profile) for data in datas]

    def update_from_dict(self, data) -> None:
        data = self._process_dict(data, self._active_profile)
        for key, value in self._filter_kwargs(data, self._get_keys()).items():
            # todo improve
            setattr(self, key, value)
