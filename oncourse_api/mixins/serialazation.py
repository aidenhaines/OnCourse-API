from typing import Any, Dict, List, TypeVar

import attr

import oncourse_api.utils.serializer as serializer


T = TypeVar("T")


@attr.s()
class DictSerializationMixin:
    @classmethod
    def _get_keys(cls) -> frozenset:
        if (keys := getattr(cls, "_keys", None)) is None:
            keys = frozenset(field.name for field in attr.fields(cls))
            setattr(cls, "_keys", keys)
        return keys

    @classmethod
    def _get_init_keys(cls) -> frozenset:
        if (init_keys := getattr(cls, "_init_keys", None)) is None:
            init_keys = frozenset(field.name.removeprefix("_") for field in attr.fields(cls) if field.init)
            setattr(cls, "_init_keys", init_keys)
        return init_keys

    @classmethod
    def _filter_kwargs(cls, kwargs_dict: dict, keys: frozenset) -> dict:
        return {k: v for k, v in kwargs_dict.items() if k in keys}

    @classmethod
    def _process_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        data = cls._process_dict(data)
        return cls(**cls._filter_kwargs(data, cls._get_init_keys()))

    @classmethod
    def from_list(cls, datas: List[Dict[str, Any]]):
        return [cls.from_dict(data) for data in datas]

    def update_from_dict(self: T, data: Dict[str, Any]) -> T:
        data = self._process_dict(data)
        for key, value in self._filter_kwargs(data, self._get_keys()).items():
            # todo improve
            setattr(self, key, value)

        return self

    def _check_object(self) -> None:
        pass

    def to_dict(self) -> Dict[str, Any]:
        self._check_object()
        return serializer.to_dict(self)
