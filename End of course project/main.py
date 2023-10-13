from user import User
import sys

print("""
    *******************
    *    WELCOME !    *
    *******************
""")
while True:
    print("""
    Login, select 1.
    Register, select 2.
    Exit program, select 3.
""")
    try:
        option = int(input('Your option: '))
        if option == 1:
            login = User()
            login.user_login()
        elif option == 2:
            create = User()
            create.user_create()
        elif option == 3:
            print('\nExiting program...')
            sys.exit()
        else:
            print('\nYour selected option is not available.')
    except ValueError:
        print(User.valoare_invalida)