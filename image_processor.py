import sqlite3
import requests
from PIL import Image
from io import BytesIO
import os

# Webhook URL (Change this to the actual endpoint where notifications should be sent)
WEBHOOK_URL = "http://127.0.0.1:5000/webhook"

# Create a folder to save compressed images
OUTPUT_FOLDER = "compressed_images"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Connect to the database
conn = sqlite3.connect("image_processing.db")
cursor = conn.cursor()

# Fetch unprocessed images
cursor.execute("SELECT id, input_image_urls FROM images WHERE status='processing'")
rows = cursor.fetchall()

print(f"Found {len(rows)} rows to process")  # Debugging line

for row in rows:
    image_urls = row[1].split(",")  # Get image URLs
    compressed_urls = []  # To store compressed image paths
    
    for index, url in enumerate(image_urls):
        url = url.strip()  # Remove extra spaces
        try:
            print(f"Downloading image: {url}")  # Debugging line

            # Download the image with a User-Agent header
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad response

            # Open the image
            image = Image.open(BytesIO(response.content))

            # Convert RGBA to RGB if needed
            if image.mode == "RGBA":
                image = image.convert("RGB")

            # Compress and save the image
            output_path = os.path.join(OUTPUT_FOLDER, f"compressed_{row[0]}_{index}.jpg")
            image.save(output_path, "JPEG", quality=50)

            compressed_urls.append(output_path)

            print(f"Saved to: {output_path}")  # Debugging line
        
        except Exception as e:
            print(f"Error processing {url}: {e}")  # Now prints actual error messages

    # Only update the database if images were successfully processed
    if compressed_urls:
        cursor.execute(
            "UPDATE images SET output_image_urls=?, status='completed' WHERE id=?",
            (",".join(compressed_urls), row[0])
        )
        conn.commit()

        # ✅ Trigger the webhook after processing is completed
        webhook_data = {
            "image_id": row[0],
            "status": "completed",
            "output_images": compressed_urls
        }
        try:
            print(f"Triggering webhook for image ID {row[0]}...")
            response = requests.post(WEBHOOK_URL, json=webhook_data)
            print(f"Webhook Response: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error triggering webhook: {e}")

conn.close()
print("Image processing completed successfully!")
