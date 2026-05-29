from pydantic import BaseModel, Field, field_validator, field_serializer

from datetime import datetime


class Data(BaseModel):
    field_int: int
    field_str: str
    field_dt: datetime | str = Field(default_factory=datetime.now)

    @field_serializer("field_dt")
    def serialize_field_dt(self, dt: datetime) -> str:
        return dt.isoformat()

    @field_validator("field_dt")  # noqa
    @classmethod
    def validate_field_dt(cls, v: ...) -> datetime:
        if isinstance(v, datetime):
            return v
        elif isinstance(v, str):
            return datetime.fromisoformat(v)
        else:
            raise ValueError(
                f"field_dt must be one of the allowed types: datetime or str(isoformat). But it's {type(v)}",
            )


class Item(BaseModel):
    name: str
    data: Data


class DataPartial(Data):
    field_int: int | None = None
    field_str: str | None = None
    field_dt: datetime | None = None


class ItemPartial(Item):
    name: str | None = None
    data: Data | None = None
