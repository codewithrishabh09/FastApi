from pydantic import BaseModel, Field, AnyUrl, field_validator, model_validator, computed_field
from typing import Annotated, Literal, Optional, List
from uuid import UUID
# from datatime import datatime

class Product(BaseModel):
    id: Annotated[int, 
    Field(
        ge=1,
        description="Unique products ID",
        example=1,
    ),
    ]
    sku: Annotated[
        str,
        Field(
            min_length=6,
            max_length=30,
            title="SKU",
            description="Stock Keeping Unit",
            example="SKU-SMA-0005",
        ),
    ]
    name: Annotated[
    str,
    Field(
        min_length=3,
        max_length=90,
        title="Product Name",
        description="Readable products name (3-90 chars.)",
        example="Levi's Fashion",
    ),
    ]
    description: Annotated[
        str,
        Field(
            min_length=2,
            max_length=30,
            description="Short product description",
        ),
    ]
    category: Annotated[
        str,
        Field(
            min_length=3,
            max_length=30,
            description="Category like mobile/laptop/electronic/accessories",
            example="mobiles",
        ),
    ]
    brand: Annotated[
        str,
        Field(
            min_length=1,
            max_length=30,
            example="Vivo",
        ),
    ]
    price: Annotated[
        float,
        Field(gt=0, strict=True, description="Base price (INR)"),
    ]
    currency: Literal["INR"] = "INR"

    discont_percent: Annotated[
        int,
        Field(ge=0, le=90, description="Discount in present (0-99)"),
    ] = 0

    stock: Annotated[
        int, 
        Field(ge=0, description="Available stock (>=0)"),
    ]

    is_avaliable: Annotated[
        bool,
        Field(description="Is product active?"),
    ]
    
    rating: Annotated[
        float,
        Field(ge=0, le=5, strict=True, description="Rating out of 5"),
    ]

    tags: Annotated[
        Optional[List[str]],
        Field(
            default=None, max_length=10, description="up to 10 tags maximum",
        ),
    ]

    image_url: Annotated[
        List[AnyUrl],
        Field(
            max_length=1, description="Atleat 1 image url",
        ),
    ]

    # dimension_cm
    # created data and time
    @field_validator("sku", mode="after")  
    @classmethod
    def validate_sku_formet(cls, value:str):
        if "-" not in value:
            raise ValurError("SKU must have '-'")
        
        last = value.split("-")[-1]
        if not(len(last)==4 and last.isdigit()):
            raise ValueError("SKU end with a 4-digit sequence like -2345")

        return value







