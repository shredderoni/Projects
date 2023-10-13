import tkinter as tk
import tkinter.font as font

def convert():
    try:
        input_value = float(input_entry.get())
        value_unit = unit_var.get()

        result = input_value * units[value_unit]
        result_final.config(text=f"{result}")
    except ValueError:
        result_final.config(text="Please enter a number!")
    except KeyError:
        result_final.config(text="Can't convert that!")

units = {
    ('Pounds -> Kilograms'): 0.453592,
    ('Kilograms -> Pounds'): 2.20462,
    ('Inches -> Centimeters'): 2.54,
    ('Centimeters -> Inches'): 0.393701
}

# Main Window
window = tk.Tk()
window.geometry("500x300")
window.title("Unit Converter")
window.configure(bg = 'lightblue2')

# Fonts
font1 = font.Font(family = 'Verdana', size = '30')
font2 = font.Font(family = 'Verdana', size = '16')
font3 = font.Font(family = 'Verdana', size = '12')

# Title
main = tk.Label(window, text = 'Unit Converter', bg = 'lightblue2')
main['font'] = font1
main.place(relx = '0.48', rely = '0.1', anchor = 'center')

# Input
input_label = tk.Label(window, text = 'Value:', bg = 'lightblue2')
input_label['font'] = font2
input_label.place(relx = '0.3', rely = '0.4', anchor = 'e')

input_entry = tk.Entry(window)
input_entry['font'] = font3
input_entry.place(relx = '0.32', rely = '0.4', anchor = 'w')

# Unit
unit_label = tk.Label(window, text = 'Unit:', bg = 'lightblue2')
unit_label['font'] = font2
unit_label.place(relx = '0.3', rely = '0.55', anchor = 'e')

unit_var = tk.StringVar(window)
unit_var.set(('Pounds -> Kilograms'))
unit_var_option = tk.OptionMenu(window, unit_var, *units)
unit_var_option['font'] = font3
unit_var_option.place(relx = '0.32', rely = '0.55', anchor = 'w')

# Convert Button
convert_button = tk.Button(window, text = 'Convert', command = convert)
convert_button.place(relx = '0.48', rely = '0.7', anchor = 'center')

# Result
result_label = tk.Label(window, text = 'Result:', bg = 'lightblue2')
result_label['font'] = font2
result_label.place(relx = '0.3', rely = '0.85', anchor = 'e')

result_final = tk.Label(window, bg = 'lightblue2', fg = 'red')
result_final['font'] = font2
result_final.place(relx = '0.32', rely = '0.85', anchor = 'w')

# Main Loop
window.mainloop()