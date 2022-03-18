from attr import fields, has
from datetime import datetime, timezone


def to_dict(inst) -> dict:
    if (converter := getattr(inst, "as_dict", None)) is not None:
        return converter()

    attrs = fields(inst.__class__)
    d = {}

    for a in attrs:
        if a.metadata.get("no_export", False):
            continue

        raw_value = getattr(inst, a.name)
        if raw_value is None or raw_value is False or raw_value == "":
            continue

        if (c := a.metadata.get("export_converter", None)) is not None:
            value = c(raw_value)
        else:
            value = _to_dict_any(raw_value)

        if isinstance(value, (bool, int)) or value:
            d[a.name] = value

    return d


def _to_dict_any(inst):
    if has(inst.__class__):
        return to_dict(inst)
    elif isinstance(inst, dict):
        return {key: _to_dict_any(value) for key, value in inst.items()}
    elif isinstance(inst, (list, tuple, set, frozenset)):
        return [_to_dict_any(item) for item in inst]
    elif isinstance(inst, datetime):
        if inst.tzinfo:
            return inst.isoformat()
        else:
            return inst.replace(tzinfo=timezone.utc).isoformat()
    else:
        return inst
