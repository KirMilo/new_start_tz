import datetime
import re
from collections.abc import Iterable

from pydantic import BaseModel, field_serializer, field_validator


def get_date(string: str) -> list[str]:  # year, month, day
    if string[2].isdigit():  # direct seq
        return string.split(string[4])
    else:  # reversed seq
        return string.split(string[2])[::-1]


class Entry(BaseModel):
    dt: datetime.datetime | str
    user: str
    phone: list[int] | list[str] | str | None
    email: str | None
    reason: str

    @field_validator("dt")  # noqa
    @classmethod
    def validate_dt(cls, value: str):
        date, time = value.split(" ")
        return datetime.datetime(*map(int, get_date(date) + time.split(":")))

    @field_serializer("dt")
    def normalize_dt(self, v: datetime.datetime) -> str:
        return v.isoformat()

    @field_serializer("email")
    def encode_email(self, value: str | None) -> str | None:
        if isinstance(value, str):
            username, domain = value.split("@")
            return (username[:2] if len(username) > 1 else '') + ("*" * 8) + domain
        elif value is None:
            return None
        else:
            raise TypeError(f"Email must be a string or None. Received {type(value)}")

    @field_validator("phone")  # noqa
    @classmethod
    def normalize_phone(cls, value: list[int] | list[str] | str | None) -> str | None:
        if isinstance(value, Iterable):
            return "+{}-{}{}{}-{}{}{}-{}{}-{}{}".format(*value)
        elif value is None:
            return None
        else:
            raise TypeError(f"Phone must be a Iterable or None. Received {type(value)}")


def parse_lines(filename="test.txt") -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.readlines()


def get_entry(line: str) -> Entry:
    m1 = line.find("]")
    dt = line[1:m1]
    user = line[m1 + 1:line.find("(")].strip()

    m2 = line.find("(")
    m3 = line.rfind(")")
    phone = re.sub(r'\D', '', line[m2 + 1:m3])[:11]
    phone = phone if len(phone) == 11 else None

    search_email = re.findall(r'email:\s*([^\s)]+)', line)
    if search_email:
        email = search_email[0]
    else:
        email = None

    reason = line[m3 + 1:].strip()

    return Entry(dt=dt, user=user, email=email, phone=phone, reason=reason)


def main():
    lines = parse_lines()
    entries = [get_entry(line) for line in lines]

    for entry in entries:
        dt, user, phone, email, reason = entry.model_dump().values()
        print(
            f"[{dt}] {user} ({('phone: ' + phone) if phone else ''}"
            f"{", " if phone and email else ''}"
            f"{('email: ' + email) if email else ''}) {reason}"
        )

if __name__ == "__main__":
    main()
    # Зашифровать номера телефонов в +*-***-**-**
    # Скрыть e-mail адреса любым удобным образом
    # Унифицировать даты и время
