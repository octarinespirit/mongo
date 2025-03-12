"""For testing the pymongo database"""
import bcrypt
import base64
from pymongo import MongoClient

def password_hashing(password: str) -> str:
    """Password is hashed by bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return base64.b64encode(hashed).decode()

def insert_multiple(to_insert: list):
    """Inserts many new user records to the database"""
    with MongoClient() as client:
        db = client.mydb
        users = db.users
        user_list = []
        try:
            for user in to_insert:
                username = user.get("username")
                password = user.get("password")

                if not username or not password:
                    print(f"User skipped because of missing data (username or password): {user}")
                    continue

                user_record = user.copy()
                user_record["password"] = password_hashing(user["password"])
                user_list.append(user_record)

            if user_list:
                user_ids = users.insert_many(user_list).inserted_ids
                print(f"User records created with ids: {user_ids}")
                print(f"Stored total of {len(to_insert)} users.")
        except:
            print("Could not insert record.")

def update(to_update: dict, update_to: dict):
    """Updates one record from the database. If it is a password, the password is hashed before saved."""
    with MongoClient() as client:
        db = client.mydb
        users = db.users
        try:
            if "password" in to_update:
                update_to["password"] = password_hashing(update_to["password"])
            else:
                users.update_one(to_update, update_to)
            print("Record updated.")
        except:
            print("Could not update record.")

def delete(item_to_delete: dict):
    """Deletes one record from the database"""
    with MongoClient() as client:
        db = client.mydb
        users = db.users
        try:
            users.delete_one(item_to_delete)
            print("Record deleted.")
        except:
            print("Could not delete the record")

user1 = {"username": "joonas", "password": "123", "favorite_nmbr": "007", "hobbies": ["bowling", "nature", "gym"]}
user2 = {"username": "janne", "password": "hei101", "favorite_food": "pasta" , "hobbies": ["books", "cars", "skiing"]}
user3 = {"username": "jaakko", "password": "k88yui", "phone": "0508920324"}

# Add new user records
new_users =[user1, user2, user3]
insert_multiple(new_users)

# Update records
to_update = {"username": "janne"}
update_to = {"$set": {"username": "jouni"}}
update(to_update, update_to)

# Delete records
to_delete = {"username": "joonas"}
delete(to_delete)

# Counting
with MongoClient() as client:
    db = client.mydb
    users = db.users
    find = {"username": "janne"}
    print("User records found: ", users.count_documents({}))
    print("Users with the name Janne found: ", users.count_documents(find))

# Indexing
with MongoClient() as client:
    db = client.mydb
    users = db.users
    db.users.create_index("username")
    print(f"Indexed username janne found from object: {users.find({"username": "janne"})}")
