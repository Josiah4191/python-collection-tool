#Josiah Stoltzfus, Nov 25, 2024, CPT 187 W01, Project: Collection Management Tool
from collectors_tool.ui.ui_frames import Login_Frame, Root
from collectors_tool import db

"""
account information:
    username: user
    password: password

    username: admin
    password: password

required modules:
    tkinter
    PIL - pip install pillow
    sqlite3
    os
"""
def main(): 
    #connect to database
    db.connect()

    #window
    root = Root()

    #frames
    Login_Frame(root)

    #run
    root.mainloop()

if __name__=="__main__":
    main() 
