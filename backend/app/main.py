from typing import Union
from app.db.db import populate_hash_table_qp, populate_hash_map_sc, get_data_for_fuzzysearch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from thefuzz import fuzz, process
import time

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

@app.get("/calculate_daily_nutrition")
def calc_daily_nutrition(product_ids : list[int]) -> dict[str, float]:
    calories_qp = 0.0
    protein_qp = 0.0
    sugar_qp = 0.0
    calories_sc = 0.0
    protein_sc = 0.0
    sugar_sc = 0.0

    start_time_qp = time.time() 
    for id in product_ids:
        food = hash_table_qp.has(id)
        calories_qp  += food.calories
        protein_qp += food.protein
        sugar_qp += food.sugar
    end_time_qp = time.time()
    time_taken_qp = end_time_qp - start_time_qp


    start_time_sc = time.time() 
    for id in product_ids:
        food = hash_map_sc.has(id)
        calories_sc  += food.calories
        protein_sc += food.protein
        sugar_sc += food.sugar
    end_time_sc = time.time()
    time_taken_sc = end_time_sc - start_time_sc

    result_dict = {
        "calories": calories_qp,
        "protein": protein_qp,
        "sugar": sugar_qp,
        "query_time_qp": time_taken_qp,
        "query_time_sc": time_taken_sc
    }

    return result_dict