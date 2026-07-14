from fastapi import FastAPI, HTTPException, Query, Path
from app.services.products import all_get_products
from app.schema.product import Product
import json

app = FastAPI()

# using fastapi for learn backend------->>>>>CURD Oprations 
# GET--> Read
# POST--> Create
# 
# uses of GET method for read----->>>>>>
@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI E-commerce API"}

@app.get("/products")
def list_products(name: str = Query(
    default=None,
    min_length=2,
    max_length=50,
    description="Search by products names (case insensitive)",
    example="Funskool Toy Product 125",
    ),
    sort_by_prices:bool = Query(
        default=False,
        description="Sort products by prices."
    ),
    order: str = Query(
            default="asc", 
            description="Sort order when sort_by_prices=true (asc, dec)"
    ),

    # Pagination params — limit: max items per page, offset: items to skip
    limit:int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of items to return",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Pagination Offset",
    ),

):

    products = all_get_products()

    if name:
        needle = name.strip().lower()  
        products = [p for p in products if needle in p.get('name', " ").lower()]

    if not products:
        raise HTTPException(status_code=404, detail=f"No products found with name of {name}")
    
    if sort_by_prices:
        reverse = order == "desc"
        products = sorted(products, key=lambda p: p.get("price", 0), reverse=reverse)

        

    total = len(products)
    products = products[offset: offset + limit ]
    return {
        "total": total,
        "limit": limit,
        "items": products
    }


@app.get("/products/{products_id}")
# path uses for rules and validations
def get_products_by_id(
    products_id: int = Path(
        ...,
        ge=1,
        le=999,
        description="ID of the products",
        example="1",
    )
):

    products = all_get_products()
    for product in products:
        if product["id"] == products_id:
            return product
    
    raise HTTPException(status_code=404, detail="Products will be not found.")


# uses of POST method for create---------->>>>>

@app.post("/products", status_code=201)
def create_product(product: Product):
    return product