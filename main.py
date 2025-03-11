"""For testing the pymongo database"""
from pymongo import MongoClient

client = MongoClient()
db = client.mydb

users = db.users

def insert(to_insert):
    """Inserts many new user records to the database"""
    user_id = users.insert_many(to_insert).inserted_ids
    print(f"User record created with id: {user_id}")


def update(to_update, update_to):
    """Updates one record from the database"""
    users.update_one(to_update, update_to)
    print("Record updated.")

def delete(item_to_delete: dict):
    """Deletes one record from the database"""
    users.delete_one(item_to_delete)
    print("Record deleted.")

user1 = {"username": "joonas", "password": "123", "favorite_nmbr": "007", "hobbies": ["bowling", "nature", "gym"]}
user2 = {"username": "janne", "password": "hei101", "favorite_food": "pasta" , "hobbies": ["books", "cars", "skiing"]}

new_users =[user1, user2]
insert(new_users)

to_update = {"username": "janne"}
update_to = {"$set": {"username": "jouni"}}
update(to_update, update_to)

to_delete = {"username": "joonas"}
delete(to_delete)

find = {"username": "janne"}

print("User records found: ", users.count_documents({}))
print("Users with the name Janne found: ", users.count_documents(find))
