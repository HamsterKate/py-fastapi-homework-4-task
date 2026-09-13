from datetime import date

from fastapi import UploadFile, Form, File, HTTPException
from pydantic import BaseModel, field_validator, HttpUrl, ConfigDict

from validation import (
    validate_name,
    validate_image,
    validate_gender,
    validate_birth_date
)


class ProfileRequestSchema(BaseModel):
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    info: str
    avatar: UploadFile

    _validate_first_name = field_validator("first_name")(validate_name)
    _validate_last_name = field_validator("last_name")(validate_name)
    _validate_gender = field_validator("gender")(validate_gender)
    _validate_date_of_birth = field_validator("date_of_birth")(validate_birth_date)
    _validate_avatar = field_validator("avatar")(validate_image)

    @field_validator("info")
    @classmethod
    def validate_info(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Info field cannot be empty or contain only spaces.")
        return value

    @classmethod
    def as_form(
            cls,
            first_name: str = Form(...),
            last_name: str = Form(...),
            gender: str = Form(...),
            date_of_birth: date = Form(...),
            info: str = Form(...),
            avatar: UploadFile = File(...),
    ) -> "ProfileRequestSchema":
        return cls(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            info=info,
            avatar=avatar,
        )


class ProfileResponseSchema(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    info: str
    avatar: HttpUrl

    model_config = ConfigDict(from_attributes=True)
