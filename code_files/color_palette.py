# Third Party Imports
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

import PIL
from PIL import Image, ImageTk

# Local Application Imports
from util import resource_path


class ColorPalette:
    def __init__(self):
        # Constants For Program
        self.font = "Futura"
        self.title_size = 40
        self.code_size = 20
        self.palette_length = 8
        self.image_size = 450
        self.window_color = "#e6be94"
        self.title_color = "#654321"

        # Main Program Window Setup
        self.window = tk.Tk()
        self.window.title("Color Palette")
        self.window.config(bg=self.window_color)

        # For displaying the image (initially a placeholder image)
        self.current_image_pil = Image.open(resource_path("assets/canvas.png")).resize((self.image_size, self.image_size))
        self.current_image_rgba = self.current_image_pil.convert("RGBA")
        self.current_image = ImageTk.PhotoImage(self.current_image_pil)

        # Title Stuff
        self.title_label = tk.Label(text="Color Palette", font=(self.font, self.title_size, "bold"), justify="center",
                                    bg=self.window_color, fg=self.title_color)
        self.title_label.grid(row=0, column=0, columnspan=self.palette_length)

        # Image Path Text Entry and Button
        self.image_path_entry = tk.Entry(self.window, width=50, state="readonly", highlightbackground=self.window_color)
        self.image_path_entry.grid(row=1, column=0, columnspan=self.palette_length)
        self.image_display_button = tk.Button(text="Browse Image Files", command=self.find_image,
                                              highlightbackground=self.window_color)
        self.image_display_button.grid(row=2, column=0, columnspan=self.palette_length)

        # Setup Canvas
        self.canvas = tk.Canvas(self.window, height=self.image_size, width=self.image_size, borderwidth=0,
                                highlightbackground=self.window_color, bg=self.window_color)
        self.canvas.grid(row=3, column=0, columnspan=self.palette_length)
        self.canvas_image = self.canvas.create_image(self.image_size / 2, self.image_size / 2,
                                                     image=self.current_image)

        # Create Initial Color Palette (Consists of Frames)
        self.hex_label_list = []  # List of hex code labels for each color
        self.color_frame_list = [] # List of frames that hold colors
        for i in range(self.palette_length):
            hex_label = tk.Entry(self.window, font=(self.font, self.code_size), width=9, borderwidth=3,
                                 highlightbackground=self.window_color)
            hex_label.grid(row=4, column=i)
            hex_label.config(state="readonly", readonlybackground=self.window_color)
            self.hex_label_list.append(hex_label)
            color_frame = tk.Frame(self.window, bg=self.window_color, width=128, height=128,
                                   relief="solid", highlightbackground=self.window_color)
            color_frame.grid(row=5, column=i)
            self.color_frame_list.append(color_frame)

    # Functions Used By Program
    def get_pixel_color(self, event, rgba) -> None:
        """
        Function to get color of a pixel on the current displayed image
        :param event: the event of clicking on a canvas pixel
        :param rgba: the rgba image displayed on the canvas
        :return: None
        """
        # Sometimes the canvas has an issue where clicking the edge of the canvas results in an IndexError
        try:
            # Get the pixel's position and the hex code at the position
            pixel_pos = (event.x, event.y)
            pixel_color = self.rgba_to_hex(rgba.getpixel(pixel_pos)) # Converts the pixel's rgb value to hex code
            for i in range(self.palette_length - 1, 0, -1): # To push the least recent color over to the right
                current_label = self.hex_label_list[i]
                next_label = self.hex_label_list[i - 1]
                # Change the current label to the one on the left
                current_label.config(state="normal")
                current_label.delete(0, tk.END)
                current_label.insert(0, next_label.get())
                current_label.config(state="readonly")
                current_frame = self.color_frame_list[i]
                next_frame = self.color_frame_list[i - 1]
                # Change the current color to the one on the left
                current_frame.config(bg=next_frame.cget("bg"))
            # Put most recent pixel color onto the leftmost square
            self.hex_label_list[0].config(state="normal")
            self.hex_label_list[0].delete(0, tk.END)
            self.hex_label_list[0].insert(0, pixel_color)
            self.hex_label_list[0].config(state="readonly")
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
            # Run the code inside if the image_file_path is not None (if it exists)
            if image_file_path:
                # Try to open the new image file and display it
                self.current_image_pil = Image.open(image_file_path).resize((self.image_size, self.image_size))
                self.current_image_rgba = self.current_image_pil.convert("RGBA")
                self.current_image = ImageTk.PhotoImage(self.current_image_pil)
                self.canvas.itemconfig(self.canvas_image, image=self.current_image)
                # The canvas will run the function get_pixel_color() any time the left mouse button clicks on it
                # lambda event = can take in arguments for an event function
                self.canvas.bind("<Button-1>", func=lambda event: self.get_pixel_color(event, self.current_image_rgba))
                # Reset the palette when a new image is displayed
                for i in range(self.palette_length):
                    self.color_frame_list[i].config(bg=self.window_color) # Reset color frames
                    self.hex_label_list[i].config(text="") # Reset hex code labels
        except (IsADirectoryError, PIL.UnidentifiedImageError, TimeoutError): # In the case a directory/non-image file is selected
            # Display error message for an invalid image file
            messagebox.showerror("ERROR!", "Invalid image file.\nPlease try again.")
        else:
            # If the image file path exists
            if image_file_path:
                self.image_path_entry.config(state="normal")  # Allow text entry to be edited
                self.image_path_entry.delete(0, tk.END) # Delete all text inside entry
                self.image_path_entry.insert(0, image_file_path) # Write image file path to entry
                self.image_path_entry.config(state="readonly")  # Set it back to read only
