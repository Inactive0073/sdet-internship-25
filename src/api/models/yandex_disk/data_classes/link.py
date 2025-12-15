from dataclasses import dataclass

from .base import BaseDataClass


@dataclass
class LinkDataClass(BaseDataClass):
    href: str = ""
    method: str = ""
    templated: bool = False
