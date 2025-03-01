from flask import Flask, request, jsonify
import sqlite3
import pandas as pd
import uuid
from flask import Response

app = Flask(__name__)

# Function to connect to the database
def connect_db():
    return sqlite3.connect("image_processing.db")

# API to upload CSV
@app.route("/upload", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    # Read CSV file
    df = pd.read_csv(file)

    # Check required columns
    required_columns = ["Product Name", "Input Image Urls"]
    if not all(col in df.columns for col in required_columns):
        return jsonify({"error": "Invalid CSV format"}), 400

    # Generate a unique request ID
    request_id = str(uuid.uuid4())

    # Store data in the database
    conn = connect_db()
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO images (product_name, input_image_urls, status) VALUES (?, ?, 'processing')",
            (row["Product Name"], row["Input Image Urls"]),
        )

    conn.commit()
    conn.close()

    return jsonify({"message": "File uploaded successfully!", "request_id": request_id}), 200

# ✅ New Status API to check processing status
@app.route("/status/<int:image_id>", methods=["GET"])
def check_status(image_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT product_name, input_image_urls, output_image_urls, status FROM images WHERE id=?", (image_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({
            "product_name": row[0],
            "input_image_urls": row[1],
            "output_image_urls": row[2] if row[2] else "Processing...",
            "status": row[3]
        })
    else:
        return jsonify({"error": "Image ID not found"}), 404
    # ✅ Webhook API to receive processing completion notifications
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(f"Webhook received: {data}")  # Debugging

    return jsonify({"message": "Webhook received successfully!"}), 200


# ✅ API to export processed data as CSV
@app.route("/export", methods=["GET"])
def export_csv():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Fetch processed images
    cursor.execute("SELECT id, product_name, input_image_urls, output_image_urls, status FROM images WHERE status='completed'")
    rows = cursor.fetchall()
    conn.close()

    # Create CSV data
    def generate():
        yield "Image ID,Product Name,Input Image URLs,Output Image URLs,Status\n"
        for row in rows:
            yield f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}\n"

    # Return CSV file
    return Response(generate(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=processed_images.csv"})



if __name__ == "__main__":
    app.run(debug=True)
