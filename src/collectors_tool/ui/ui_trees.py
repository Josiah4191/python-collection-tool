#Josiah Stoltzfus, Nov 25, 2024, CPT 187 W01, Project: Collection Management Tool

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import os

from pathlib import Path
from collectors_tool import db
from collectors_tool import account
from collectors_tool.record import Record
from collections import defaultdict

'''
Custom Classes:

Directory_Tree (the methods used to manage the items have been disabled, but the code is still there. 
                adding/editing/deactivating is managed in the other trees)
Source_Tree
Item_Tree
Category_Tree
Collection_Tree

Popup_Frame
Edit_Source_Frame
Edit_Item_Frame
Edit_Category_Frame
Edit_Collection_Frame

'''

#this treeview is for displaying a hierarchical relationship between categories/collections/items/sources
class Directory_Tree(ttk.Treeview):                     # DIRECTORY TREE SEARCH
    def __init__(self, parent):
        super().__init__(parent, height=15, selectmode="browse", columns=["id"])

        #configure tree
        self.rowconfigure(0, weight=1)
        self.heading("id", text="ID")
        self.heading("#0", text="Directory")
        self.column("id", width=60, anchor="center")
        self.column("#0", width=150)


        # folder where app.py lives (collectors_tool/)
        BASE_DIR = Path(__file__).resolve().parents[1]

        # data directory
        DATA_DIR = BASE_DIR / "data"

        # icons folder
        ICONS_DIR = DATA_DIR / "icons"

        def _debug_path(name: str):
            p = ICONS_DIR / name
            print(f"ICON DEBUG: {p} exists={p.exists()}")
            return p

        def _load_icon_or_none(name: str):
            path = _debug_path(name)
            if not path.exists():
                return None
            try:
                img = tk.PhotoImage(file=path.as_posix())
            except Exception:
                try:
                    from PIL import Image, ImageTk
                    img = ImageTk.PhotoImage(Image.open(path))
                except Exception as e:
                    print(f"ICON LOAD FAIL for {name}: {e}")
                    return None
            return img

        # Create & KEEP references
        self.folder_icon = _load_icon_or_none("open-folder.png")
        self.square_icon = _load_icon_or_none("square.png")
        self.person_icon = _load_icon_or_none("user.png")

        # Belt-and-suspenders cache so references live on self
        self._icons = {"folder": self.folder_icon, "square": self.square_icon, "person": self.person_icon}

        # individual icons
        self.person_icon_file = ICONS_DIR / "user.png"
        self.square_icon_file = ICONS_DIR / "square.png"
        self.folder_icon_file = ICONS_DIR / "open-folder.png"

        if os.path.exists(self.person_icon_file):
            self.person_icon = Image.open(self.person_icon_file) #<a href="https://www.flaticon.com/free-icons/person" title="person icons">Person icons created by Md Tanvirul Haque - Flaticon</a>
            self.person_icon = self.person_icon.resize((10,10))
            self.person_icon = ImageTk.PhotoImage(self.person_icon)
        else:
            self.person_icon = None
            print("Person icon not found")
        #square icon
        if os.path.exists(self.square_icon_file):
            self.square_icon = Image.open(self.square_icon_file) #<a href="https://www.flaticon.com/free-icons/times-square" title="times square icons">Times square icons created by Royyan Wijaya - Flaticon</a>
            self.square_icon = self.square_icon.resize((10,10))
            self.square_icon = ImageTk.PhotoImage(self.square_icon)
        else:
            self.square_icon = None
            print("Square icon not found")
        #folder icon
        if os.path.exists(self.folder_icon_file):
            self.folder_icon = Image.open(self.folder_icon_file) #<a href="https://www.flaticon.com/free-icons/open-folder" title="open folder icons">Open folder icons created by kmg design - Flaticon</a>
            self.folder_icon = self.folder_icon.resize((15,15))
            self.folder_icon = ImageTk.PhotoImage(self.folder_icon)
        else:
            self.folder_icon = None
            print("Folder icon not found")

        #create scrollbar
        scrollbarY = ttk.Scrollbar(self, orient="vertical")
        scrollbarY.place(relx=1, rely=0, relheight=1, anchor="ne")
        #tree.bind("<Button-1>", lambda event: tree.yview_scroll(int(event.delta / 60)), tk.UNITS)
        self.config(yscrollcommand=scrollbarY.set)
        scrollbarY.config(command=self.yview)

        #retrieve all records from database to populate the treeview
        self.item_records = db.get_active_items()
        self.category_records = db.get_active_categories()
        self.collection_records = db.get_active_collections()
        self.source_records = db.get_active_sources()



        # create empty lists to collect the iids
        self.category_iids   = []
        self.collection_iids = []
        self.item_iids       = []
        self.source_iids     = []

        # create empty lists to collect the ids
        self.category_ids    = []
        self.collection_ids  = []
        self.item_ids        = []
        self.source_ids      = []

        # tiny helper to avoid repeated if/else for image
        def _insert(parent, img, text, values):
            kwargs = {"image": img} if img is not None else {}
            return self.insert(parent, index=tk.END, text=f" {text}", values=values, **kwargs)

        # populate the treeview by matching primary keys from the records
        for category in self.category_records:
            category_iid = _insert("", self.folder_icon, category.category_name.title(), [category.category_id])
            self.category_iids.append(category_iid)
            self.category_ids.append(category.category_id)

            for collection in self.collection_records:
                if category.category_id == collection.category_id:
                    collection_iid = _insert(category_iid, self.folder_icon, collection.collection_name.title(), [collection.collection_id])
                    self.collection_iids.append(collection_iid)
                    self.collection_ids.append(collection.collection_id)

                    for item in self.item_records:
                        if item.collection_id == collection.collection_id:
                            item_iid = _insert(collection_iid, self.square_icon, item.item_name.title(), [item.item_id])
                            self.item_iids.append(item_iid)
                            self.item_ids.append(item.item_id)

                            for source in self.source_records:
                                if item.source_id == source.source_id:
                                    source_iid = _insert(item_iid, self.person_icon, f"{source.first_name.title()} {source.last_name.title()}", [source.source_id])
                                    self.source_iids.append(source_iid)
                                    self.source_ids.append(source.source_id)


        """

        #create empty lists to collect the iids
        self.category_iids = []
        self.collection_iids = []
        self.item_iids = []
        self.source_iids = []

        #create empty lists to collect the id for each row in their respective tables within the database
        self.category_ids = []
        self.collection_ids = []
        self.item_ids = []
        self.source_ids = []

        #populate the treeview by matching primary keys from the records
        for category in self.category_records: #loop through the category records
            #the insert method returns the iid of the item that was inserted
            if self.folder_icon:
                category_iid = self.insert("", index=tk.END, image=self.folder_icon, text=f" {category.category_name.title()}", values=[category.category_id])
            else:
                category_iid = self.insert("", index=tk.END, text=f" {category.category_name.title()}", values=[category.category_id])
            self.category_iids.append(category_iid) # put all the category iids in a list
            self.category_ids.append(category.category_id) #put each category id in a list
            for collection in self.collection_records: #loop through collection records
                if category.category_id == collection.category_id: #check if category_ids match
                    if self.folder_icon:
                        collection_iid = self.insert(category_iid, image=self.folder_icon, index=tk.END, text=f" {collection.collection_name.title()}", values=[collection.collection_id])
                    else:
                        collection_iid = self.insert(category_iid, index=tk.END, text=f" {collection.collection_name.title()}", values=[collection.collection_id])
                    self.collection_iids.append(collection_iid) # put all the collection iids in a list to refer to them later
                    self.collection_ids.append(collection.collection_id) # put the collection_id in a list to connect it to the collection_iids
                    for item in self.item_records: #loop through item records
                        if item.collection_id == collection.collection_id: #check if the collection_ids match
                            if self.square_icon:
                                item_iid = self.insert(collection_iid, image=self.square_icon, index=tk.END, text=f" {item.item_name.title()}", values=[item.item_id])
                            else:
                                item_iid = self.insert(collection_iid, index=tk.END, text=f" {item.item_name.title()}", values=[item.item_id])
                            self.item_iids.append(item_iid) # put all the item iids in a list to refer to them later
                            self.item_ids.append(item.item_id) # put the item_id in a list to connect it to the item_iids
                            for source in self.source_records: #loop through source records
                                if item.source_id == source.source_id: #check if the source_ids match
                                    if self.person_icon:
                                        source_iid = self.insert(item_iid, image=self.person_icon, index=tk.END, text=f" {source.first_name.title()} {source.last_name.title()}", values=[source.source_id])
                                    else:
                                        source_iid = self.insert(item_iid, index=tk.END, text=f" {source.first_name.title()} {source.last_name.title()}", values=[source.source_id])
                                    self.source_iids.append(source_iid) # put all the source iids in a list to refer to them later
                                    self.source_ids.append(source.source_id) # put all the source_ids in a list to conect it to the source_iids
            """

#this treeview displays and manages the source table
class Source_Tree(ttk.Treeview):                                # SOURCE TREE SEARCH
    def __init__(self, parent):
        super().__init__(parent, show="headings", selectmode="browse")
        
        #get active source records
        self.sources = db.get_active_sources()

        #id, firstname, last name, phone, email, address, city, state
        columns=["id", "first name", "last name", "phone", "email", "address", "city", "state"]
        self.configure(columns=columns)
        self.column("state", anchor="center")

        #create popup frame on double click
        self.bind("<Double-Button-1>", self.popup_entry)

        #create the headings
        for column in self["columns"]:
            if column == "id":
                self.heading(column, text="ID")
            else:
                self.heading(column, text=f"{column.title()}")

        #configure the columns
        self.column("id", width=10, anchor="center")
        self.column("first name", width=40, anchor="center")
        self.column("last name", width=40, anchor="center")
        self.column("phone", width=80, anchor="center")
        self.column("email", width=80, anchor="center")
        self.column("address", width=40, anchor="center")
        self.column("city", width=40, anchor="center")
        self.column("state", width=10, anchor="center")

        #create scrollbar
        scrollbarY = ttk.Scrollbar(self, command=self.yview, orient="vertical")
        scrollbarY.place(relx=1, rely=0, relheight=1, anchor="ne")
        self.config(yscrollcommand=scrollbarY.set)

        #configure the tags
        self.tag_configure("even", background="lightgray")
        self.tag_configure("odd", background="white")

        #create list to store the iids
        self.source_iids = []

        count = 0
        #populate treeview with alternating colors
        for source in self.sources:
            if count % 2 == 0:
                source_iid = self.insert("", tag="even", index=tk.END, values=[source.source_id, source.first_name.title(), source.last_name.title(), source.phone, source.email, source.address.title(), source.city.title(), source.state.title()])
            else:
                source_iid = self.insert("", tag="odd", index=tk.END, values=[source.source_id, source.first_name.title(), source.last_name.title(), source.phone, source.email, source.address.title(), source.city.title(), source.state.title()])
            count += 1
            self.source_iids.append(source_iid)

    #this method gets the selected item in the tree, gets the value of the id column, deactivates the source, and deletes the item
    def delete_source(self):
        try:
            selection = self.selection()
            id = self.item(selection)["values"][0]
            db.deactivate_source(id)
            self.delete(selection)
        except:
            pass
    
    #this method will get the Record object for the selected item in the treeview
    def get_selected_source(self):
        try:
            selection = self.selection()[0] #get the selected item
            for iid in self.source_iids: #loop through the list of iids (not really needed, i guess)
                for source in self.sources: #loop through the list of source Record objects
                    if self.item(selection)["values"][0] == source.source_id: #check where the value of id in the selected item matches the source_id of the source object
                        return source #return that source object where there is a match
        except:
            pass
    #this method creates the popup frame and configures the buttons. 
    #the delete button will delete/deactivate the source
    #the edit button creates an Edit_Source_Frame
    def popup_entry(self, event):
        source = self.get_selected_source()
        try:
            frame = Popup_Frame(self, source)
            frame.place(x=event.x, y=event.y)
            frame.edit_button.configure(command=self.create_edit_source_frame)
            frame.delete_button.configure(command=self.delete_source)

            #validate user
            if account.get_account().type == "user":
                frame.edit_button.configure(state="disabled")
                frame.delete_button.configure(state="disabled")
        except:
            pass
    
    #this method creates an Edit_Source_Frame and is the callback function used for the edit button
    def create_edit_source_frame(self):
        source = self.get_selected_source()
        Edit_Source_Frame(self, source)


#this is the treeview that displays and manages the item table. it works the same as the source, category, and collection treeviews
class Item_Tree(ttk.Treeview):                                  # ITEM TREE SEARCH
    def __init__(self, parent):
        super().__init__(parent, show="headings", selectmode="browse", height=15)

        self.items = db.get_active_items()
        #ID, item, price, value, description
        columns = ["id", "item", "price", "value", "description"]
        self.configure(columns=columns)
        self.column("id", width=10, anchor="center")
        self.column("item", width=60)
        self.column("price", width=20, anchor="center")
        self.column("value", width=20, anchor="center")
        self.column("description", width=150)
        self.heading("id", text="ID")
        self.heading("item", text="Item")
        self.heading("price", text="Price")
        self.heading("value", text="Value")
        self.heading("description", text="Description")

        #configure the tags for the rows
        self.tag_configure("even", background="lightgray")
        self.tag_configure("odd", background="white")

        #create scrollbar
        scrollbarY = ttk.Scrollbar(self, command=self.yview, orient="vertical")
        scrollbarY.place(relx=1, rely=0, relheight=1, anchor="ne")
        self.config(yscrollcommand=scrollbarY.set)

        #configure click event
        self.bind("<Double-Button-1>", self.popup_entry)

        #collect the iids
        self.item_iids = []

        count = 0
        #populate treeview
        for item in self.items:
            #if it's an even number row, the tag is "even" (lightgray)
            if count % 2 == 0:
                item_iid = self.insert("", tag = "even", index=tk.END, values=[item.item_id, item.item_name.title(), item.price_paid, item.current_value, item.description.capitalize()])
            else:
                #if it's an odd number row, the tag is "odd" (white)
                item_iid = self.insert("", tag = "odd", index=tk.END, values=[item.item_id, item.item_name.title(), item.price_paid, item.current_value, item.description.capitalize()])
            count += 1
            self.item_iids.append(item_iid)

    #this method deletes the item in the tree and deactivates the record in the table
    def delete_item(self):
        try:
            selection = self.selection()
            id = self.item(selection)["values"][0]
            db.deactivate_item(id)
            self.delete(selection)
        except:
            pass
    #this method gets an item record that corresponds to the selected item in the tree
    def get_selected_item(self):
        try:
            selection = self.selection()[0]
            for iid in self.item_iids:
                for item in self.items:
                    if self.item(selection)["values"][0] == item.item_id:
                        return item
        except:
            pass
    #this method creates and configures the edit/delete buttons to edit an item and delete/deactivate an item
    def popup_entry(self, event):
        item = self.get_selected_item()
        try:
            frame = Popup_Frame(self, item)
            frame.place(x=event.x, y=event.y)
            frame.edit_button.configure(command=self.create_edit_item_frame)
            frame.delete_button.configure(command=self.delete_item)

            #validate user
            if account.get_account().type == "user":
                frame.edit_button.configure(state="disabled")
                frame.delete_button.configure(state="disabled")
        except:
            pass
    #this method creates an Edit_Item_Frame
    def create_edit_item_frame(self):
        item = self.get_selected_item()
        Edit_Item_Frame(self, item)

#this treeview displays and manages the data in the category table. it works the same as the item, collection, and source trees
class Category_Tree(ttk.Treeview):                          # CATEGORY TREE SEARCH

    def __init__(self, parent):
        super().__init__(parent, show="headings", selectmode="browse")

        #create scrollbar
        scrollbarY = ttk.Scrollbar(self, command=self.yview, orient="vertical")
        scrollbarY.place(relx=1, rely=0, relheight=1, anchor="ne")
        self.config(yscrollcommand=scrollbarY.set)

        # collect category_iids
        self.category_iids = []

        #configure click event
        self.bind("<Double-Button-1>", self.popup_entry)
        
        #configure tags
        self.tag_configure("even", background="lightgray")
        self.tag_configure("odd", background="white")

        # get category records
        self.categories = db.get_active_categories()
        # show category
        count = 0
        for category in self.categories:
            if count % 2 == 0:
                category_iid = self.insert("", index=tk.END, tag="even", values=[category.category_id, category.category_name.title()])
            else:
                category_iid = self.insert("", index=tk.END, tag="odd", values=[category.category_id, category.category_name.title()])
            count+=1
            self.category_iids.append(category_iid)

        #configure columns and create headings
        columns = ["id", "name"]
        self.configure(columns=columns)
        self.column("id", anchor="center", width=15)
        self.column("name")
        self.heading("id", text="ID")
        self.heading("name", text="Category")

    #this method deletes/deactivates the selected item in the category tree
    def delete_category(self):
        try:
            selection = self.selection()
            id = self.item(selection)["values"][0]
            db.deactivate_category(id)
            self.delete(selection)
        except:
            pass

    #this method gets the category object that corresponds to the selected category
    def get_selected_category(self):
        try:
            selection = self.selection()[0]
            for iid in self.category_iids:
                for category in self.categories:
                    if self.item(selection)["values"][0] == category.category_id:
                        return category
        except:
            pass
    #this method creates a popup frame for editing and deleting/deactivating a selected category      
    def popup_entry(self, event):
        category = self.get_selected_category()
        try:
            frame = Popup_Frame(self, category)
            frame.place(x=event.x, y=event.y)
            frame.edit_button.configure(command=self.create_edit_category_frame)
            frame.delete_button.configure(command=self.delete_category)
            
            #validate user
            if account.get_account().type == "user":
                frame.edit_button.configure(state="disabled")
                frame.delete_button.configure(state="disabled")
        except:
            pass

    #this method creates an Edit_Category_Frame
    def create_edit_category_frame(self):
        category = self.get_selected_category()
        frame = Edit_Category_Frame(self, category)
        frame.place(relx=0.5, rely=0.5, relheight=0.3, relwidth=0.5, anchor="center")



#this treeview displays and manages the data from the collection table. it works the same as the category, source, and item trees
class Collection_Tree(ttk.Treeview):                      # COLLECTION TREE SEARCH

    def __init__(self, parent):
        super().__init__(parent, selectmode="browse", show="headings")

        #create scrollbar
        scrollbarY = ttk.Scrollbar(self, command=self.yview, orient="vertical")
        scrollbarY.place(relx=1, rely=0, relheight=1, anchor="ne")
        self.config(yscrollcommand=scrollbarY.set)
        
        #configure double click event
        self.bind("<Double-Button-1>", self.popup_entry)

        # get collection records
        self.collections = db.get_active_collections()
        columns = ["id", "name"]
        self.configure(columns=columns)
        self.column("id", anchor="center", width=15)
        self.column("name")
        self.heading("id", text="ID")
        self.heading("name", text="Collection")

        self.tag_configure("even", background="lightgray")
        self.tag_configure("odd", background="white")

        # collect collection iids
        count = 0
        self.collection_iids = []
        for collection in self.collections:
            if count % 2 == 0:
                collection_iid = self.insert("", index=tk.END, tag="even", values=[collection.collection_id, collection.collection_name.title()])
            else:
                collection_iid = self.insert("", index=tk.END, tag="odd", values=[collection.collection_id, collection.collection_name.title()])
            count+=1
            self.collection_iids.append(collection_iid)

    #this method deletes/deactivates the selected collection
    def delete_collection(self):
        try:
            selection = self.selection()
            id = self.item(selection)["values"][0]
            self.delete(selection)
            db.deactivate_collection(id)
        except:
            pass
    
    #this method returns a collection object that corresponds to the selected collection item
    def get_selected_collection(self):
        try:
            selection = self.selection()[0]
            for iid in self.collection_iids:
                for collection in self.collections:
                    if self.item(selection)["values"][0] == collection.collection_id:
                        return collection
        except:
            pass

    #this method creates a popup frame to edit and delete/deactivate an item in the collection tree     
    def popup_entry(self, event):
        collection = self.get_selected_collection()
        try:
            frame = Popup_Frame(self, collection)
            frame.place(x=event.x, y=event.y)
            frame.edit_button.configure(command=self.create_edit_collection_frame)
            frame.delete_button.configure(command=self.delete_collection)

            #validate user
            if account.get_account().type == "user":
                frame.edit_button.configure(state="disabled")
                frame.delete_button.configure(state="disabled")
        except:
            pass
    
    #this method creates an Edit_Collection_Frame
    def create_edit_collection_frame(self):
        collection = self.get_selected_collection()
        frame = Edit_Collection_Frame(self, collection)
        frame.place(relx=0.5, rely=0.5, relheight=0.3, relwidth=0.5, anchor="center")


#this frame is a popup frame for editing and deleting/deactivating an item in the tree
class Popup_Frame(ttk.Frame):                           # POPUP FRAME SEARCH

    def __init__(self, parent, source):
        super().__init__(parent)
        self.edit_button = ttk.Button(self, text="Edit")
        self.edit_button.pack(fill=tk.BOTH, expand=True)
        self.delete_button = ttk.Button(self, text="Delete")
        self.delete_button.pack(fill=tk.BOTH, expand=True)
        self.focus_force()
        self.bind("<Leave>", self.close_window)
        
    def close_window(self, event):
        self.destroy()


#this frame manages editing for the source table
class Edit_Source_Frame(ttk.Frame):                         # EDIT SOURCE FRAME SEARCH
    def __init__(self, parent, source: "Record"):
        super().__init__(parent, borderwidth=2, relief="raised")
        self.source = source
        self.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.5, anchor="center")
        
        #configure the rows
        self.rowconfigure(0, weight=1)
        self.rowconfigure(9, weight=1)
        #configure the columns
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        #close button
        close_button = ttk.Button(self, width=2, text="X", command=self.destroy)
        close_button.place(relx=0, rely=0, anchor="nw")
        #submit button
        self.submit_button = ttk.Button(self, text="Submit", command=self.edit_source)
        self.submit_button.grid(column=1, row=8)

        #firstname label
        self.first_name = ttk.Label(self, text="First Name")
        self.first_name.grid(column=0, row=1)
        #firstname entry
        self.first_name_entry = ttk.Entry(self)
        self.first_name_entry.grid(column=1, row=1)

        #lastname label
        self.last_name = ttk.Label(self, text="Last Name")
        self.last_name.grid(column=0, row=2)
        #lastname entry
        self.last_name_entry = ttk.Entry(self)
        self.last_name_entry.grid(column=1, row=2)
        
        #phone label
        self.phone = ttk.Label(self, text="Phone")
        self.phone.grid(column=0, row=3)
        #phone] entry
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.grid(column=1, row=3)

        #email label
        self.email = ttk.Label(self, text="Email")
        self.email.grid(column=0, row=4)
        #email entry
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(column=1, row=4)

        #address label
        self.address = ttk.Label(self, text="Adddress")
        self.address.grid(column=0, row=5)
        #address entry
        self.address_entry = ttk.Entry(self)
        self.address_entry.grid(column=1, row=5)

        #city label
        self.city = ttk.Label(self, text="City")
        self.city.grid(column=0, row=6)
        #city entry
        self.city_entry = ttk.Entry(self)
        self.city_entry.grid(column=1, row=6)

        #state label
        self.state = ttk.Label(self, text="State")
        self.state.grid(column=0, row=7)
        #state entry
        self.state_entry = ttk.Entry(self)
        self.state_entry.grid(column=1, row=7)

    #this method gets all of the text from the entry boxes and changes the selected Record object values
    #once the values are changed, the Record object is passed to the db.update_source() method to update the database with the new values
    def edit_source(self):
        self.source.first_name = self.first_name_entry.get().lower()
        self.source.last_name = self.last_name_entry.get().lower()
        self.source.phone = self.phone_entry.get().lower()
        self.source.email = self.email_entry.get().lower()
        self.source.address = self.address_entry.get().lower()
        self.source.city = self.city_entry.get().lower()
        self.source.state = self.state_entry.get().lower()
        db.update_source(self.source)
        self.submit_button.configure(state="disabled") #disable the button after submitting


#this frame manages editing for the Item table. It works the same as the source,category, and collection frames
class Edit_Item_Frame(ttk.Frame):                   # EDIT ITEM FRAME SEARCH
    def __init__(self, parent, item):
        super().__init__(parent, borderwidth=2, relief="raised")
        self.item = item
        self.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.5, anchor="center")
        #configure rows
        self.rowconfigure(0, weight=1)
        self.rowconfigure(9, weight=1)
        #configure columns
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        #close button
        close_button = ttk.Button(self, width=2, text="X", command=self.destroy)
        close_button.place(relx=0, rely=0, anchor="nw")
        #submit button
        self.submit_button = ttk.Button(self, text="Submit", command=self.edit_item)
        self.submit_button.grid(column=1, row=8)

        #item name label
        self.item_name = ttk.Label(self, text="Item Name")
        self.item_name.grid(column=0, row=1)
        #item name entry
        self.item_name_entry = ttk.Entry(self)
        self.item_name_entry.grid(column=1, row=1)

        #price_paid label
        self.price_paid = ttk.Label(self, text="Price")
        self.price_paid.grid(column=0, row=2)
        #price_paid entry
        self.price_paid_entry = ttk.Entry(self)
        self.price_paid_entry.grid(column=1, row=2)
        
        #curent_value label
        self.current_value = ttk.Label(self, text="Value")
        self.current_value.grid(column=0, row=3)
        #current_value entry
        self.current_value_entry = ttk.Entry(self)
        self.current_value_entry.grid(column=1, row=3)

        #description label
        self.description = ttk.Label(self, text="Description")
        self.description.grid(column=0, row=4)
        #description entry
        self.description_entry = ttk.Entry(self)
        self.description_entry.grid(column=1, row=4)

    def edit_item(self):
        self.item.item_name = self.item_name_entry.get().lower()
        self.item.price_paid = self.price_paid_entry.get().lower()
        self.item.current_value = self.current_value_entry.get().lower()
        self.item.description = self.description_entry.get().lower()
        db.update_item(self.item)
        self.submit_button.configure(state="disabled")


#this frame manages editing for the category table. it works the same as the other edit frames
class Edit_Category_Frame(ttk.Frame):                       #EDIT CATEGORY FRAME SEARCH
    def __init__(self, parent, category):
        super().__init__(parent, borderwidth=2, relief="raised")
        self.category = category
        self.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.5, anchor="center")
        
        #configure rows
        self.rowconfigure(0, weight=1)
        self.rowconfigure(9, weight=1)
        #configure columns
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        #close button
        close_button = ttk.Button(self, width=2, text="X", command=self.destroy)
        close_button.place(relx=0, rely=0, anchor="nw")
        #submit button
        self.submit_button = ttk.Button(self, text="Submit", command=self.edit_category)
        self.submit_button.grid(column=1, row=8)

        #category name label
        self.category_name = ttk.Label(self, text="Category Name")
        self.category_name.grid(column=0, row=1)
        #category name entry
        self.category_name_entry = ttk.Entry(self)
        self.category_name_entry.grid(column=1, row=1)

    def edit_category(self):
        self.category.category_name = self.category_name_entry.get().lower()
        db.update_category(self.category)
        self.submit_button.configure(state="disabled")


#this frame manages editing for the collection table
class Edit_Collection_Frame(ttk.Frame):                 # EDIT COLLECTION FRAME SEARCH
    def __init__(self, parent, collection):
        super().__init__(parent, borderwidth=2, relief="raised")
        self.collection = collection
        self.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.5, anchor="center")
        #configure rows
        self.rowconfigure(0, weight=1)
        self.rowconfigure(9, weight=1)
        #configure columns
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        #close button
        close_button = ttk.Button(self, width=2, text="X", command=self.destroy)
        close_button.place(relx=0, rely=0, anchor="nw")
        #submit button
        self.submit_button = ttk.Button(self, text="Submit", command=self.edit_collection)
        self.submit_button.grid(column=1, row=8)

        #collection name label
        self.collection_name = ttk.Label(self, text="Collection Name")
        self.collection_name.grid(column=0, row=1)
        #collection name entry
        self.collection_name_entry = ttk.Entry(self)
        self.collection_name_entry.grid(column=1, row=1)

    def edit_collection(self):
        self.collection.collection_name = self.collection_name_entry.get().lower()
        db.update_collection(self.collection)
        self.submit_button.configure(state="disabled")

