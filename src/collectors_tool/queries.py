#Josiah Stoltzfus, Nov 25, 2024, CPT 187 W01, Project: Collection Management Tool

"""
These are the queries that are used in the program. The idea was to try to organize the queries and make the database
module cleaner. Not every query is stored here, but most of them are.
"""

active_queries = (
        "select * from category where active = 1",
        "select * from collection where active = 1",
        "select * from item where active = 1",
        "select * from source where active = 1",
        "select * from user where active = 1"
)

(ACTIVE_CATEGORIES, ACTIVE_COLLECTIONS, ACTIVE_ITEMS, ACTIVE_SOURCES, ACTIVE_USERS) = active_queries    

UPDATE_SOURCE_ITEMS = """update item
set active = 0
where source_id in (select source_id from source where active = 0);
"""

UPDATE_COLLECTION_ITEMS = """update item
set active = 0
where collection_id in (select collection_id from collection where active = 0);
"""

UPDATE_COLLECTIONS = """update collection set active = 0
where category_id in (select category_id from category where active = 0)
"""

EDIT_SOURCE = """update source set
first_name = ?,
last_name = ?,
phone = ?,
email = ?,
address = ?,
city = ?,
state = ?
where source_id = ?"""

EDIT_ITEM = """update item set
item_name = ?,
price_paid = ?,
current_value = ?,
description = ?
where item_id = ?"""

EDIT_CATEGORY = """update category set
category_name = ?
where category_id = ?"""

EDIT_COLLECTION = """update collection set
collection_name = ?
where collection_id = ?"""

CREATE_ADMIN = """insert into user (username, password, type, active) values ("admin", "password", "admin", 1)"""

CREATE_USER = """insert into user (username, password, type, active) values ("user", "password", "user", 1)"""

CREATE_CATEGORY_TABLE = """CREATE TABLE "category" (
	"category_id"	INTEGER,
	"category_name"	TEXT,
	"active"	INTEGER DEFAULT 1,
	PRIMARY KEY("category_id")
);"""

CREATE_USER_TABLE = """CREATE TABLE "user" (
	"user_id"	INTEGER,
	"username"	TEXT,
	"password"	TEXT,
	"type"	TEXT,
	"active"	INTEGER DEFAULT 1,
	PRIMARY KEY("user_id")
);"""

CREATE_COLLECTION_TABLE = """CREATE TABLE "collection" (
	"collection_id"	INTEGER,
	"category_id"	INTEGER,
	"collection_name"	TEXT,
	"active"	INTEGER DEFAULT 1,
	PRIMARY KEY("collection_id"),
	FOREIGN KEY("category_id") REFERENCES "category"("category_id")
);"""

CREATE_ITEM_TABLE = """CREATE TABLE "item" (
	"item_id"	INTEGER,
	"collection_id"	INTEGER,
	"source_id"	INTEGER,
	"item_name"	TEXT,
	"description"	TEXT,
	"price_paid"	INTEGER,
	"current_value"	INTEGER,
	"active"	INTEGER DEFAULT 1,
	PRIMARY KEY("item_id"),
	FOREIGN KEY("collection_id") REFERENCES "collection"("collection_id"),
	FOREIGN KEY("source_id") REFERENCES "source"("source_id")
);"""

CREATE_SOURCE_TABLE = """CREATE TABLE "source" (
	"source_id"	INTEGER,
	"first_name"	TEXT,
	"last_name"	TEXT,
	"phone"	TEXT,
	"email"	TEXT,
	"address"	TEXT,
	"city"	TEXT,
	"state"	TEXT,
	"active"	INTEGER DEFAULT 1,
	PRIMARY KEY("source_id")
);"""

