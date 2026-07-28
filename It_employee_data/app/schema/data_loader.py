from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Annotated
from enum import Enum
from datetime import date


class StatusEnum(str, Enum):
    active = "Active",
    inactive = "Inactive",
    on_leave = "On Leave",
    terminated = "Terminated"


class Employee(BaseModel):
    id: Annotated[int,
    Field(
        ge=1,
        descripition="Officail employee id.",
        example=5,
    )
    ]
    first_name: Annotated[str,
    Field(
        min_length=3,
        max_length=15,
        title="Employee First Name",
        descripition="Enter employee first name.",
        example="Ayush",
    )
    ]
    last_name: Annotated[str,
    Field(
        min_length=3,
        max_length=10,
        title="Employee Last Name",
        descripition="Enter employee lat name.",
        example="Yadav",
    )
    ]
    email: Annotated[EmailStr,
    Field(
        descripition="Enter employee email address.",
        example="ayush.yadav5@example.com",
    )
    ]

    @field_validator("email", mode="after")
    @classmethod
    def validate_employee_email_domain(cls, value: EmailStr):
        allowed_domain = ["example.com", "gmail.com", "company.com"]
        domain = value.split("@")[-1].lower()
        if domain not in allowed_domain:
            raise valueError(f"Employee email domain not allowed: {domain}")
        return value

    phone: Annotated[str,
    Field(
        pattern=r"^[6-9]\d{9}$",
        descripition="Enter employee 10-digit phone number.",
        example="9039671407",
    )
    ]
    department: Annotated[str,
    Field(
        min_length=3,
        max_length=30,
        title="Employee Department",
        descripition="Enter employee depzrtment name.",
        example="Data Science",
    )
    ]
    designation: Annotated[str,
    Field(
        min_length=2,
        max_length=30,
        title="Employee Designation",
        descripition="Enter employee job designation.",
        example="DevOps",
    )
    ]
    salary: Annotated[int,
    Field(
        gt=0,
        le=10000000,
        descripition="Enter employee/anual salary.",
        example=450000,
    )
    ]
    experience: Annotated[int,
    Field(
        gt=0,
        le=50,
        descripition="How many year of exprience of employees",
        example=3,
    )
    ]
    city: Annotated[str,
    Field(
        min_length=2,
        max_length=30,
        descripition="Employee current City.",
        example="Lucknow",
    )
    ]
    state: Annotated[str,
    Field(
        min_length=2,
        max_length=30,
        descripition="Employee current state.",
        example="Jaipur",
    )
    ]
    joining_date: Annotated[date,
    Field(
        descripition="Date when employee joining the compnay.",
        example="2022-06-15",
    )
    ]
    status: Annotated[StatusEnum,
    Field(
        descripition="Current employee status",
        example="Active",
    )
    ]
    
