import tkinter as tk
from tkinter import messagebox


def show_confirmation():
    # Show a confirmation popup
    response = messagebox.askyesno("Confirm Save", "Are you sure you want to save?")
    
    if response:
        print("Data saved successfully!")
    else:
        print("Save canceled.")


# Create the main app window
root = tk.Tk()
root.title("Save Confirmation Example")
root.geometry("400x200")
show_contour = False

# Add a label and save button
tk.Label(root, text="Click save to trigger confirmation:", font=("Helvetica", 14)).pack(pady=20)

save_button = tk.Button(root, text="Save", command=show_confirmation, bg="green", fg="white", padx=20, pady=10)
save_button.pack()
contour_button = tk.Button(root, 
                           text="Hide Contour" if show_contour else "Show Contour",
                           command=lambda: toggle_contour(contour_button))

def toggle_contour(button):
    print(show_contour)
    show_contour = not show_contour
    button.config(text="Hide Contour" if show_contour else "Show Contour")

contour_button.pack()
# Start the Tkinter event loop
root.mainloop()

# Let me know if you want me to tweak anything! 🚀
