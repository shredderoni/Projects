import sqlite3 as sql
import bcrypt
from portfolio import Portfolio
from string import ascii_letters

connect = sql.connect("data.db")
cursor = connect.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_login NVARCHAR(60) NOT NULL,
            user_password NVARCHAR(60) NOT NULL,
            user_first_name NVARCHAR(60),
            user_last_name NVARCHAR(60),
            user_tag NVARCHAR(60)
        )
        """)
connect.commit()

class User:
    characters = ascii_letters + ' '
    valoare_invalida = """
* *  ********************************  * *
 *    You entered an invalid option!    *
* *  ********************************  * *
"""

    def __init__(self):
        self.username = ''
        self.password = ''
        self.first_name = ''
        self.last_name = ''
        self.tag = 'New'

    # Data to create a new user
    @staticmethod
    def create_username():
        print('ATTENTION! The username needs to contain only letters!')
        while True:
            create_username = input("Username: ")
            check_if_exist = [user[0] for user in cursor.execute("SELECT user_login FROM users")]
            if create_username in check_if_exist:
                print("\nThis username is already in use. Please choose another one.")
            elif create_username.isalpha() != True:
                print("\nThe username needs to contain only letters!")
            else:
                return create_username
    
    @staticmethod
    def create_password():
        SpecialChar = ['!', '%', '&', '$', '#']
        print("""ATTENTION! The password needs to contain at least:
        - 8 characters.
        - one UPPERCASE.
        - one lowercase.
        - one number.
        - one of these characters !, %, &, $, #
""")

        while True:
            create_password = input("Password: ")
            if len(create_password) < 8:
                print("\nYour password needs to contain minimum 8 characters!")
            elif not any(char.isdigit() for char in create_password):
                print('\nYour password needs to contain minimum 1 number!')
            elif not any(char.isupper() for char in create_password):
                print('\nYour password needs to contain minimum 1 UPPERCASE!')
            elif not any(char.islower() for char in create_password):
                print('\nYour password needs to contain minimum 1 lowercase!')
            elif not any(char in SpecialChar for char in create_password):
                print('\nYour password needs to contain at least one of these characters !, %, &, $, #.')
            else:
                encodedPw = create_password.encode('utf-8')
                saltGen = bcrypt.gensalt()
                hashedPw = bcrypt.hashpw(encodedPw, saltGen)
                return hashedPw
            
    @staticmethod
    def create_first_name():
        check = False
        while not check:
            create_first_name = input('First name: ')
            if set(create_first_name).difference(__class__.characters):
                print('\nThe name can only contain letters.')
            else:
                check = True
                return create_first_name
            
    @staticmethod
    def create_last_name():
        check = False
        while not check:
            create_last_name = input('Name: ')
            if set(create_last_name).difference(__class__.characters): 
                print('\nThe name can only contain letters.')
            else:
                check = True
                return create_last_name
            
    def create_tag(self):
        options = {
            1: 'User',
            2: 'Photographer',
            3: 'Admin'
        }
        print('Account types:')
        if self.tag == 'New' or self.tag == 'User':
            options_filtered = {key: options[key] for key in options.keys() & {1, 2}}
            for i,j in options_filtered.items():
                print(f'    {i} -> {j}') 
        elif self.tag == 'Admin':
            for i,j in options.items():
                print(f'    {i} -> {j}')
        check = False
        while not check:
            try:
                if self.tag == 'New' or self.tag == 'User':
                        creare_tag = int(input('\nFor what purpose are you creating this account? (number of type, for ex. 1): '))
                        if creare_tag not in range(1,3):
                            print('\nPlease select one of the valid options.')
                        else:
                            check = True
                            return options[creare_tag]
                else:
                        creare_tag = int(input('\nFor what purpose are you creating this account? (number of type, for ex. 1): '))
                        if creare_tag not in range(1,4): 
                            print('\nPlease select one of the available options.')
                        else:
                            check = True
                            return options[creare_tag]
            except ValueError:
                print(__class__.valoare_invalida)

    # Create user account
    def user_create(self):
        self.username = self.create_username()
        self.password = self.create_password()
        self.first_name = self.create_first_name()
        self.last_name = self.create_last_name()
        self.tag = self.create_tag()
        self.user_insert()

    # Inserting user account into database
    def user_insert(self):
        cursor.execute("""
        INSERT INTO users (user_login, user_password, user_first_name, user_last_name, user_tag) VALUES (?, ?, ?, ?, ?)
        """, (self.username, self.password, self.first_name, self.last_name, self.tag))
        connect.commit()
        print('\nAccount was successfully created.')

    # Login
    def user_login(self):
        print("""
    *********
    * LOGIN *
    *********
""")
        while True:
            username = input('\nUsername: ')
            check_if_exist = [user[0] for user in cursor.execute("SELECT user_login FROM users")]
            if username not in check_if_exist: 
                print("\nThis username doesn't exist.")
            else:
                break
        cursor.execute("SELECT user_password FROM users WHERE user_login = '{}'".format(username))
        db_password = cursor.fetchone()[0]
        check_password = 0
        while check_password < 3:
            password = input('Password: ')
            password = password.encode('utf-8')
            verify_password = bcrypt.checkpw(password, db_password)
            if not verify_password:
                check_password += 1
                print(f'Wrong password! You have {3-check_password} tries left.')
            else:
                check_password += 3
                print('\nLogin successful!')
                self.username = username
                self.user_menu()

    # Main menu after login
    def user_menu(self):
        while True:
            print("""
    For account settings, select 1.
    For portfolio details, select 2.
    To return to previous menu, select 3.
""")
            try:
                option = int(input('Your option: '))
                if option == 1:
                    self.user_submenu()
                elif option == 2:
                    portfolio = Portfolio()
                    portfolio.portfolio_menu(self.username)
                elif option == 3:
                    print('\nExit submenu...')
                    return
                else:
                    print('\nSelected option is not valid.')
            except ValueError:
                print(self.valoare_invalida)

    # Submenu user
    def user_submenu(self):
        cursor.execute(f"SELECT user_tag FROM users WHERE user_login = '{self.username}'")
        self.tag = cursor.fetchone()[0]

        while True:
            if self.tag in ['User', 'Photographer']: 
                print("""
    To view your account details, select 1.
    To change password, select 2.
    To change the name, select 3.
    To change user type, select 4.
    To return to previous menu, select 5.
""")
                sub_menu = {
                    1: self.user_details,
                    2: self.change_password,
                    3: self.change_name,
                    4: self.change_tag
                }
                try:
                    option = int(input('Your option: '))
                    if option in range(1,5):
                        sub_menu[option]()
                    elif option == 5:
                        print('\nExiting submenu...')
                        return
                    else:
                        print('\nSelected option is not valid.')    
                except ValueError:
                    print(self.valoare_invalida)

            elif self.tag == 'Admin':
                print("""
    To view your account details, select 1.
    To change password, select 2.
    To change the name, select 3.
    To view all users, select 4.
    To delete a user, select 5.
    To create a new user, select 6.
    To return to previous menu, select 7.
    """)
                sub_menu = {
                    1: self.user_details,
                    2: self.change_password,
                    3: self.change_name,
                    4: self.display_users,
                    5: self.user_delete,
                    6: self.user_create
                }
                try:
                    option = int(input('Your option: '))
                    if option in range(1, 7):
                        sub_menu[option]()
                    elif option == 7:
                        print('\nExiting submenu...')
                        return
                    else:
                        print('\nSelected option is not valid.')
                except ValueError:
                    print(self.valoare_invalida)

    # Account details
    def user_details(self):
        cursor.execute(f"SELECT user_first_name, user_last_name, user_tag FROM users WHERE user_login = '{self.username}'")
        detail = cursor.fetchone()
        print(f"""
    Username: {self.username}
    First name: {detail[0]}
    Last name: {detail[1]}
    User type: {detail[2]}
""")
    
    # Account settings
    def change_password(self):
        print("""
    ******************
    * PASSWORD RESET *
    ******************
""")
        cursor.execute("UPDATE users SET user_password = ? WHERE user_login = ?", (self.create_password(), self.username))
        connect.commit()
        print('\nPassword has been changed.')

    def change_name(self):
        while True:
            try:
                option = int(input("""
    To change last name, select 1.
    To change first name, select 2.
    To cancel, select 3.

Your option: """))
                if option == 1:
                    cursor.execute("UPDATE users SET user_last_name = ? WHERE user_login = ?", (self.create_last_name(), self.username))
                elif option == 2:
                    cursor.execute("UPDATE users SET user_first_name = ? WHERE user_login = ?", (self.create_first_name(), self.username))
                elif option == 3:
                    print('\nCancelling...')
                    return
                else:
                    print('\nSelected option is not valid.')
            except ValueError:
                print(self.valoare_invalida)
            cursor.execute(f"SELECT user_first_name, user_last_name FROM users WHERE user_login = '{self.username}'")
            db_name_t = cursor.fetchone()
            name = db_name_t[0] + ' ' + db_name_t[1]
            cursor.execute("UPDATE portfolios SET portfolio_photographer_name = ? WHERE portfolio_username = ?", (name, self.username))
            connect.commit()
            print('\nName has been changed.')

    def change_tag(self):
        print("""
    ****************
    * CHANGING TAG *
    ****************
""")
        cursor.execute("UPDATE users SET user_tag = ? WHERE user_login = ?", (self.create_tag(), self.username))
        connect.commit()
        print('\nUser type has been changed.')

    # Admin functions
    # Display users
    @staticmethod
    def display_users():
        ids = [user[0] for user in cursor.execute("SELECT user_id FROM users")]
        users = [user[0] for user in cursor.execute("SELECT user_login FROM users")]
        for id, user in zip(ids, users):
            print(f'Id: {id} -> Username: {user}')
                
    # Delete user
    @staticmethod
    def user_delete():
        User.display_users()

        check = False
        while not check:
            try:
                option = int(input('Which user would you like to delete? (Id, for ex. "2"): '))
                check_if_exist = [user[0] for user in cursor.execute("SELECT user_id FROM users")]
                if option not in check_if_exist:
                    print("\nSelected user doesn't exist.")
                else:
                    check = True
                    cursor.execute("DELETE FROM users WHERE user_id = {}".format(option))
                    connect.commit()
                    print('\nUser has been deleted.')
                    return
            except ValueError:
                print(__class__.valoare_invalida)

# if __name__ == '__main__':
#     test = User()
#     # test.user_create()
#     test.user_login()
#     pass