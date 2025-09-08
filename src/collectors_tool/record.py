#Josiah Stoltzfus, Nov 25, 2024, CPT 187 W01, Project: Collection Management Tool

"""
This class is used to store the data from the tables in the database. Each Record object corresponds
to a row of data in the database. When creating a Record object, the constructor receives a dictionary.
The key, value pairs in the dictionary represent the fields and the values for a row in the database.

When the Record object is created, the constructor will loop through the dictionary and dynamically
create fields that correspond to the name of the keys from the table, and the value of that key will be assigned
to that attribute. The constructor also creates a separate list containing the keys, and a separate list
containing the values. These are used as properties to get a list of the values and keys.

The toString method of the Record class will return all of the names of the attributes for the class (excluding the built-in attributes), so the user
knows what kind of data they can access for each object. A Record object isn't matched to any specific table in 
the database, and it will contain the fields and keys for whatever the query returns.

For a demonstration of the class, refer to the test.py file

"""
class Record:
    def __init__(self, row: dict[str, str]):
        self._keys = [] #create a list to store the keys
        self._values = []#create a list to store the values
        for key, value in row.items(): #loop through the items in the dictionary
            key = key.lower().replace(" ", "") #make the key and value lowercase #remove any spaces in the name of the field
            setattr(self, key, value) #this method will assign the key as an attribute, and the value as it's value
            self._keys.append(key) #this adds the key to the list of keys
            self._values.append(value) #this adds the value to the list of values

    @property
    def values(self):
        return self._values
    
    @property
    def keys(self):
        return self._keys

    def activate(self): 
        self._active = 1

    def deactivate(self):
        self._active = 0

    def __str__(self):
        #the dir method returns a list of all the attributes and methods for an object
        fields = [x for x in dir(self) if not x.startswith("_")] #filter the list from dir() and remove the builtin attributes that begin/end with __
        return f"Attributes: [ {"  ".join(fields)} ]" #turn the list of attributes into a string and return it


def main():
    pass


if __name__ == "__main__":
    main()



