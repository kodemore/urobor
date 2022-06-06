import uuid
from datetime import datetime

from bson import ObjectId


def create_iso_time() -> str:
    return datetime.utcnow().isoformat("T", timespec="seconds").split("T")[1]


def create_iso_date() -> str:
    return datetime.utcnow().isoformat("T").split("T")[0]


def create_iso_datetime() -> str:
    return datetime.utcnow().isoformat("T", timespec="seconds")


def create_object_id() -> str:
    return str(ObjectId())


def create_uuid() -> str:
    return str(uuid.uuid4())
