import sqlite3 as sql
import os, shutil, uuid
from os.path import exists
from PIL import Image as PILImage
from string import ascii_letters
from datetime import date

connect = sql.connect("data.db")
cursor = connect.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name NVARCHAR(60),
            image_data NVARCHAR(255),
            image_settings NVARCHAR(255),
            image_portfolio_title NVARCHAR(60),
            image_date NVARCHAR(255),
            image_portfolio_id INTEGER,
            image_username NVARCHAR(60)
        )
        """)
connect.commit()
# FOREIGN KEY (image_portfolio_id) REFERENCES portfolios (portfolio_id)

class Image:
    characters = ascii_letters + ' '
    valoare_invalida = """
* *  ********************************  * *
 *    You entered an invalid option!    *
* *  ********************************  * *
"""
    def __init__(self):
        self.name = ''
        self.image = ''
        self.settings = ''
        self.title = ''
        self.id = ''
        self.username = ''

    # Select image and insert into database
    @staticmethod
    def create_name():
        check = False
        while not check:
            name = input('\nSelect a name for the image: ')
            if set(name).difference(__class__.characters):
                print('\nThe name can only contain letters.')
            else:
                check = True
                return name

    @staticmethod
    def create_image():
        check = False
        while not check:
            image = input('\nSelect image (path to image): ')
            if not exists(image):
                print('\nImage doesn\'t exist or path is wrong.')
            else:
                check = True
                filename = str(uuid.uuid4())
                shutil.copy(image, f'{os.getcwd()}\\images\\{filename}.jpg')
                return f'{os.getcwd()}\\images\\{filename}.jpg'
            
    @staticmethod
    def create_settings():
        settings = input('\nEnter camera settings for this image: ')
        return settings


    def image_insert(self):
        day = date.today()
        day_modified = day.strftime('%B %d, %Y')
        cursor.execute("""
        INSERT INTO images (image_name, image_data, image_settings, image_portfolio_title, image_date, image_portfolio_id, image_username) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.name, self.image, self.settings, self.title, day_modified, self.id, self.username))
        connect.commit()
        print('\nImage was added successfully.')

    def image_create(self):
        cursor.execute(f"SELECT portfolio_title FROM portfolios WHERE portfolio_id = '{self.id}'") 
        title = cursor.fetchone()[0]
        self.name = self.create_name()
        self.image = self.create_image()
        self.settings = self.create_settings()
        self.title = title
        self.image_insert()

    def image_menu(self, portfolio_id, username):
        self.id = portfolio_id
        self.username = username
        cursor.execute(f"SELECT user_tag FROM users WHERE user_login = '{self.username}'")
        tag = cursor.fetchone()[0]
        menu = {
            1: self.image_catalog,
            2: self.image_submenu
        }
        while True:
            if tag == 'User':
                print("""
    To display the images, select 1.
    To return to previous menu, select 2.
""")
                try:
                    option = int(input('Your option: '))
                    if option == 1:
                        menu[option]()
                    elif option == 2:
                        print('Exiting submenu...')
                        return
                except ValueError:
                    print(self.valoare_invalida)
            elif tag in ['Photographer', 'Admin']:
                print("""
    To display the images, select 1.
    For more options, select 2.
    To return to previous menu, select 3.
""")
                try:
                    option = int(input('Your option: '))
                    if option == 1:
                        menu[option]()
                    elif option == 2:
                        cursor.execute(f"SELECT portfolio_username FROM portfolios WHERE portfolio_id = '{self.id}'")
                        data = cursor.fetchone()[0]
                        if data != self.username:
                            print('\nSelected portfolio doesn\'t belong to you. Returning...')
                            return
                        menu[option]()
                    elif option == 3:
                        print('\nExiting submenu...')
                        return
                    else:
                        print('\nSelected option is not valid.')
                except ValueError:
                    print(self.valoare_invalida)

    def image_submenu(self):
        menu = {
            1: self.image_create,
            2: self.image_name_edit,
            3: self.image_settings_edit,
            4: self.image_delete,
        }
        while True:
            print("""
    To upload an image, select 1.
    To change the name of an image, select 2.
    To change the camera settings of an image, select 3.
    To delete an image, select 4.
    To return to previous menu, select 5.
""")
            try:
                option = int(input('Your option: '))
                if option in range(1,5):
                    menu[option]()
                elif option == 5:
                    print('\nExiting submenu...')
                    return
                else:
                    print('\nSelected option is not valid.')
            except ValueError:
                print(self.valoare_invalida)
    
    # View image
    def image_catalog(self):
        cursor.execute(f"SELECT image_id, image_name, image_settings, image_portfolio_title, image_date FROM images WHERE image_portfolio_id = '{self.id}'")
        data = cursor.fetchall()
        if len(data) == 0:
            print('\nThis portfolio doesn\'t contain any images.')
            return
        else:
            for value in data:
                print(f'\nId: {value[0]}\nName: {value[1]}\nCamera settings: {value[2]}\nPortfolio: {value[3]}\nDate: {value[4]}')
        while True:
            try:
                select = int(input('\nWhich image would you like to see?: '))
                cursor.execute(f"SELECT image_id FROM images WHERE image_id = '{select}'")
                if select != cursor.fetchone()[0]:
                    print('Selected image is not available.')
                else:
                    cursor.execute(f"SELECT image_data FROM images WHERE image_id = '{select}'")
                    image = PILImage.open(f"{cursor.fetchone()[0]}")
                    image.show()
                    return
            except ValueError:
                print(self.valoare_invalida)
            except KeyboardInterrupt:
                return

    def image_data(self):
        cursor.execute(f"SELECT image_id, image_name, image_settings, image_portfolio_title, image_date \
                                                 FROM images WHERE image_username = '{self.username}'")
        for value in cursor.fetchall():
            print(f'\nId: {value[0]}\nName: {value[1]}\nSettings: {value[2]}\nPortfolio: {value[3]}\nDate: {value[4]}')

    def image_name_edit(self):
        self.image_data()
        while True:
            print("""
    To continue, select 1.
    To cancel, select 2.
""")
            try:
                option = int(input('Your option: '))
                if option == 1:
                    while True:
                        try:
                            select = int(input('Select an image: '))
                            if select not in [id[0] for id in cursor.execute(f"SELECT image_id FROM images WHERE image_username = '{self.username}'")]:
                                print('\nSelected image is not available.')
                            else:
                                break
                        except ValueError:
                            print(self.valoare_invalida)
                        except KeyboardInterrupt:
                            return
                    cursor.execute("UPDATE images SET image_name = ? WHERE image_id = ?", (self.create_name(), select))
                    connect.commit()
                    print('\nName has been changed.')
                elif option == 2:
                    print('\nCancelling...')
                    return
                else:
                    print('\nSelected option is not valid.')
            except ValueError:
                print(self.valoare_invalida)

    def image_settings_edit(self):
        self.image_data()
        while True:
            print("""
    To continue, select 1.
    To cancel, select 2.
""")
            try:
                option = int(input('Your option: '))
                if option == 1:
                    while True:
                        try:
                            select = int(input('Select an image: '))
                            if select not in [id[0] for id in cursor.execute(f"SELECT image_id FROM images WHERE image_username = '{self.username}'")]:
                                print('\nSelected image is not available')
                            else:
                                break
                        except ValueError:
                            print(self.valoare_invalida)
                        except KeyboardInterrupt:
                            return
                    cursor.execute("UPDATE images SET image_settings = ? WHERE image_id = ?", (self.create_settings(), select))
                    connect.commit()
                    print('\nCamera settings have been updated')
                elif option == 2:
                    print('\nCancelling...')
                    return
                else:
                    print('\nSelected image is not available.')
            except ValueError:
                print(self.valoare_invalida)


    def image_delete(self):
        self.image_data()
        while True:
            print("""
    To continue, select 1.
    To cancel, select 2.
""")
            try:
                option = int(input('Your option: '))
                if option == 1:
                    while True:
                        try:
                            select = int(input('\nSelect an image: '))
                            if select not in [id[0] for id in cursor.execute(f"SELECT image_id FROM images WHERE image_username = '{self.username}'")]:
                                print('\nSelected image is not available.')
                            else:
                                break
                        except ValueError:
                            print(self.valoare_invalida)
                        except KeyboardInterrupt:
                            return
                    cursor.execute(f"DELETE FROM images WHERE image_id = '{select}'")
                    connect.commit()
                    print('\nImage has been deleted.')
                elif option == 2:
                    print('\nCancelling...')
                    return
                else:
                    print('\nSelected option is not available.')
            except ValueError:
                print(self.valoare_invalida)

if __name__ == '__main__':
    pass