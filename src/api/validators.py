import re

from fastapi import HTTPException

VALIDATE_USER_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
PHONE_NUMBER_PATTERN = re.compile(
    r"^([+]?[\s0-9]+)?(\d{3}|[(]?[0-9]+[)])?([-]?[\s]?[0-9])+$"
)


def validate_name(value):
    if not VALIDATE_USER_PATTERN.match(value):
        raise HTTPException(status_code=422, detail="Name should contains only letters")
    return value


def validate_surname(value):
    if not VALIDATE_USER_PATTERN.match(value):
        raise HTTPException(
            status_code=422, detail="Surname should contains only letters"
        )
    return value


def validate_phone_number(value):
    if not PHONE_NUMBER_PATTERN.match(value):
        raise HTTPException(status_code=422, detail="Incorrect phone number")
    return value
