# Welcome to Our Backend

Make sure in your terminal path you have cd'd into backend directory.

First create a virtual environment (you only need to do this once):

`python -m venv .venv`

Each time you want to use the backend, be sure to activate the virtual environment:

`source .venv/bin/activate`

Now you can install the dependencies for this project in your virtual environment:

`pip install -r requirements.txt`

With the csv files on your local computer, the code in this backend can generate the database necessary for the app. __Make sure to only run this file if food.db does NOT exist in your local backend folder.__ You only need to run this once to generate the database:

`python -m app.db.db`

Finally, to run our api locally:

`fastapi dev app/main.py`

To connect wtih front end, run:

* `cd ../frontend`
* `npm run dev`

## Citation for dataset used to build the database
U.S. Department of Agriculture (USDA), Agricultural Research Service. FoodData
Central: USDA Global Branded Food Products Database. Version Current: April 2024.
Internet: fdc.nal.usda.gov.