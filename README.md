# Image Metadata to KML Converter

This Python script fetches GPS coordinates from JPEG images and creates a KML (Keyhole Markup Language) file that can be used to display the images' locations in Google Earth.

## Requirements

- Python 3.x
- `piexif` library (install via `pip install piexif`)
- `Pillow` library (install via `pip install Pillow`)

## Usage

1. Clone the repository or download the source code.
2. Open a terminal or command prompt and navigate to the project directory.
3. Run the script with the following command:

   ```shell
   python script.py


The script will prompt you to enter the path of the folder where the JPEG images are located.
After providing the folder path, the script will generate a KML file named output.kml in the current directory.
Open the KML file in Google Earth to visualize the image locations on the map.
Please note that the script requires the images to have GPS information embedded in their EXIF metadata. If any images lack GPS information, the script will display an error message for those images.