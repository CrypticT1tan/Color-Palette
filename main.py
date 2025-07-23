from tkinter import *
from tkinter.filedialog import askopenfilename
import PIL
from PIL import Image, ImageTk
import sys
import os

class ColorPalette:
    def __init__(self):
        # Main Program Window Setup
        self.window = Tk()
        self.window.title("Color Palette Generator")

        # Constants For Program
        self.font = "Futura"
        self.title_size = 30
        self.code_size = 15
        self.palette_length = 8
        self.image_size = 450

        # For displaying the image (initially a placeholder image)
        self.current_image_pil = Image.open(self.resource_path("start.png"))
        self.current_image_rgba = self.current_image_pil.convert("RGBA")
        self.current_image = ImageTk.PhotoImage(self.current_image_pil)

        # Title Stuff
        self.title_label = Label(text="Color Palette Generator", font=(self.font, self.title_size, "bold"), justify="center")
        self.title_label.grid(row=0, column=0, columnspan=self.palette_length)

        # Image Path Text Entry and Button
        self.image_path_entry = Entry(self.window, width=50, state="readonly")
        self.image_path_entry.grid(row=1, column=0, columnspan=self.palette_length)
        self.image_display_button = Button(text="Browse Image Files", command=self.find_image)
        self.image_display_button.grid(row=2, column=0, columnspan=self.palette_length)

        # Setup Canvas
        self.canvas = Canvas(self.window, height=self.image_size, width=self.image_size)
        self.canvas.grid(row=3, column=0, columnspan=self.palette_length)
        self.canvas.create_image(self.image_size / 2, self.image_size / 2, image=self.current_image)

        # Create Initial Color Palette (Consists of Frames)
        self.hex_label_list = []  # List of hex code labels for each color
        self.color_frame_list = [] # List of frames that hold colors
        for i in range(self.palette_length):
            self.hex_label = Label(self.window, font=(self.font, self.code_size))
            self.hex_label.grid(row=4, column=i)
            self.hex_label_list.append(self.hex_label)
            self.color_frame = Frame(self.window, bg="white", borderwidth=3, width=128, height=128, relief="solid", padx=0,
                                pady=0)
            self.color_frame.grid(row=5, column=i)
            self.color_frame_list.append(self.color_frame)

    # Functions Used By Program
    def get_pixel_color(self, event, rgba) -> None:
        """
        Function to get color of a pixel on the current displayed image
        :param event: the event of clicking on a canvas pixel
        :param rgba: the rgba image displayed on the canvas
        :return: None
        """
        # Get the pixel's position and the hex code at the position
        # Sometimes the canvas has an issue where clicking the edge of the canvas results in an IndexError
        try:
            pixel_pos = (event.x, event.y)
            pixel_color = self.rgba_to_hex(rgba.getpixel(pixel_pos)) # Converts the pixel's rgb value to hex code
            for i in range(self.palette_length - 1, 0, -1): #
                current_label = self.hex_label_list[i]
                next_label = self.hex_label_list[i - 1]
                current_label.config(text=next_label.cget("text"))
                current_frame = self.color_frame_list[i]
                next_frame = self.color_frame_list[i - 1]
                current_frame.config(bg=next_frame.cget("bg"))
            self.hex_label_list[0].config(text=pixel_color)
            self.color_frame_list[0].config(bg=pixel_color)
        except IndexError:
            pass

    def rgba_to_hex(self, rgba) -> str:
        """
        Converts a rgba tuple full of integer values into a hexadecimal code string
        :param rgba: the rgba tuple to be converted (rgba accounts for images with transparency)
        :return: the hexadecimal string
        """
        # r = red, b = blue, g = green, a = alpha
        r, g, b, a = rgba
        # :02x = 2-digit hex, zero-padding if needed
        return f'#{r:02x}{g:02x}{b:02x}'

    def find_image(self) -> None:
        """
        Finds the image based on the image file path from the text entry and displays it on the canvas
        :return: None
        """
        try:
            # Bring up user file system to allow them to open a file
            image_file_path = askopenfilename()
            # Run the code inside if the image_file_path is not None
            if image_file_path:
                # Write the image file path into the text entry
                self.image_path_entry.config(state="normal") # Allow text entry to be edited
                self.image_path_entry.delete(0, END)
                self.image_path_entry.insert(0, image_file_path)
                self.image_path_entry.config(state="readonly") # Set it back to read only
                # Display the image on the canvas
                self.current_image_pil = Image.open(self.resource_path(self.image_path_entry.get())).resize((self.image_size, self.image_size))
                self.current_image_rgba = self.current_image_pil.convert("RGBA")
                self.current_image = ImageTk.PhotoImage(self.current_image_pil)
                self.canvas.create_image(self.image_size / 2, self.image_size / 2, image=self.current_image)
                # The canvas will run the function get_pixel_color() any time the left mouse button clicks on it
                # lambda event = can take in arguments for an event function
                self.canvas.bind("<Button-1>", func=lambda event: self.get_pixel_color(event, self.current_image_rgba))
                # Reset the palette when a new image is displayed
                for i in range(self.palette_length):
                    self.color_frame_list[i].config(bg="white") # Reset color frames
                    self.hex_label_list[i].config(text="") # Reset hex code labels
        except (IsADirectoryError, PIL.UnidentifiedImageError, TimeoutError): # In the case a directory/non-image file is selected
            # Remove the invalid directory from the text entry
            self.image_path_entry.config(state="normal")
            self.image_path_entry.delete(0, END)
            self.image_path_entry.config(state="readonly")

    def resource_path(self, relative_path):
        """
        Function to get the absolute path to the images/sounds for PyInstaller to use
        :param relative_path: the relative path of the resource
        :return: the absolute path of the resource
        """
        try:
            # PyInstaller temporary folder
            base_path = sys._MEIPASS
        # # In cases where the .py file is run instead of the app (_MEIPASS doesn't exist)
        except AttributeError:
            # Sets the base_path to the current working directory
            base_path = os.path.abspath(".")
        # The absolute path of the resource passed in is returned
        return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    color_palette = ColorPalette()
    # Prevent the window from closing immediately upon reaching the end of this file
    # Loops back to the top
    color_palette.window.mainloop()

