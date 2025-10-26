from typing import Annotated, Any, Literal

import streamlit as st
from pydantic import BaseModel, BeforeValidator, Field, SecretStr, ValidationError


def ensure_string_only(value: str) -> str:
    """Validator to ensure the string contains only alphabetic characters."""
    if value.isnumeric():
        raise ValueError("String must contain only alphabetic characters.")
    return value

StringOnly = Annotated[str, BeforeValidator(ensure_string_only)]

class FormDataSchema(BaseModel):
    """Pydantic model for the demo form.

    - name, role, and location are required strings
    - age is optional (int)
    """

    name: StringOnly = Field(strict=True, description="Your name", min_length=2, max_length=100)
    age: int | None = Field(default=None, description="Your age", ge=10, le=120)
    password: SecretStr = Field(..., description="Your password", min_length=8, max_length=16)
    role: Literal["User", "Admin", "Guest"] = Field(..., description="Your role")
    location: StringOnly = Field(strict=True, description="Your location", min_length=2, max_length=50)


st.title("My Streamlit App")

_form_data: dict[str, Any] = {}

"""
Forms in Streamlit do not dynamically update until submission. i.e. the values inside the form fields are not updated 
until the form is submitted.
"""
with st.form(key="demo-form"):
    _form_data["name"] = st.text_input("Enter name:")
    _form_data["age"] = st.number_input("Enter age:", min_value=10, max_value=120, value=10, step=1)
    _form_data["role"] = st.selectbox("Select role:", ["User", "Admin", "Guest"])
    _form_data["location"] = st.text_input("Enter location:")
    _form_data["password"] = st.text_input("Enter password:", type="password")

    submit_button: bool = st.form_submit_button("Submit")


# Only validate when the form is submitted
if submit_button:
    # Treat a 10 age as "not provided" (optional). Adjust as needed.
    if _form_data.get("age") == 10:
        _form_data["age"] = None

    try:
        form_data = FormDataSchema(**_form_data)
    except ValidationError as e:
        # Show structured validation errors in the Streamlit UI
        st.error("There were validation errors in the form input:")
        st.json(e.errors())
    else:
        st.success("Bravo! Form validated successfully.")
        # Display cleaned/validated data
        st.json(form_data.model_dump())
