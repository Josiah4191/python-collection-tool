#Josiah Stoltzfus, Nov 25, 2024, CPT 187 W01, Project: Collection Management Tool

import database as db
from python.record import Record
import os
#Josiah Stoltzfus, Nov 25, 2024, CPT 187 W01, Project: Collection Management Tool

def main():
    db.connect() #connect to database

    items = db.get_active_items() #get all active rows from the item table. returns list of Record objects

    print(type(items[0])) #get the type for the first item <class '#business.Record'>
    print()

    for item in items: #loop through Record list
        print(item.keys) #print the keys for each Record
    print()

    for item in items: #loop through Record list
        print(item.values) #print the values for each Record
    print()

    for item in items: #loop through Record list
        print(item) #print each Record object as a string
        
    db.close() #close connection to database


if __name__ == "__main__":
    main()
