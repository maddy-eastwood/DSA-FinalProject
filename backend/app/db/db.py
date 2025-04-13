# This file was used to parse the public FDC Branded Food dataset and create a database for us to use
''' Food data citation:
U.S. Department of Agriculture (USDA), Agricultural Research Service. FoodData
Central: USDA Global Branded Food Products Database. Version Current: April 2024.
Internet: fdc.nal.usda.gov.'''

import pandas as pd
import os, sys
from sqlmodel import Field, Session, SQLModel, create_engine, select
import time
from app.quadraticprobing.hashmap import HashTable, FoodContainer
from collections import defaultdict

class Food(SQLModel, table=True):
    # id MUST be provided when creating a Food instance
    id: int = Field(primary_key = True)
    description: str
    calories: float
    protein: float
    sugar: float
    brand: str

sqlite_file_name = "./food.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def parse_and_create_foods():
    # parse dataset from csv files using pandas
    food = os.path.expanduser('~/Downloads/FoodData_Central_branded_food_csv_2024-10-31/food.csv')
    foodDf = pd.read_csv(food, usecols=["fdc_id", "description"])
    # drop any fdc_id (food product) with no description
    foodDf = foodDf.dropna(subset=["description"])

    branded_food = os.path.expanduser('~/Downloads/FoodData_Central_branded_food_csv_2024-10-31/branded_food.csv')
    brandedDf = pd.read_csv(branded_food, usecols=["fdc_id", "brand_name", "serving_size", "serving_size_unit"])

    invalid_fdc_ids = brandedDf[
        brandedDf['brand_name'].isna() | 
        brandedDf['serving_size_unit'].isna() | 
        brandedDf['serving_size'].isna()
        ]['fdc_id'].tolist()
    # drop any fdc_id that has no brand name, serving size, or serving size unit provided
    foodDf = foodDf[~foodDf['fdc_id'].isin(invalid_fdc_ids)]

    nutrient = os.path.expanduser('~/Downloads/FoodData_Central_branded_food_csv_2024-10-31/nutrient.csv')
    nutrientDf = pd.read_csv(nutrient, usecols=["id", "name", "unit_name"])

    food_nutrient = os.path.expanduser('~/Downloads/FoodData_Central_branded_food_csv_2024-10-31/food_nutrient.csv')
    foodNutrientDf = pd.read_csv(food_nutrient, usecols=["fdc_id", "nutrient_id", "amount"])

    # create dictionaries
    branded_map = brandedDf.set_index('fdc_id')['brand_name'].to_dict()
    serving_size_map = brandedDf.set_index('fdc_id')['serving_size'].to_dict()
    nutrient_map = nutrientDf.set_index('id')['name'].to_dict()
    food_nutrient_map = dict()

    # 1008: Calories, 1003: Protein, 2000: Total Sugars, 1063: Sugars, Total
    nutrients_of_interest = [1008, 1003, 2000, 1063]

    # create visited set to keep track of description, brand pairs that have been added to the db
    already_added_to_db = set()

    # populate food_nutrient_map
    for row in foodNutrientDf.itertuples(index=False, name="Row"):
        fdc_id = row.fdc_id
        nutrient_id = row.nutrient_id

        if nutrient_id in nutrients_of_interest:
            if fdc_id not in food_nutrient_map:
                food_nutrient_map[fdc_id] = dict()
            food_nutrient_map[fdc_id][nutrient_id] = row.amount

    db_count = 0

    with Session(engine) as session:
        # iterate through foodDf (dataframe for info in food.csv)
        for row in foodDf.itertuples(index=False, name="Row"):
            # if fdc_id is in foodDf but no nutritional info of interest is available, skip it
            if row.fdc_id not in food_nutrient_map:
                continue

            brand_name: str = branded_map.get(row.fdc_id)
            product_description: str = row.description

            if (product_description, brand_name) in already_added_to_db:
                # will not insert duplicate description, brand name combinations
                continue

            already_added_to_db.add((product_description, brand_name))

            nutrients = food_nutrient_map.get(row.fdc_id)
            serving_size = serving_size_map.get(row.fdc_id)

            # if any of this information is missing, skip this fdc_id from being added to the db
            cal_per_100g = nutrients.get(1008)
            protein_per_100g = nutrients.get(1003)
            sugar_per_100g = nutrients.get(2000)

            if cal_per_100g is None or protein_per_100g is None:
                continue
            if sugar_per_100g is None:
                sugar_per_100g = nutrients.get(1063)
                if sugar_per_100g is None:
                    continue

            cal_per_serving = (cal_per_100g/100) * serving_size
            protein_per_serving = (protein_per_100g/100) * serving_size
            sugar_per_serving = (sugar_per_100g/100) * serving_size

            food_entry = Food(
                id = int(row.fdc_id),
                description = product_description,
                calories = cal_per_serving,
                protein = protein_per_serving,
                sugar = sugar_per_serving,
                brand = brand_name
            )
            session.add(food_entry)
            db_count += 1
        session.commit()
    print(f"Inserted {db_count} into food.db")

def populate_hash_table() -> tuple[HashTable, dict, set]:
    with Session(engine) as session:
        start_time = time.time()
        statement = select(Food)
        food_entries = session.exec(statement).all()
        hash_table = HashTable()
        description_map = defaultdict(list)
        all_brands = set()
        # description_map = dict()
        for food in food_entries:
            brand = food.brand
            food_to_insert = FoodContainer(food.id,
                                           food.description,
                                           food.calories,
                                           food.protein,
                                           food.sugar,
                                           food.brand)
            hash_table.insert(food.id, food_to_insert)
            # fuzzy_search_string = food.description + ' ' + food.brand
            description_map[food.description].append((food.brand, food.id))
            all_brands.add(food.brand)
        end_time = time.time()
        print(f"size of hash table: {hash_table.getSize()}")
        print(f" size of description_to_id_map: {len(description_map)}")
        print(f"time to read db & construct hash table: {end_time - start_time}")
        return hash_table, description_map, all_brands


if __name__ == '__main__':
    create_db_and_tables()
    parse_and_create_foods()