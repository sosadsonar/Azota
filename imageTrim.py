from PIL import Image
import requests
import io 


def crop_image_from_url(image_url, crop_coordinates, output_filename):
    """
    Downloads, crops, and saves an image from a URL.

    Args:
        image_url: The URL of the image to be downloaded.
        crop_coordinates: A tuple of (left, top, right, bottom) coordinates for cropping.
        output_filename: The filename for the saved cropped image.
    """
    try:
        # Download the image
        response = requests.get(image_url)

        # Check for successful download
        if response.status_code == 200:
            image_data = response.content

            # Open the image in memory
            image = Image.open(io.BytesIO(image_data))

            # Crop the image
            cropped_image = image.crop(crop_coordinates)

            # Save the cropped image
            print("Putting images")
            cropped_image.save(output_filename, format="PNG")
            print(f"Image cropped and saved successfully to '{output_filename}'.")
            
        else:
            print(f"Error downloading image: {response.status_code}")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    crop_image_from_url()
