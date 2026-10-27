from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from typing import Annotated
from enum import Enum
from datetime import date


VALID_DEPARMENTS = [
    "HR", "Engineering", "Sales", "Marketing", "Data Science",
    "Finance", "Support", "Operations", "Legal", "IT",
    "Product", "Design", "AI/ML", "DevOps"
]

DEPARTMENT_DESIGNATION_MAP = {
    "Engineering": ["Software Engineer", "DevOps", "Frontend Developer", "Team Lead", "Backend Developer"],
    "HR": ["HR Executive", "Manager", "Team Lead"],
    "Sales": ["Sales Executive", "Manager", "Team Lead"],
    "Marketing": ["Marketing Executive", "Manager"],
    "Data Science": ["Data Scientist", "ML Engineer", "DevOps"],
    "Finance": ["Finance Executive", "Manager"],
    "Support": ["Support Executive", "Team Lead"],
    "IT": ["Software Engineer", "DevOps", "Support Executive"],
}

DESIGNATION_SALARY_RANGE = {
    "Intern": (10000, 25000),
    "Software Engineer": (30000, 80000),
    "Senior Software Engineer": (60000, 150000),
    "Team Lead": (80000, 200000),
    "Manager": (100000, 300000),
    "DevOps": (40000, 120000),
}

CITY_STATE_MAP = {
    "Lucknow": "Uttar Pradesh",
    "Jaipur": "Rajasthan",
    "Delhi": "Delhi",
    "Mumbai": "Maharashtra",
    "Bangalore": "Karnataka",
    "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal",
    "Hyderabad": "Telangana",
    "Pune": "Maharashtra",
    "Ahmedabad": "Gujarat",
}

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
    def validate_employee_email_domain(cls, value: EmailStr) -> EmailStr:
        allowed_domain = ["example.com", "gmail.com", "company.com"]
        domain = value.split("@")[-1].lower()
        if domain not in allowed_domain:
            raise ValueError(f"Employee email domain not allowed: {domain}")
        return value.lower()

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
        descripition="Enter employee department name.",
        example="Data Science",
    )
    ]

    @field_validator("department", mode="after")
    @classmethod
    def validate_department(cls, value: str) -> str:
        if value not in VALID_DEPARMENTS:
            raise ValueError(f"Department '{value}', is not a recogized department")
        return value.strip().title()

    
    designation: Annotated[str,
    Field(
        min_length=2,
        max_length=30,
        title="Employee Designation",
        descripition="Enter employee job designation.",
        example="DevOps",
    )
    ]

    @model_validator(mode="after")
    def validate_designation_matches_department(self):
        allowed_designations = DEPARTMENT_DESIGNATION_MAP.get(self.department)
        if allowed_designations and self.designation not in allowed_designations:
            raise ValueError(
                f"Designation '{self.designation}' is not valid for department '{self.department}'. "
                f"Allowed designations: {allowed_designations}"
            )
        return self

    salary: Annotated[int,
    Field(
        gt=0,
        le=10000000,
        descripition="Enter employee/annual salary.",
        example=450000,
    )
    ]

    @model_validator(mode="after")
    def validate_salary_for_desiganation(self):
        salary_range = DESIGNATION_SALARY_RANGE.get(self.designation)
        if salary_range:
            min_salary, max_salary = salary_range
            if not (min_salary <= max_salary <= max_salary):
                raise ValueError(
                    f"Salary {self.salary} is out of range for designation '{self.designation}'."
                    f"Expected range: {min_salary} - {max_salary}"
                )
        return self

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

    @model_validator(mode="after")
    def validate_city_state_match(self):
        expcted_state = CITY_STATE_MAP.get(self.city)
        if expcted_state and expcted_state != self.state:
            raise ValueError(
                f"City '{self.city}' is in {expcted_state}, but the state is '{self.state}'."
                f"Expected state: {expcted_state}"
            )
        return self

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


   
    
