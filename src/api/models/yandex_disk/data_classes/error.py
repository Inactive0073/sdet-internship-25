from dataclasses import dataclass

from .base import BaseDataClass


@dataclass
class ErrorDataClass(BaseDataClass):
    message: str = ""
    description: str = ""
    error: str = ""
