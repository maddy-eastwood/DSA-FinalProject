# the imports 
from typing import Union
from app.db.db import populate_hash_table_qp, populate_hash_map_sc, get_data_for_fuzzysearch
from fastapi import FastAPI
# allows front end to access api
from fastapi.middleware.cors import CORSMiddleware 
# using this for string matching
from thefuzz import fuzz, process
#being used to measure performance time between the two hashing strategies
import time

# ***pydantic model to recieve the front end data - lets FASTAPI automatically parse and validate JSON sent from frontend
from pydantic import BaseModel

app = FastAPI()

# allows all origins regardless of the front end
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
#quadractic probing
hash_table_qp, timer_qp = populate_hash_table_qp()
# separate chaining
hash_map_sc, timer_sc = populate_hash_map_sc()
# maps food descriptions
description_map, all_brands = get_data_for_fuzzysearch()
# this maps from a food's description to a list of tuples of (food's brand, food's id), since description isn't unique
# list of all descriptions used for fuzzy matching
description_choices = list(description_map.keys())

# just a basic check I JUST COMMENTED IT OUT FOR NOW
#@app.get("/")
#def read_root():
    #return {"Hello": "World"}

# using quadratic probing hash table to check if food with this id exists and returns it
@app.get("/quadraticprobing/{key}")
def read_root(key: int):
    return {"result": hash_table_qp.has(key)}

# using separate chaining hash table to check if a food with this id exists and returns it
@app.get("/separatechaining/{key}")
def getFood(key: int):
    return {"result": hash_map_sc.has(key)}

# perfoms a fuzzy search based on description AKA user input matched with description_choices - brand further filters matches
@app.get("/fuzzysearch")
def find_products(description: str, brand: str = None):
    # fuzzy search - if brand is provided, fuzzy matches that 
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
        # returns up to 100 products as (description, brand, id)
        for product_description, score in description_matches:
            for product in description_map[product_description]:
                # iterate through the number of products there are with this matched description
                if len(result) <= 100:
                    result.append((product_description, product[0], product[1]))

    return {"products": result}

# not actively being used in the logic - this is a demo end point
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# given a list of product ids, compute total calories, protein and sugar and compare lookup times for qp and sc
@app.get("/calculate_daily_nutrition")
def calc_daily_nutrition(product_ids : list[int]) -> dict[str, float]:
    calories_qp = 0.0
    protein_qp = 0.0
    sugar_qp = 0.0
    calories_sc = 0.0
    protein_sc = 0.0
    sugar_sc = 0.0

# iterates over product ids, calls .has(id) for each DS, adds up nutrition and measures time taken using time.time()
# returns a dictionary with nutrition and timing info
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

# ***defining a pydtantic model called FoodList 
# ***expects a JSON object with a key "foods" mapping to a list of strings - matches what svelte sends
class FoodList(BaseModel):
    foods: list[str]


# ***new post endpoint 
@app.post("/")
# ***FastApi automatically parses incoming JSON into a FoodList object
def handle_food_names(data: FoodList):
    # ***storing all matched food product IDs here
    matching_ids = []

    # ***iterate over the 10 food strings submitted by the user
    for food in data.foods:
        # ***skip any empty ones
        if not food.strip():
            continue # ***skip empty strings

        # ***fuzzy match to find close matches between the input food name and know product descriptions
        description_matches = process.extract(food, description_choices, limit=10, scorer=fuzz.partial_token_sort_ratio)

        # ***go thru each best match
        for match, _ in description_matches:
            # *** get all product entries for that description
            for product in description_map.get(match, []):
                # ***append the food's unique id to the list
                matching_ids.append(product[1]) # ***product[1] is the food ID
                break # ***only take the first match - no duplicates or going further than needed

    # ***calls existing function to calculate calories, protein, sugar and query times using the two hash tables 
    return calc_daily_nutrition(matching_ids)