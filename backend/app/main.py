from typing import Union
from app.db.db import populate_hash_table_qp, populate_hash_map_sc, get_data_for_fuzzysearch
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

# hash_table, description_to_id_map, all_brands = populate_hash_table()
# brand_choices = list(all_brands)
hash_table_qp, timer_qp = populate_hash_table_qp()
hash_map_sc, timer_sc = populate_hash_map_sc()
description_map, all_brands = get_data_for_fuzzysearch()
# this maps from a food's description to a list of tuples of (food's brand, food's id), since description isn't unique
description_choices = list(description_map.keys())

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/quadraticprobing/{key}")
def read_root(key: int):
    return {"result": hash_table_qp.has(key)}

@app.get("/separatechaining/{key}")
def getFood(key: int):
    return {"result": hash_map_sc.has(key)}

@app.get("/fuzzysearch")
def find_products(description: str, brand: str = None):
    # fuzzy search
    if brand is not None:
        brand_matches: tuple[str, int | float] = process.extract(brand, all_brands, limit=25, scorer=fuzz.ratio)
    else:
        brand_matches = []

    description_matches: tuple[str, int | float] = process.extract(description, description_choices, limit=10000, scorer=fuzz.partial_token_sort_ratio)

    brand_matches = [b[0] for b in brand_matches]
    for b in brand_matches:
        print(f"brand: {b}")

    result = []

    if brand is not None:
        print(f"size of description_matches: {len(description_matches)}")
        for product_description, score in description_matches:
            for product in description_map[product_description]:
                # iterate through the number of products there are with this matched description
                if product[0] in brand_matches:
                    if len(result) <= 100:
                        result.append((product_description, product[0], product[1]))
    else:
        for product_description, score in description_matches:
            for product in description_map[product_description]:
                # iterate through the number of products there are with this matched description
                if len(result) <= 100:
                    result.append((product_description, product[0], product[1]))

    return {"products": result}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}