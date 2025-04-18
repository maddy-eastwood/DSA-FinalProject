# Welcome to Our Backend

To download the necessary dataset to run our web app, open your browser and navigate to:
https://fdc.nal.usda.gov/download-datasets

Here you can download the October 2024 Branded CSV file. This should be downloaded into your "Downloads" folder.

Make sure in your terminal path you have navigated to backend directory.

First create a virtual environment (you only need to do this once):

`python -m venv .venv`

Each time you want to use the backend, be sure to activate the virtual environment:

For Mac: `source .venv/bin/activate`

For Windows:
`.\.venv\Scripts\Activate`

Now you can install the dependencies for this project in your virtual environment:

`pip install -r requirements.txt`

or 

`pip install -r requirements-windows.txt`

Dependencies include:

* pandas
* sympy
* sqlmodel
* fastapi
* thefuzz

With the CSV files on your local computer (assuming they are in your Downloads folder), the code in this backend can generate the database necessary for the app. __Make sure to only run this file if food.db does NOT exist in your local backend folder.__ You only need to run this once to generate the database:

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

## Note for Windows Users

Allow scripts to run as admin:

`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`

