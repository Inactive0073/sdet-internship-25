from dataclasses import dataclass

from .base import BaseDataClass


@dataclass
class ResourceDataClass(BaseDataClass):
    name: str = ""
    path: str = ""
    created: str = ""
    modified: str = ""
    mime_type: str = ""
    media_type: str = ""
    size: int = 0
    type: str = ""
