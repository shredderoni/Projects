import customtkinter as ctk
import random, os
from PIL import Image

activities = ["Cooking/Baking", "Crochet", "Origami", "Gaming", "Museum Tour"]

countries = ["Afghanistan","Albania","Algeria","Andorra","Angola","Antigua and Barbuda","Argentina","Armenia",
            "Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium", 
            "Belize","Benin","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Brazil","Brunei","Bulgaria",
            "Burkina Faso","Burundi","Côte d'Ivoire","Cabo Verde","Cambodia","Cameroon","Canada","Central African Republic",
            "Chad","Chile","China","Colombia","Comoros","Congo","Costa Rica","Croatia","Cuba","Cyprus",
            "Czech Republic","Democratic Republic of the Congo","Denmark","Djibouti","Dominica","Dominican Republic",
            "Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Eswatini","Ethiopia",
            "Fiji","Finland","France","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea",
            "Guinea-Bissau","Guyana","Haiti","Holy See","Honduras","Hungary","Iceland","India","Indonesia","Iran","Iraq",
            "Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kiribati","Kuwait","Kyrgyzstan",
            "Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Madagascar",
            "Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia",
            "Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar (formerly Burma)","Namibia","Nauru",
            "Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","North Korea","North Macedonia","Norway","Oman",
            "Pakistan","Palau","Palestine State","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal",
            "Qatar","Romania","Russia","Rwanda","Saint Kitts and Nevis","Saint Lucia","Saint Vincent and the Grenadines","Samoa",
            "San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia",
            "Slovenia","Solomon Islands","Somalia","South Africa","South Korea","South Sudan","Spain","Sri Lanka","Sudan","Suriname",
            "Sweden","Switzerland","Syria","Tajikistan","Tanzania","Thailand","Timor-Leste","Togo","Tonga","Trinidad and Tobago",
            "Tunisia","Turkey","Turkmenistan","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States of America",
            "Uruguay","Uzbekistan","Vanuatu","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"]

museum_tours = ["The Louvre", "Solomon R. Guggenheim Museum", "Smithsonian National Museum of Natural History", 
                "Van Gogh Museum", "Getty Museum", "The Vatican Museum", "Thyssen-Bornemisza Museum", "Georgia O’Keeffe Museum", 
                "National Museum of Anthropology, Mexico City", "British Museum, London", "NASA", "National Women's History Museum", 
                "Metropolitan Museum of Art", "High Museum of Art, Atlanta", "Detroit Institute of Arts", "Rijksmuseum, Amsterdam", 
                "National Museum of the United States Air Force", "MoMA (The Museum of Modern Art)", "Museum of Fine Arts, Boston"]

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Date Night Picker")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(width=False, height=False)

        #Radio button frame
        self.radio_frame = IncludeCountryFrame(self, title="Do you want to include a country?", values=["Yes", "No"])
        self.radio_frame.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew", rowspan=2)

        #Pick button
        self.button_1 = ctk.CTkButton(self, text="Pick date :3", command=self.date_picker)
        self.button_1.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=3)

        #Results activity
        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew", rowspan=2)

        self.title = ctk.CTkLabel(self.frame, text="Results", fg_color="gray30", corner_radius=6, width=200)
        self.title.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.label_activity = ctk.CTkLabel(self.frame, text="")
        self.label_activity.grid(row=1, column=0, padx=10, pady=10, rowspan=3)

    def date_picker(self):
        try:
            self.frame_extra.destroy()
        except:
            pass

        activity_nr = self.radio_frame.get_slider_value()
        activity = random.sample(activities, activity_nr)

        self.activity_picker(activity_nr, activity)

        if self.radio_frame.get_radio_value() == 1 or "Museum Tour" in activity:
            self.frame_extra = ctk.CTkFrame(self)
            self.frame_extra.grid(row=0, column=2, padx=(0, 10), pady=(10, 0), sticky="nsew")

        if self.radio_frame.get_radio_value() == 1:
            self.country_pick = random.choice(countries)
            
            self.title_country = ctk.CTkLabel(self.frame_extra, text="Country is", fg_color="gray30", corner_radius=6, width=200)
            self.title_country.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

            cur_dir = os.getcwd()
            try:
                self.image = ctk.CTkImage(dark_image=Image.open(f"{cur_dir}\\flags\\{self.country_pick}.png"), size=(30, 23))
            except FileNotFoundError:
                pass
            self.image_label = ctk.CTkLabel(self.frame_extra, image=self.image, text="")
            self.image_label.grid(row=1, column=0, padx=10, pady=10)

            self.label_country = ctk.CTkLabel(self.frame_extra, text=f"{self.country_pick}")
            self.label_country.grid(row=1, column=1, padx=10, pady=10)

        if "Museum Tour" in activity:
            self.title_museum = ctk.CTkLabel(self.frame_extra, text="Museum Tour is", fg_color="gray30", corner_radius=6, width=200)
            self.title_museum.grid(row=2, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

            self.museum = ctk.CTkLabel(self.frame_extra, text=f"{random.choice(museum_tours)}")
            self.museum.grid(row=3, column=0, padx=10, pady=(10, 0), columnspan=2)

    def activity_picker(self, activity_nr, activity):
        if activity_nr == 1:
            self.label_activity.configure(text=f"{activity[0]}")
        elif activity_nr == 2:
            self.label_activity.configure(text=f"{activity[0]}\n\n{activity[1]}")
        elif activity_nr == 3:
            self.label_activity.configure(text=f"{activity[0]}\n\n{activity[1]}\n\n{activity[2]}")


class IncludeCountryFrame(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.title = title
        self.values = values
        
        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=2, column=0, padx=5, pady=(0, 10), sticky="ew")

        self.radio_var = ctk.IntVar(value=2)
        for i, value in enumerate(self.values):
            radiobutton = ctk.CTkRadioButton(self, text=value, variable=self.radio_var, value=i+1)
            radiobutton.grid(row=i+3, column=0, padx=10, pady=(0, 10), sticky="w")

        self.activities = ctk.CTkLabel(self, text="Number of activities - (1)", fg_color="gray30", corner_radius=6)
        self.activities.grid(row=0, column=0, padx=5, pady=(5, 10), sticky="ew")

        self.slider_var = ctk.IntVar(value=1)
        self.slider = ctk.CTkSlider(self, from_=1, to=3, number_of_steps=2, variable=self.slider_var, command=self.update_slider_value)
        self.slider.grid(row=1, column=0, padx=5, pady=(0, 30), sticky="ew")

    def get_radio_value(self):
        return self.radio_var.get()
    
    def update_slider_value(self, value):
        self.activities.configure(text=f"Number of activities - ({int(value)})")

    def get_slider_value(self):
        return self.slider_var.get()

app = App()
app.mainloop()