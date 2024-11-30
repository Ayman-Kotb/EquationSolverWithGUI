from tkinter import *
from tkinter import messagebox
import numpy as np
from numpy import *

unknowns = 0  # Global variable to store the number of unknowns
entries = []  # To hold the input entries for coefficients and constants

def nxt(frame):
    """Raise the specified frame."""
    frame.tkraise()

def noOfUnknownsSubmitButton(frame):
    """Process the number of unknowns."""
    global unknowns
    try:
        unknowns = int(entry.get())
        if unknowns <= 0:
            raise ValueError("Number of unknowns must be positive.")
        create_input_fields(frame)
        nxt(frame)
    except ValueError as e:
        messagebox.showerror(title="ERROR", message="Please enter a valid positive integer for unknowns.")

def create_input_fields(frame):
    """Dynamically create input fields for the coefficients and constants."""
    global entries
    # Clear previous entries if any
    # for widget in frame.winfo_children():
    #     widget.destroy()
    entries = []

    Label(frame, text="Enter coefficients and constants for each equation:", font=("JetBrains Mono", 22), bg="#B2C0FA").grid(row = 0 , column=1 , columnspan=2*unknowns+2 , pady = 20 )
    
    for i in range(unknowns): 
        r=0
        row_entries = []
        Label(frame, text=f"Equation {i + 1}:", font=("JetBrains Mono", 20), bg="#B2C0FA").grid(row=i+1, column=0)
        for j in range(unknowns):
            lbl = Label(frame, text=f"x{j + 1}:", font=("JetBrains Mono", 18), bg="#B2C0FA")
            lbl.grid(row = i+1, column= r+1)
            ent = Entry(frame, font=("JetBrains Mono", 18), width=5)
            ent.grid(row = i+1, column= r+2)
            row_entries.append(ent)
            r= r+2 
        lbl1 = Label(frame, text="=", font=("JetBrains Mono", 18), bg="#B2C0FA")
        lbl1.grid(row = i+1 , column =r+1)
        const_entry = Entry(frame, font=("JetBrains Mono", 18), width=5)
        const_entry.grid(row = i+1, column=r+2)
        row_entries.append(const_entry)
        entries.append(row_entries)
        Frame(frame).grid(row = i+1 , column=r+3)  # Add spacing between rows

    Button(frame, text="Solve", font=("JetBrains Mono", 16), bg="#B2C0FA", command=solve_equations).grid(row = unknowns+1 , column= 1 , columnspan=2*unknowns+2 , pady=20)

def solve_equations():
    """Solve the system of equations."""
    try:
        coefficients = []
        constants = []
        for row in entries:
            coefficients.append([float(e.get()) for e in row[:-1]])  # Get all coefficients
            constants.append(float(row[-1].get()))  # Get the constant
        coefficients = np.array(coefficients)
        constants = np.array(constants)

        # Solve using numpy's linear algebra module
        solution = np.linalg.solve(coefficients, constants)

        # Display the result
        result_text = "\n".join([f"x{i + 1} = {value:.4f}" for i, value in enumerate(solution)])
        messagebox.showinfo("Solution", result_text )
    except ValueError:
        messagebox.showerror("Input Error", "Please ensure all fields are filled with numeric values.")
    except np.linalg.LinAlgError:
        messagebox.showerror("Math Error", "The system of equations has no unique solution.")

# Main window setup
main = Tk()
main.geometry("800x800")
main.title("Equations Solver")
main.config(background="#B2C0FA")

# Container for frames
container = Frame(main)
container.config(background="#B2C0FA")
container.pack(fill="both", expand=True)

# Frames for each "page"
window = Frame(container, bg="#B2C0FA")
window2 = Frame(container, bg="#B2C0FA")
window3 = Frame(container, bg="#B2C0FA")

# Add frames to container
for frame in (window, window2, window3):
    frame.grid(row=0, column=0, sticky="nsew")

# Page 1 - Welcome screen
Label(window, text="Welcome to the Equations Solver!", font=("JetBrains Mono", 24, 'bold'), bg="#B2C0FA").grid(row=0 , column = 2,  columnspan=2 ,pady=20)
Button(window, text="NEXT", font=("JetBrains Mono", 20), bg="#B2C0FA", command=lambda: nxt(window2)).grid(row=1 , column=2 ,columnspan=1 , pady=20)

# Page 2 - Input number of unknowns
Label(window2, text="Enter the number of unknowns:", font=("JetBrains Mono", 21), bg="#B2C0FA").pack(pady=20)
entry = Entry(window2, font=("JetBrains Mono", 21))
entry.pack(pady=10)
Button(window2, text="Submit", font=("JetBrains Mono", 21), bg="#B2C0FA", command=lambda: noOfUnknownsSubmitButton(window3)).pack()

# Page 3 - Input coefficients and constants
window3.config(bg="#B2C0FA")

# Start the application
window.tkraise()
main.mainloop()
