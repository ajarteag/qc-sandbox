
import pandas as pd
import sqlite3


db_dir = "./embedding_database/"

# Load only the columns you care about
df = pd.read_excel(
    db_dir + "food.xlsx",
    usecols=["ID", "name", "Food Group", "Calories", "Fat (g)", "Carbohydrate (g)"]
)


# Optional: clean up blank rows or IDs
df = df.dropna(subset=["id", "name"])

# Connect to SQLite (creates food.db if it doesn't exist)
conn = sqlite3.connect(db_dir + "food.db")

# Save the DataFrame to the database (overwrites any existing table)
df.to_sql(
    "foods",
    conn,
    if_exists="replace",  # use "fail" to error if table already exists
    index=False
)

conn.close()
print("Done! Saved", len(df), "rows to food.db")





#This is the source of the food data that we got
#https://tools.myfooddata.com/nutrition-facts-database-spreadsheet.php 

#to note:
#1. we are using the id so we need to somehow index this efficiently when we serach 
#2. We concetenate the name and food group to get the description 
#3. we store information on calories, proteins, fats, and carbs no other info 
#4. all data is in grams per 100g of food item

'''


#this is what we have as data so far 


#food.csv -> has the food items 
#descriptions, food category id 
#fdc id connected to it 
#food category id can be joined with description to create the correct long description 
#you can cache the description in a dict so that it doesn't really cause issue 

#use fdc_id to get the item + search for the calries i think 


#food_category.csv needs to have the descriptiosn 

#food nutriet conversion factor.csv -> has the fcd_id connected to an id 
#get the fcd_id to be just the id 

#then use the id for food_calorie_converstion_factor 
#then you can get the grams of proteins, fat and carbs 


'''

