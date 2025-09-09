#Josiah Stoltzfus, Nov 25, 2024, CPT 187 W01, Project: Collection Management Tool

import sqlite3
from collectors_tool import queries as q
from collectors_tool.record import Record
from pathlib import Path
import os
conn = None

#connect to database
def connect():
    global conn
    if not conn:

        BASE_DIR = Path(__file__).resolve().parent
        print("Base:", BASE_DIR)

        # data directory
        DATA_DIR = BASE_DIR / "data"
        print(DATA_DIR)
        
        db_file = DATA_DIR / "collectorsTool.db"
        print(db_file)
        
        #check if database exists
        if os.path.exists(db_file):
            conn = sqlite3.connect(db_file)
            conn.row_factory = sqlite3.Row
        #if database doesn't exist, create new database
        else:
            conn = sqlite3.connect(db_file)
            conn.row_factory = sqlite3.Row
            conn.execute(q.CREATE_USER_TABLE)
            conn.execute(q.CREATE_CATEGORY_TABLE)
            conn.execute(q.CREATE_SOURCE_TABLE)
            conn.execute(q.CREATE_COLLECTION_TABLE)
            conn.execute(q.CREATE_ITEM_TABLE)
            conn.execute(q.CREATE_ADMIN)
            conn.execute(q.CREATE_USER)

#this method accepts a query argument and returns a list of Record objects that contains the fields/values from the query results
#this method will convert the rowfactory into a dictionary which holds the keys/values, which can be passed to create a Record object
def get_records(query):
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        results_dict =[]
        records = []
        
        #loop through the query results, convert each row to dictionary, then add to list
        for row in results:
            results_dict.append(dict(row))
        
        #loop through list of dictionaries and create a Record object, then add to list of Records
        for row in results_dict:
            records.append(Record(row))
        
        #return list of record objects
        return records

#get all active users in the database
def get_active_users():
    return get_records(q.ACTIVE_USERS)
#get all active items in the database
def get_active_items():
    return get_records(q.ACTIVE_ITEMS)
#get all active categories in the database
def get_active_categories():
    return get_records(q.ACTIVE_CATEGORIES)
#get all active sources in the database
def get_active_sources():
    return get_records(q.ACTIVE_SOURCES)
#get all active collections in the database
def get_active_collections():
    return get_records(q.ACTIVE_COLLECTIONS)

#deactivates a source 
def deactivate_source(id):
    query = "update source set active = 0 where source_id = ?"
    cursor = conn.cursor()
    cursor.execute("BEGIN TRANSACTION")
    cursor.execute(query, (id,))
    cursor.execute(q.UPDATE_SOURCE_ITEMS)
    conn.commit()

#deactivates an item
def deactivate_item(id):
    query = "update item set active = 0 where item_id = ?"
    cursor = conn.cursor()
    cursor.execute(query, (id,))
    conn.commit()

#deactivates a category
def deactivate_category(id):
    query = "update category set active = 0 where category_id = ?"    
    cursor = conn.cursor()
    cursor.execute("BEGIN TRANSACTION")
    cursor.execute(query, (id,))
    cursor.execute(q.UPDATE_COLLECTIONS)
    cursor.execute(q.UPDATE_COLLECTION_ITEMS)
    conn.commit()

#deactivates a collection
def deactivate_collection(id):
    query = "update collection set active = 0 where collection_id = ?"
    cursor = conn.cursor()
    cursor.execute("BEGIN TRANSACTION")
    cursor.execute(query, (id,))
    cursor.execute(q.UPDATE_COLLECTION_ITEMS)
    conn.commit()

#adds an item
def add_item(item:'Record'):
    #item table keys: collection_id, source_id, item_name, description, price_paid, current_value
    query = "insert into item (collection_id, source_id, item_name, description, price_paid, current_value) values (?, ?, ?, ?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(query, item.values)
    conn.commit()
    print("item record added: ", dict(zip(item.keys, item.values)))

#adds a source
def add_source(source:'Record'):
    values = [x for x in source.values]
    #source table keys: first_name, last_name, phone, email, address, city, state
    query = "insert into source (first_name, last_name, phone, email, address, city, state) values (?, ?, ?, ?, ?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    print("source record added: ", dict(zip(source.keys, source.values)))

#adds a category
def add_category(category:'Record'):
    values = category.values
    #category table keys: category_name
    query = "insert into category (category_name) values (?)"
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    print("category record added: ", dict(zip(category.keys, category.values)))

#adds a collection
def add_collection(collection:'Record'):
    values = collection.values
    #collection table keys: category_id, collection_name
    query = "insert into collection (category_id, collection_name) values (?, ?)"
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    print("collection record added: ", dict(zip(collection.keys, collection.values)))

#activates all of the rows in the database
def activate_all_items():
    activate_collections()
    activate_sources()
    activate_items()
    activate_categories()

#activates all collections
def activate_collections():
    query = "update collection set active=1 where active=0"
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

#activates all categories
def activate_categories():
    query = "update category set active=1 where active=0"
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

#activates all sources
def activate_sources():
    query = "update source set active=1 where active=0"
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

#activates all items
def activate_items():
    query = "update item set active=1 where active=0"
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

#updates a source
#first_name, last_name, phone, email, address, city, state, source_id
def update_source(source: "Record"):
    query = q.EDIT_SOURCE
    cursor = conn.cursor()
    cursor.execute(query, (source.first_name, source.last_name, source.phone, source.email, source.address, source.city, source.state, source.source_id))
    print("Source updated") 
    conn.commit()

#updates an item
#item_name, price_paid, current_value, description
def update_item(item: "Record"):
    query = q.EDIT_ITEM
    cursor = conn.cursor()
    cursor.execute(query, (item.item_name, item.price_paid, item.current_value, item.description, item.item_id))
    print("Item updated")
    conn.commit()

#updates a category
def update_category(category: "Record"):
    query = q.EDIT_CATEGORY
    cursor = conn.cursor()
    cursor.execute(query, (category.category_name, category.category_id))
    print("Category updated")
    conn.commit()

#updates a collection
def update_collection(collection: "Record"):
    query = q.EDIT_COLLECTION
    cursor = conn.cursor()
    cursor.execute(query, (collection.collection_name, collection.collection_id))
    print("Collection updated")

#closes the database
def close():
    if conn:
        conn.close()

def main():
    pass

if __name__ == "__main__":
    main()











