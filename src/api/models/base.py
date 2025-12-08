from pydantic import BaseModel, ConfigDict


class BaseCommonModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore", populate_by_name=True, from_attributes=True
    )
