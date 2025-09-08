#Josiah Stoltzfus, Nov 25, 2024, CPT 187 W01, Project: Collection Management Tool

'''
This module creates an Account class that's used to store the state of the user that's signed in
The user attribute in the Account class is meant to store a Record object that matches one of the rows from the User table from the database
The set_account is called when the user logs in
The get_account is called to activate/deactivate parts of the program based on the user type
'''

def set_account(user):
    Account.user = user


def get_account():
    return Account.user


class Account():
    user = None