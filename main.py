from tkinter import Tk, Frame, Canvas, Button, Text, Label
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

window = Tk()
window.title("Watermark This!")
window.geometry("1500x900")

# Global variable to store drag data
drag_data = {}

def start_drag(event, item_id):
    # Record the starting position when mouse is pressed
    global drag_data
    drag_data = {'x': event.x, 'y': event.y, 'item_id': item_id}


def drag_motion(event):
    # Calculate the distance moved
    delta_x = event.x - drag_data['x']
    delta_y = event.y - drag_data['y']

    # Update the item's position
    canvas.move(drag_data['item_id'], delta_x, delta_y)

    # Update the starting position for the next movement
    drag_data['x'] = event.x
    drag_data['y'] = event.y


def create_label():

    watermark_text = text_box.get("1.0", "end-1c")

    # Create a new text item dynamically on the canvas
    new_label_id = canvas.create_text(100, 100, text=f"{watermark_text}", font=("Arial", 16))

    # Bind the mouse events to this new text item
    canvas.tag_bind(new_label_id, "<Button-1>", lambda event: start_drag(event, new_label_id))  # When mouse button is pressed
    canvas.tag_bind(new_label_id, "<B1-Motion>", drag_motion)  # When mouse is moved while pressed


# Configure window grid
window.columnconfigure((0, 1), weight=1, uniform="1")  # Left and Right columns take equal space
window.rowconfigure(0, weight=1)  # Row expands to take available height

# Create a red frame to hold the canvas (left side)
preview = Frame(window, bg='red')
preview.grid(column=0, row=0, sticky='nsew')  # Red frame expands

# Configure the grid inside the red frame (preview)
preview.columnconfigure(0, weight=1)  # Make sure the column inside red frame expands
preview.rowconfigure(0, weight=1)  # Make sure the row inside red frame expands

# Create a blue frame (right side) with a fixed width (no expansion)
settings = Frame(window, bg='blue')
settings.grid(column=1, row=0, sticky='nsew')  # Blue frame on the right, expands to fill its grid cell

# Create a canvas inside the red frame
canvas = Canvas(preview, bg='lightblue')
canvas.grid(column=0, row=0, sticky='nsew')  # Canvas fills the red frame


# Function to resize image to fit the canvas
def resize_image_to_canvas():
    file = askopenfilename()
    # Load the image (replace with your image path)
    image = Image.open(file)

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Resize the image to fit the canvas size
    resized_image = image.resize((canvas_width, canvas_height))
    photo = ImageTk.PhotoImage(resized_image)

    # Display the resized image on the canvas
    canvas.create_image(0, 0, anchor='nw', image=photo)

    # Keep a reference to avoid garbage collection
    canvas.image = photo  # This line prevents the image from being garbage collected

choose_file = Button(settings, text='Choose File', command=resize_image_to_canvas)
choose_file.grid(column = 0, row = 1, padx=10, pady=10)

text_box = Text(settings, width=40, height=3)
text_box.grid(column = 0, row = 2, padx = 10, pady = 10)

apply_watermark = Button(settings, text='Apply', command='')
apply_watermark.grid(column = 1, row = 2)

welcome_label = Label(settings, text="Hello and welcome", width=40, height=10, font=("Arial", 24))
welcome_label.grid(column = 0, row = 0, sticky = 'ew', columnspan=2)

# Button to create new labels during runtime
create_label_button = Button(settings, text="Create Label", font=("Arial", 14), command=create_label)
create_label_button.grid(column = 0, row = 3)


# Main loop
window.mainloop()
