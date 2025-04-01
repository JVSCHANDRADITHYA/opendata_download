import os
import pandas as pd
import requests
from tqdm import tqdm

# Set default folder
DEFAULT_SAVE_FOLDER = os.path.join(os.getcwd(), "NGA_Dataset")

def convert_iiif_to_jpg(iiif_url):
    """Convert IIIF API URL to a direct image download URL."""
    return iiif_url + "/full/full/0/default.jpg"

def download_image(url, save_folder):
    """Download an image from a URL and save it to the specified folder."""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_name = url.split("/")[-3] + ".jpg"  # Extract unique ID
            file_path = os.path.join(save_folder, file_name)
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False

def download_dataset(csv_path, save_folder=DEFAULT_SAVE_FOLDER):
    """Download all images from the dataset CSV file."""
    os.makedirs(save_folder, exist_ok=True)
    df = pd.read_csv(csv_path)

    if 'iiifurl' not in df.columns:
        print("Error: 'iiifurl' column not found in CSV.")
        return

    image_urls = df['iiifurl'].dropna().apply(convert_iiif_to_jpg).tolist()

    print(f"Starting download of {len(image_urls)} images...")
    for url in tqdm(image_urls):
        download_image(url, save_folder)

    print(f"✅ All images downloaded to: {save_folder}")

if __name__ == "__main__":
    csv_path = input("Enter the path to published_images.csv: ").strip()
    save_folder = input(f"Enter save location (default: {DEFAULT_SAVE_FOLDER}): ").strip() or DEFAULT_SAVE_FOLDER
    download_dataset(csv_path, save_folder)
