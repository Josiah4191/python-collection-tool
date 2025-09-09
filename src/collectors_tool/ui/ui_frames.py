#Josiah Stoltzfus, Nov 25, 2024, CPT 187 W01, Project: Collection Management Tool

import tkinter as tk
from tkinter import ttk, IntVar
from pathlib import Path
from PIL import ImageTk, Image
from collectors_tool import db
from collectors_tool.record import Record
from collectors_tool.ui.ui_trees import Category_Tree, Collection_Tree, Item_Tree, Source_Tree, Directory_Tree
from collectors_tool import account as account
import os

'''
Custom Classes:

Root window
Main_Frame
Login_Frame
Directory_Frame
Notebook_Frame
Record_Notebook

About_Frame
Credit_Frame
Help_Frame

Add_Item_Frame
Collection_Frame
Category_Frame
Source_Frame

'''
                                                          # ROOT SEARCH
class Root(tk.Tk):                                       
    def __init__(self):
        super().__init__()
        # main setup
        self.title("Collection Manager") #title of the window
        self.geometry("1000x600") #set the default size of the window

        #this method is used to assign a callback method for when the program is exited. the on_close method will close the database
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        #select the theme for the GUI

    #this method destroys the root window and closes the database
    def on_close(self):
        db.close()
        self.destroy()

class Main_Frame(ttk.Frame):                              # MAIN FRAME SEARCH
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        #directory frame
        self.directory_frame = Directory_Frame(self)
        #notebook frame
        self.notebook_frame = Notebook_Frame(self)

        #refresh button
        self.refresh_button = ttk.Button(self.notebook_frame.notebook, width=6, text="Refresh", command=self.refresh)
        self.refresh_button.grid(column=2, row=0, pady=(30, 0), padx=(100,0))
        #restore button
        self.restore_button = ttk.Button(self.notebook_frame.notebook, width=6, text="Restore", command=self.restore)
        self.restore_button.grid(column=4, row=0, pady=(30,0))
        #logout button
        self.logout_button = ttk.Button(self.directory_frame, width=10, text="Logout", command=self.logout)
        self.logout_button.place(relx=0.5, rely=1, anchor="s")

        #check if user account is an admin or user account
        if account.get_account() == "user":
            #if it's a user, disable the refresh/restore buttons
            self.refresh_button.configure(state="disabled")
            self.restore_button.configure(state="disabled")

    #refresh the app to show the updated changes
    def refresh(self):
        self.destroy()
        Main_Frame(self.master)
        
    #activates all of the rows in the database
    def restore(self):
        db.activate_all_items()

    #logout button. destroys the main frame, and creates the login frame
    def logout(self):
        self.destroy()

#this is the frame for logging in. it acts as a welcome screen and manages user validation               #LOGIN FRAME SEARCH
class Login_Frame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relheight=1, relwidth=1)
        #configure self columns/rows
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        #create frames
        self.left_frame = ttk.Frame(self, borderwidth=2, relief="raised")
        self.left_frame.grid(column=0, row=0, sticky="nesw")

        self.right_frame = ttk.Frame(self, borderwidth=2, relief="raised")
        self.right_frame.grid(column=1, row=0, sticky="nesw")

        #configure right frame columns/rows
        self.right_frame.rowconfigure(0, weight=1)
        self.right_frame.rowconfigure(8, weight=1)
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.columnconfigure(1, weight=4)
        self.right_frame.columnconfigure(2, weight=1)

        #welcome label
        self.welcome = ttk.Label(self.right_frame, text="Welcome!")
        self.welcome.grid(column=1, row=0)
        
        # folder where app.py lives (collectors_tool/)
        BASE_DIR = Path(__file__).resolve().parents[1]
        print("Base:", BASE_DIR)

        # data directory
        DATA_DIR = BASE_DIR / "data"

        # icons folder
        ICONS_DIR = DATA_DIR / "icons"

        # individual icons
        self.person_icon_file = ICONS_DIR / "user.png"

        if os.path.exists(self.person_icon_file):
            self.person_icon = Image.open(self.person_icon_file) #<a href="https://www.flaticon.com/free-icons/person" title="person icons">Person icons created by Md Tanvirul Haque - Flaticon</a>
            self.person_icon = self.person_icon.resize((70, 70))
            self.person_icon = ImageTk.PhotoImage(self.person_icon)
        else:
            self.person_icon = None

        if self.person_icon:
            self.user_image = ttk.Label(self.right_frame, image=self.person_icon)
            self.user_image.grid(column=1, row=1, pady=(0, 15))
        else:
            print("Person icon not found")
        
        #username box
        self.user = ttk.Entry(self.right_frame)
        self.user.grid(column=1, row=2)
        self.user.insert(0, "Username")
        self.user.bind("<FocusIn>", self.delete_user_placeholder)
        self.user.bind("<FocusOut>", self.insert_user_placeholder)

        #password box
        self.password = ttk.Entry(self.right_frame)
        self.password.grid(column=1, row=3)
        self.password.insert(0, "Password")
        self.password.bind("<FocusIn>", self.delete_password_placeholder)
        self.password.bind("<FocusOut>", self.insert_password_placeholder)

        #login button
        self.login_button = ttk.Button(self.right_frame, text="Login", command=self.on_submit) ## change back to self.onsubmit for authentication
        self.login_button.grid(column=1, row=4)

        #remember checkbox
        self.check_var = IntVar()
        self.checkbutton = tk.Checkbutton(self.right_frame, text="Remember Me", variable=self.check_var, offvalue=0, onvalue=1)
        self.checkbutton.grid(column=1, row=6)

        #error label
        self.error_label = ttk.Label(self.right_frame, foreground="red", anchor="center")
        self.error_label.grid(column=1, row=7, pady=(5,0))

    #the login button will destroy the login screen and create the main_frame
    def login(self):
        Main_Frame(self.master)

    #this method will validate the user that logs in. it only checks for user and admin at the moment
    def validate_user(self, username, password):
        valid = False
        users = db.get_active_users()

        for user in users:
            if username == user.username and password == user.password:
                valid = True
                #set the user account that signs in
                #the user is a Record object from the user table that matches the username and password that's entered
                account.set_account(user)

        if username == "admin" and password == "password":
            valid = True
            __user__ = "admin"
        elif username == "user" and password == "password":
            valid = True
            __user__ = "user"
        else:
            valid = False
        return valid
    
    #login error label
    def show_error_message(self):
        self.error_label.configure(text="We couldn't verify your account\n          with that information.")

    #clears the error label
    def clear_error_message(self):
        self.error_label.configure(text="")

    #this method is used to check whether or not they checked the remember me box on login
    def remember_login_credentials(self):
        if self.check_var.get() == 0:
            return False
        else:
            return True
    
    #this will clear the username and password entry boxes
    def clear_entry(self):
        self.user.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.user.focus()
        self.password.focus()

    #this is the callback method for the submit button
    def on_submit(self):
        username = self.user.get() #get the text from username entry
        password = self.password.get() #get the text from password entry
        if self.validate_user(username, password): #pass the username/password text to the validate_user method (returns true/false)
            self.login()
            if not self.remember_login_credentials(): #check whether or not the remember checkbox is checked
                self.clear_entry() #if it isnt checked, clear the entry (otherwise, the text will remain)
        else:
            self.show_error_message() #if validation returns false, show error label message
    
    #this is the callback method for <FocusOut> event on the username entry. If the entry is empty, insert "Username"
    def insert_user_placeholder(self, event):
        if self.user.get() == "":
            self.user.insert(0, "Username")

    #this is the callback method for <FocusIn> event on the username entry. When the entry is focused, if the text is "Username", clear the text
    def delete_user_placeholder(self, event):
        if self.user.get() == "Username":
            self.user.delete(0, tk.END)
            self.clear_error_message()

    #behaves the same as the two methods above for the user name, but this is for the password
    def insert_password_placeholder(self, event):
        if self.password.get() == "":
            self.password.insert(0, "Password")

    def delete_password_placeholder(self, event):
        if self.password.get() == "Password":
            self.password.delete(0, tk.END)
            self.clear_error_message()

#this frame contains the directory tree. it also manages the about/credit/help buttons      # DIRECTORY FRAME SEARCH
class Directory_Frame(ttk.Frame): 
    def __init__(self, parent):
        super().__init__(parent, borderwidth=2, relief="raised")
        self.place(relx=0, rely=0, relheight=1, relwidth=0.3)

        #create about button
        self.about_button = ttk.Button(self, text="About", command=self.show_about_info)
        self.about_button.grid(column=0, row=0)
        #create credit button
        self.credit_button = ttk.Button(self, text="Credits", command=self.show_credit_info)
        self.credit_button.grid(column=1,row=0)
        #create help button
        self.help_button = ttk.Button(self, text="?", width=4, command=self.show_help)
        self.help_button.grid(column=2, row=0)
        #create description treeview
        self.directory_tree = Directory_Tree(self)
        self.directory_tree.place(relx=0, rely=0.11, relwidth=1, relheight=0.78)

    # creates the About frame
    def show_about_info(self):
        About_Frame(self)
        self.about_button.configure(state="disabled")

    #creates the Credit information frame
    def show_credit_info(self):
        Credit_Frame(self)
        self.credit_button.configure(state="disabled")

    #creates the Help frame for instructions
    def show_help(self):
        Help_Frame(self)
        self.help_button.configure(state="disabled")


#this frame contains the Record_Notebook, which is a widget for creating tabs
class Notebook_Frame(ttk.Frame):                            # NOTEBOOK FRAME SEARCH
    def __init__(self, parent):
        super().__init__(parent, borderwidth=2, relief="raised")
        self.place(relx=0.3, rely=0, relheight=1, relwidth=0.7)

        self.notebook = Record_Notebook(self) #the Record_Notebook class is created in this frame, which contains the tree widgets for each table
        self.notebook.place(relx=0, rely=0, relheight=1, relwidth=1)
                                

#this custom Notebook widget manages all the tabs for each tree, and it also contains a tab for adding items to the tables                                
class Record_Notebook(ttk.Notebook):                        # RECORD NOTEBOOK SEARCH
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relheight=1, relwidth=1)

        #create a frame for each tab
        self.frame1 = ttk.Frame() 
        self.frame2 = ttk.Frame()
        self.frame3 = ttk.Frame()
        self.frame4 = ttk.Frame()
        self.frame5 = Add_Item_Frame() # the final frame is the custom Add_Item_Frame
        #add the frames to the notebook to create tabs
        self.add(self.frame1, padding=35, text="Category") 
        self.add(self.frame2, padding=35, text="Collection")
        self.add(self.frame3, padding=35, text="Item")
        self.add(self.frame4, padding=35, text="Source")
        self.add(self.frame5, padding=70, text="New")

        #create the custom trees and attach them to each frame
        #category tree
        self.category_tree = Category_Tree(self.frame1) 
        self.category_tree.pack(fill=tk.BOTH, expand=True)
        #collection tree
        self.collection_tree = Collection_Tree(self.frame2)
        self.collection_tree.pack(fill=tk.BOTH, expand=True)
        #item tree
        self.item_tree = Item_Tree(self.frame3)
        self.item_tree.pack(fill=tk.BOTH, expand=True)
        #source tree
        self.source_tree = Source_Tree(self.frame4)
        self.source_tree.pack(fill=tk.BOTH, expand=True)


#this is meant to be a small pop up frame to display information about the creator of the program
class About_Frame(ttk.Frame):                               # ABOUT FRAME SEARCH
    def __init__(self, parent):
        super().__init__(parent, relief="raised")
        self.place(relx=0, rely=0, relwidth=0.8, relheight=0.2)
        self.exit_button = ttk.Button(self, text="X", width=3, command=self.close)
        self.exit_button.place(relx=0, rely=0, anchor="nw")

        self.name_label = ttk.Label(self, text="Created by Josiah Stoltzfus", padding=(10,10,10,10), relief="ridge")
        self.name_label.place(relx=0.5, rely=0.5, anchor="center")
    
    def close(self):
        self.master.about_button.configure(state="enabled")
        self.destroy()

#this is meant to be a small popup frame to give accreditation
class Credit_Frame(ttk.Frame):                              # CREDIT FRAME SEARCH
    def __init__(self, parent):
        super().__init__(parent, relief="raised")

        self.place(relx=0, rely=0, relwidth=1, relheight=0.6)
        self.exit_button = ttk.Button(self, text="X", width=3, command=self.close)
        self.exit_button.place(relx=0, rely=0, anchor="nw")


        message = """
Icons by Flat Icon

"https://www.flaticon.com/free-icons/times-square" Times square icons created by Royyan Wijaya - Flaticon

"https://www.flaticon.com/free-icons/open-folder" Open folder icons created by kmg design - Flaticon

"https://www.flaticon.com/free-icons/person" Person icons created by Md Tanvirul Haque - Flaticon
        """

        self.text = tk.Text(self)
        self.text.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        self.text.insert(tk.END, message)
        self.text.configure(state="disabled")

    def close(self):
        self.master.credit_button.configure(state="enabled")
        self.destroy()
    
#this is a small popup frame to give instructions on how to use the program
class Help_Frame(ttk.Frame):                            # HELP FRAME SEARCH
    def __init__(self, parent):
        super().__init__(parent, relief="raised")

        self.place(relx=0, rely=0, relwidth=1, relheight=0.75)
        self.exit_button = ttk.Button(self, text="X", width=3, command=self.close)
        self.exit_button.place(relx=0, rely=0, anchor="nw")

        message = """

[Refresh] > Update the tables
to reflect any changes.

[Restore] > Restore all items.

Edit or delete a row by
selecting a row in the
table and double clicking.

Deleting an item will
deactivate that item.
To reactivate all items,
click restore.

Note: Restore does not
revert edited items
to their original
values.

Note: When adding a
new category, collection,
source, or item, remember
to hit refresh.

"""
        self.text = tk.Text(self)
        self.text.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        self.text.insert(tk.END, message)
        self.text.configure(state="disabled")

    def close(self):
        self.master.help_button.configure(state="enabled")
        self.destroy()



#this frame manages the steps for creating a new category
class Category_Frame(ttk.Frame):                # CATEGORY FRAME SEARCH 
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relheight=1, relwidth=1)

        #configure row
        self.rowconfigure(0, weight=1)
        self.rowconfigure(7, weight=1)
        #configure column
        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)
        
        #add_category_label
        self.add_category_label = ttk.Label(self, text="New Category")
        self.add_category_label.grid(column=2, row=1)

        #category_name entry
        self.category_name_entry = ttk.Entry(self, text="Category Name")
        self.category_name_entry.grid(column=2, row=2, sticky="nesw")
 
        #submit button
        self.submit_button = ttk.Button(self, text="Submit", command=self.add_category)
        self.submit_button.grid(column=2, row=4, sticky="nesw")
        #back button
        self.back_button = ttk.Button(self, text="Back", command=self.destroy)
        self.back_button.grid(column=2, row=5, sticky="nesw")
        
    #this method creates and returns a new category record object
    def create_category(self):
        #get selected category
        category_name = self.category_name_entry.get().lower()
        #category table keys: category_name
        keys = ["category_name",]
        values = [category_name,]
        category = Record(dict(zip(keys, values)))
        return category

    #this method adds a category record to the category table
    def add_category(self):
        #create category
        category = self.create_category()
        #add category
        db.add_category(category)
        #show confirmation/disable submit button
        self.show_confirmation()
        self.submit_button.configure(state="disabled")
        self.after(1100, lambda:self.submit_button.configure(state="enabled"))#reenable button after 2000ms

    
    # display a label that tells the user that a category was added
    def show_confirmation(self):
        confirmation_label = ttk.Label(self, foreground="green", text="Category added.")
        confirmation_label.grid(column=2, row=6)
        self.after(1000, confirmation_label.destroy)


#this frame manages the steps for adding a new collection
class Collection_Frame(ttk.Frame):                    # COLLECTION FRAME SEARCH 

        def __init__(self, parent):
            super().__init__(parent)
            self.place(relx=0, rely=0, relheight=1, relwidth=1)

            #configure row
            self.rowconfigure(0, weight=1)
            self.rowconfigure(8, weight=1)
            #configure column
            self.columnconfigure(0, weight=1)
            self.columnconfigure(3, weight=1)

            #new_collection_label
            self.new_collection_label = ttk.Label(self, text="New Collection")
            self.new_collection_label.grid(column=2, row=1)

            #category_label
            self.category_label = ttk.Label(self, text="Category")
            self.category_label.grid(column=1, row=2)

            #category combo box
            self.category_combo_box = ttk.Combobox(self, state="readonly", values=self.show_categories())
            try:
               self.category_combo_box.current(0)
            except:
                self.category_combo_box.set("<Empty>")
            self.category_combo_box.grid(column=2, row=2, sticky="nesw")
            
            #collection_label
            self.collection_label = ttk.Label(self, text="Collection")
            self.collection_label.grid(column=1, row=3)
            
            #collection_name entry
            self.collection_name_entry = ttk.Entry(self, text="Collection Name")
            self.collection_name_entry.grid(column=2, row=3, sticky="nesw")
    
            #submit button
            self.submit_button = ttk.Button(self, text="Submit", command=self.add_collection)
            self.submit_button.grid(column=2, row=5, sticky="nesw")
            #back button
            self.back_button = ttk.Button(self, text="Back", command=self.destroy)
            self.back_button.grid(column=2, row=6, sticky="nesw")

        #this method creates and returns a new collection record object
        def create_collection(self):
            #get selected collection
            collection_name = self.collection_name_entry.get().lower()
            #get category_id
            category_id = self.get_category_id()
            #collection table keys: category_id, collection_name
            keys = ["category_id", "collection_name"]
            values = [category_id, collection_name]
            #create the new collection
            collection = Record(dict(zip(keys, values)))
            return collection

        #this method adds a collection record to the collection table
        def add_collection(self):
            #create collection
            collection = self.create_collection()
            #add collection to the database
            db.add_collection(collection)
            #show confirmation/disable submit button
            self.show_confirmation()
            self.submit_button.configure(state="disabled") #disable button
            self.after(1100, lambda:self.submit_button.configure(state="enabled"))#reenable button after 2000ms

        #this method gets the selected category_id
        def get_category_id(self): #returns the category_id as an int
            #get selected category
            category_name = self.category_combo_box.get().lower()
            #get active categories
            categories = db.get_active_categories()
            #get category_id
            category_id = None
            for category in categories:
                if category_name in category.values:
                    category_id = category.category_id
                    return category_id
                
        def show_categories(self):
            categories = [x.category_name.title() for x in db.get_active_categories()]
            categories.sort()
            return categories
                
        # display a label that tells the user that a collection was added
        def show_confirmation(self):
            confirmation_label = ttk.Label(self, foreground="green", text="Collection added.")
            confirmation_label.grid(column=2, row=7)
            self.after(1000, confirmation_label.destroy)


# this frame manages the form for adding a new item
class Add_Item_Frame(ttk.Frame):                     # ADD ITEM FRAME SEARCH 
    def __init__(self):
        super().__init__(borderwidth=2, relief="groove")
        self.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(5, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(14, weight=1)

        # add item label
        self.add_item_label = ttk.Label(self, text="New Item")
        self.add_item_label.grid(column=2, row=1)
        #category label
        self.category_label = ttk.Label(self, text="Category")
        self.category_label.grid(column=1, row=2)
        #collection label
        self.collection_label = ttk.Label(self, text="Collection")
        self.collection_label.grid(column=1, row=3)
        #source label
        self.owner_label = ttk.Label(self, text="Source")
        self.owner_label.grid(column=1, row=4)
        # item name label
        self.item_name_label = ttk.Label(self, text="Item Name")
        self.item_name_label.grid(column=1, row=6, sticky="e")
        #price label
        self.price_label = ttk.Label(self, text="Price Paid")
        self.price_label.grid(column=1, row=7, sticky="e")
        #value label
        self.value_label = ttk.Label(self, text="Current Value")
        self.value_label.grid(column=1, row=8, sticky="e")
        #description label
        self.description_label = ttk.Label(self, text="Description")
        self.description_label.grid(column=1, row=9, sticky="e")

        #category combo box
        self.category_var = tk.StringVar()
        self.category_combo_box = ttk.Combobox(self, state="readonly", justify="center", textvariable=self.category_var, values=self.show_categories()) #changed state from readonly
        try:
            self.category_combo_box.current(0)
        except:
            self.category_var.set("")
        self.category_combo_box.grid(column=2, row=2, sticky="nesw")
        #collection combo box
        self.collection_var = tk.StringVar()
        self.collection_combo_box = ttk.Combobox(self, state="readonly", justify="center", textvariable=self.collection_var, values=self.show_collections()) #changed state from readonly
        try:
            self.collection_combo_box.current(0)
        except:
            self.collection_var.set("")
        self.collection_combo_box.grid(column=2, row=3, sticky="nesw")
        #the trace_add method will call the trace_category_var function whenever a new value is written to the category combo box
        self.category_var.trace_add("write", self.trace_category_var)
        #source combo box
        self.source_var = tk.StringVar()
        self.source_combo_box = ttk.Combobox(self, state="readonly", values=self.show_sources(), justify="center")
        try:
            self.source_combo_box.current(0)
        except:
            self.source_var.set("")
        self.source_combo_box.grid(column=2, row=4, sticky="nesw")

        #item name entry box
        self.item_name_entry = ttk.Entry(self)
        self.item_name_entry.grid(column=2, row=6, sticky="nesw")
        #price entry box
        self.price_box = ttk.Entry(self)
        self.price_box.grid(column=2, row=7, sticky="nesw")
        #value entry box
        self.value_box = ttk.Entry(self)
        self.value_box.grid(column=2, row=8, sticky="nesw")
        #description box
        self.description_box = ttk.Entry(self)
        self.description_box.grid(column=2, row=9, sticky="nesw")

        #category button
        self.category_button = ttk.Button(self, text="Add", command=self.load_category_frame)
        self.category_button.grid(column=3, row=2, sticky="nesw")
        #collection button
        self.collection_button = ttk.Button(self, text="Add", command=self.load_collection_frame)
        self.collection_button.grid(column=3, row=3, sticky="nesw")
        #add source button
        self.source_button = ttk.Button(self, text="Add", command=self.load_source_frame)
        self.source_button.grid(column=3, row=4, sticky="nesw")
        #submit button
        self.submit_button = ttk.Button(self, text="Submit", command=self.add_item)
        self.submit_button.grid(column=2, row=11, sticky="nesw")

        #validate user
        if account.get_account() == "user":
            self.category_button.configure(state="disabled")
            self.collection_button.configure(state="disabled")
            self.submit_button.configure(state="disabled")
            self.source_button.configure(state="disabled")

    #this method is used to keep track of the StringVar textvariable that's connected to the category combo box
    #there is a method called trace_add, which is part of a StringVar object. you can assign a function to be called whenver the textvariable is read from or written to
    #it is used here to change the selection of the collection combo box based on what the user selects in the list of categories
    def trace_category_var(self, var, index, mode):
        try:
            #sets the values in the collection combo box.
            self.collection_combo_box.configure(values=self.show_collections())
            #sets the value of the combobox to the first value in the list. returns an error if the list is empty (ie. no collections created yet for a given category)
            self.collection_combo_box.current(0) 
        except:
                self.collection_combo_box.configure(values=[]) #if there is no collection yet for that category, assign a list of empty values
                self.collection_var.set("<Add Collection>") #set the combobox text to add a collection to indicate that it's empty

    #create the frame to add a category
    def load_category_frame(self):
        Category_Frame(self)
    #create the frame to add a collection
    def load_collection_frame(self):
        Collection_Frame(self)
    #create the frame to add a source
    def load_source_frame(self):
        Source_Frame(self)

    #this method will create and return a new item record object
    def create_item(self):
        #get the user entries
        item_name = self.item_name_entry.get().lower()
        description = self.description_box.get().lower()
        price_paid = self.price_box.get().lower()
        current_value = self.value_box.get().lower()

        #get collection_id
        collection_id = self.get_collection_id()
        #get source_id
        source_id = self.get_source_id()

        #create the item record
        #item table keys: collection_id, source_id, item_name, description, price_paid, current_value
        keys = ["collection_id", "source_id", "item_name", "description", "price_paid", "current_value"]
        values = [collection_id, source_id, item_name, description, price_paid, current_value]
        item = Record(dict(zip(keys, values)))
        return item

    #this method will add an item record to the item table
    def add_item(self):
        #create item
        item = self.create_item()
        #add item to the database
        db.add_item(item)
        #show confirmation/disable button
        self.show_confirmation()
        self.submit_button.configure(state="disabled")
        self.after(1100, lambda:self.submit_button.configure(state="enabled"))
    
    #this method will get the source_id of the selected source
    def get_source_id(self):
        #separate first_name and last_name from selected source
        source_name = self.source_combo_box.get().lower() #make the user name entry lowercase
        index = source_name.find(" ")
        first_name = source_name[0:index]
        last_name = source_name[index+1:len(source_name)]
        #get source_id
        source_id = None
        #get active sources
        sources = db.get_active_sources()
        for source in sources:
            if (source.first_name == first_name) and (source.last_name == last_name):
                source_id = source.source_id
                return source_id
    
    #this method will get the collection_id of the selected collection
    def get_collection_id(self):
        #get the selected collection
        collection_name = self.collection_combo_box.get().lower()
        #get collection_id
        collection_id = None
        #get active collections
        collections = db.get_active_collections()
        for collection in collections: 
            if collection.collection_name == collection_name:
                collection_id = collection.collection_id
                return collection_id
            
    #this method will return a list of category names that are active in the database
    def show_categories(self):
        #get a list of category objects in the database where they are active
        categories = db.get_active_categories()
        #get a list of the category names from each category object in the database
        category_names = [x.category_name.title() for x in categories]
        category_names.sort()
        #return a list of all the category names
        return category_names
    
    #this method will return a list of collection names that are active in the database
    def show_collections(self):
        #get the selected category name from the combo box
        category_name = self.category_combo_box.get().lower()
        #get the categories in the database
        categories = db.get_active_categories()
        #get category_id
        category_id = None
        for category in categories: # loop through list of categories
            if category_name in category.values:  # locate where the selected category name is at in the list of categories
                category_id = category.category_id # get the category_id where there is a match
        #query to get all the collections that have a category_id that matches the selected category
        query = f"select collection_name from collection where category_id = {category_id}"
        if category_id:
            collections = db.get_records(query)
            collection_names = [x.collection_name.title() for x in collections]
            collection_names.sort()
            #return a list of collection names that belong to the selected category
            return collection_names

    #this method will return a list of source names that are active in the database
    def show_sources(self):
        # get a list of source objects for all of the active sources in the database
        sources = db.get_active_sources()
        # combine the first name and last name for each source object in the list of sources
        source_names = [x.first_name.title() + " " + x.last_name.title() for x in sources]
        source_names.sort()
        # return a list of all the first and last names in the database that are active
        return source_names
    
    # display a label that tells the user that an item was added
    def show_confirmation(self):
        confirmation_label = ttk.Label(self, foreground="green", text="Item added.")
        confirmation_label.grid(column=2, row=13)
        self.after(1000, confirmation_label.destroy)


# this frame class manages the form for adding a new source to the database
class Source_Frame(ttk.Frame):                              # SOURCE FRAME SEARCH 
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relheight=1, relwidth=1)

        #configure row
        self.rowconfigure(0, weight=1)
        self.rowconfigure(14, weight=1)
        #configure column
        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)
        
        #add source label
        self.add_source_label = ttk.Label(self, text="New Source")
        self.add_source_label.grid(column=2, row=1)
        #first name label
        self.first_name_label = ttk.Label(self, text="First Name")
        self.first_name_label.grid(column=1, row=2)
        #last name label
        self.last_name_label = ttk.Label(self, text="Last Name")
        self.last_name_label.grid(column=1, row=3)
        #phone label
        self.phone_label = ttk.Label(self, text="Phone")
        self.phone_label.grid(column=1, row=4)
        #email label
        self.email_label = ttk.Label(self, text="Email")
        self.email_label.grid(column=1, row=5)
        #address label
        self.address_label = ttk.Label(self, text="Address")
        self.address_label.grid(column=1, row=6)
        #city label
        self.city_label = ttk.Label(self, text="City")
        self.city_label.grid(column=1, row=7)
        #state label
        self.state_label = ttk.Label(self, text="State")
        self.state_label.grid(column=1, row=8)
        #zip label
        self.zip_label = ttk.Label(self, text="Zip")
        self.zip_label.grid(column=1, row=9)

        #first name entry
        self.first_name_entry = ttk.Entry(self, text="First Name")
        self.first_name_entry.grid(column=2, row=2)
        #last name entry
        self.last_name_entry = ttk.Entry(self, text="Last Name")
        self.last_name_entry.grid(column=2, row=3)
        #phone entry
        self.phone_entry = ttk.Entry(self, text="Phone")
        self.phone_entry.grid(column=2, row=4)
        #email entry
        self.email_entry = ttk.Entry(self, text="Email")
        self.email_entry.grid(column=2, row=5)
        #address entry
        self.address_entry = ttk.Entry(self, text="Address")
        self.address_entry.grid(column=2, row=6)
        #city entry
        self.city_entry = ttk.Entry(self, text="City")
        self.city_entry.grid(column=2, row=7)
        #state entry
        self.state_entry = ttk.Entry(self, text="State")
        self.state_entry.grid(column=2, row=8)
        #zip entry
        self.zip_entry = ttk.Entry(self, text="Zip")
        self.zip_entry.grid(column=2, row=9)
        #submit button
        self.submit_button = ttk.Button(self, text="Submit", command=self.add_source)
        self.submit_button.grid(column=2, row=11, sticky="nesw")
        #back button
        self.back_button = ttk.Button(self, text="Back", command=self.destroy)
        self.back_button.grid(column=2, row=12, sticky="nesw")
    
    
    #this method creates and returns a new source record object
    def create_source(self):
        #get user entries
        first_name = self.first_name_entry.get().lower().strip().replace(" ", "-")
        last_name = self.last_name_entry.get().lower().strip().replace(" ", "-")
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        #create record
        #source table keys: first_name, last_name, phone, email, address, city, state
        keys = ["first_name", "last_name", "phone", "email", "address", "city", "state"]
        values = [first_name, last_name, phone, email, address, city, state]
        new_source = Record(dict(zip(keys,values)))
        return new_source

    #this method adds a source record to the source table
    def add_source(self):
        #create the source
        source = self.create_source()
        #add the source
        db.add_source(source)
        #show confirmation to user if success or failure adding source
        self.show_confirmation()
        self.submit_button.configure(state="disabled") #disable button
        self.after(1100, lambda:self.submit_button.configure(state="enabled")) #reenable button after 2000ms


    # display a label that tells the user that a source was added
    def show_confirmation(self):
        confirmation_label = ttk.Label(self, foreground="green", text="Source added.")
        confirmation_label.grid(column=2, row=13)
        self.after(1000, confirmation_label.destroy)
