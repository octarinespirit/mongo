"""For testing the pymongo database"""
from pymongo import MongoClient

# Setting up the database
client = MongoClient()
db = client.mydb

users = db.users

def insert_multiple(to_insert: list):
    """Inserts many new user records to the database"""
    try:
        user_id = users.insert_many(to_insert).inserted_ids
        print(f"User record created with id: {user_id}")
    except:
        print("Could not insert record.")

def update(to_update, update_to: dict):
    """Updates one record from the database"""
    try:
        users.update_one(to_update, update_to)
        print("Record updated.")
    except:
        print("Could not update record.")

def delete(item_to_delete: dict):
    """Deletes one record from the database"""
    try:
        users.delete_one(item_to_delete)
        print("Record deleted.")
    except:
        print("Could not delete the record")

user1 = {"username": "joonas", "password": "123", "favorite_nmbr": "007", "hobbies": ["bowling", "nature", "gym"]}
user2 = {"username": "janne", "password": "hei101", "favorite_food": "pasta" , "hobbies": ["books", "cars", "skiing"]}

# Add new user records
new_users =[user1, user2]
insert_multiple(new_users)

# Update records
to_update = {"username": "janne"}
update_to = {"$set": {"username": "jouni"}}
update(to_update, update_to)

# Delete records
to_delete = {"username": "joonas"}
delete(to_delete)

# Counting
find = {"username": "janne"}
print("User records found: ", users.count_documents({}))
print("Users with the name Janne found: ", users.count_documents(find))

# Indexing
print(db.users.create_index("username"))
print(users.find({"username": "janne"}))
