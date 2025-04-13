from typing import Union
from app.db.db import populate_hash_table
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from thefuzz import fuzz, process

app = FastAPI()


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

hash_table, description_to_id_map, all_brands = populate_hash_table()
description_choices = list(description_to_id_map.keys())
brand_choices = list(all_brands)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/example/{key}")
def read_root(key: int):
    return {"result": hash_table.has(key)}

@app.get("/product/{description}?brand={brand}")
def find_products(description: str, brand: str = None):
    # fuzzy search

    # brand_matches = process.extract(brand, brand_choices, limit=25, scorer=fuzz.token_sort_ratio)
    # best_brand_match = brand_matches[0][0]

    # matched_descriptions = []
    # for description, product in description_to_id_map.items():
    #     for brand, product_id in product:
    #         if brand.lower() == best_brand_match.lower():
    #             matched_descriptions.append((description, product_id))
    # description_result = [desc for desc, _ in matched_descriptions]
    # desc_matches = process.extract(description, description_result, limit=25, scorer=fuzz.partial_token_sort_ratio)

    result = process.extract(description, description_choices, limit=25, scorer=fuzz.partial_token_sort_ratio)
    return {"products": [result]}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}