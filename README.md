# COLOR PALETTE

Eyedropper application that allows you to extract colors and hex codes from any image file on your computer.

## Installation
Use package manager pip to install the following:

```bash
pip install pillow
```

## Usage
To build the executable file, use the terminal to navigate to the same directory as the main.py file and run the command below:

```bash
pyinstaller main.py --hidden-import=tkinter --onefile --windowed --add-data "../assets:assets" --icon=../assets/palette.icns --name "<Desired Name of Executable>"
```

Open up the dist file to find an executable file with your desired name, and open it.

To start, click the "Browse Image File" button to open up your computer's file system. 
Then, select the image file you want to open. Your image will be displayed on the canvas.
Click anywhere on the image to get the hex code and color of the clicked pixel.
You can hold up to 8 hex codes/colors at once.

## Contact
For any questions, contact me at gavinkiosco@gmail.com or CrypticT1tan on GitHub.

## Attribution
Icon made by Freepik from www.flaticon.com