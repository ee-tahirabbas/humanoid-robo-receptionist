import tkinter as tk
from PIL import Image, ImageTk

def create_button(parent, text):
    # Helper function to create a button with text
    return tk.Button(parent, text=text, padx=10, pady=5, bg='slate gray', fg='white')  # Adjust colors as needed

def create_label(parent, text):
    # Helper function to create a label with text
    return tk.Label(parent, text=text, padx=10, pady=5, bg='slate gray', fg='white')  # Adjust colors as needed



root = tk.Tk()
root.geometry('700x550+100+30')
root.title('ChatBot created by Sheri')
root.config(bg='slate gray')

# Load the images
uni_building_photo = Image.open('uni1.png')
uni_building_image = ImageTk.PhotoImage(uni_building_photo)

# Create a label for the university building image
uni_building_label = tk.Label(root, image=uni_building_image)
uni_building_label.pack()

# Load the transparent UET logo
uet_logo_photo = Image.open('uet.png')
uet_logo_image = ImageTk.PhotoImage(uet_logo_photo)

# Create a label for the UET logo and position it over the university building image
uet_logo_label = tk.Label(uni_building_label, image=uet_logo_image, bd=0)
uet_logo_label.place(x=5, y=5)  # The (x, y) position is relative to the university building label


# Left panel
left_panel = tk.Frame(root, bg='darkgray', width=190)  # Adjust the width as needed
left_panel.pack(side=tk.LEFT, fill=tk.Y, expand=False)
left_panel.pack_propagate(False)  # Prevent the frame from resizing to fit its children


# "Chatbot" label at the top of the left panel
chatbot_label = create_label(left_panel, "Chatbot")
chatbot_label.pack(fill=tk.X, padx=10, pady=5)

# Buttons below "Chatbot" label
button_texts = ["User Guide", "Query Section", "Feedback"]
buttons = [create_button(left_panel, text) for text in button_texts]
for button in buttons:
    button.pack(fill=tk.X, padx=10, pady=5)

# Load the new PNG image that you want to display below the buttons of the left panel
robo_png_photo = Image.open('robo.png')  # Update the path to your new image file
robo_png_image = ImageTk.PhotoImage(robo_png_photo)

# Create a label for the new PNG image within the left panel below the buttons
robo_png_label = tk.Label(left_panel, image=robo_png_image, bd=0)
robo_png_label.pack(pady=2)  # Add some padding to space it out from the buttons


# Set the central content area
content_area = tk.Text(root, height=20, width=50)
content_area.pack(pady=20)

# Set the bottom panel for the "Enable Auto Detection" button
bottom_panel = tk.Frame(root, bg='white', height=60)  # Adjust color and height as needed
bottom_panel.pack(side=tk.BOTTOM, fill=tk.X)

# Add "Enable Auto Detection" button to the bottom panel
auto_detect_button = create_button(bottom_panel, "Enable Auto Detection")
auto_detect_button.place(relx=0.5, rely=0.5, anchor='center')  # Center the button


# Keep a reference to the images to prevent garbage collection
root.uni_building_image = uni_building_image
root.uet_logo_image = uet_logo_image
root.robo_png_image = robo_png_image

root.mainloop()
