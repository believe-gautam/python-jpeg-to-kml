

import os
import piexif
from PIL import Image

def extract_gps_info(image_path):
    exif_data = piexif.load(image_path)
    gps_ifd = exif_data.get("GPS", {})
    latitude = gps_ifd.get(piexif.GPSIFD.GPSLatitude)
    longitude = gps_ifd.get(piexif.GPSIFD.GPSLongitude)
    latitude_ref = gps_ifd.get(piexif.GPSIFD.GPSLatitudeRef)
    longitude_ref = gps_ifd.get(piexif.GPSIFD.GPSLongitudeRef)

    if latitude and longitude and latitude_ref and longitude_ref:
        lat = latitude[0][0] / latitude[0][1] + latitude[1][0] / latitude[1][1] / 60 + latitude[2][0] / latitude[2][1] / 3600
        lon = longitude[0][0] / longitude[0][1] + longitude[1][0] / longitude[1][1] / 60 + longitude[2][0] / longitude[2][1] / 3600

        if latitude_ref.decode() == 'S':
            lat = -lat
        if longitude_ref.decode() == 'W':
            lon = -lon

        return lat, lon

    raise ValueError("No GPS information found in the image's EXIF data.")


def create_kml(image_path):
    # Open the image using PIL
    image = Image.open(image_path)

    # Get the image size
    width, height = image.size

    # Extract GPS info
    try:
        lat, lon = extract_gps_info(image_path)
    except ValueError as e:
        print(f"Error: {e}")
        return None

    # Create the KML content
    kml_content = f'''<Placemark>
        <name>{image_path}</name>
        <description><![CDATA[<img src="{image_path}" width="300" height="200" />]]></description>
        <Point>
            <coordinates>{lon},{lat},0</coordinates>
        </Point>
    </Placemark>'''

    return kml_content


def process_images_in_folder(folder_path, output_path):
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print("Error: Folder does not exist.")
        return

    # Get the list of image files in the folder
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.jpg', '.jpeg'))]

    if not image_files:
        print("No image files found in the folder.")
        return

    # Create the KML file
    kml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
    {"".join(create_kml(os.path.join(folder_path, image_file)) for image_file in image_files)}
    </Document>
</kml>'''

    # Save the KML file
    with open(output_path, 'w') as file:
        file.write(kml_content)

    print(f'KML file "{output_path}" created successfully.')


# Example usage
folder_path = 'data'
output_path = 'output.kml'

# Process the images in the folder and generate a single KML file
process_images_in_folder(folder_path, output_path)
