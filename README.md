# Image Processing System 🖼️

This project is a **backend system** that processes images uploaded via a CSV file. The system **compresses images**, stores them in a database, and provides APIs for checking status, exporting results, and sending webhook notifications when processing is completed.

---

## 🚀 Features
- 📂 Upload CSV with image URLs (`POST /upload`)
- 🔄 Process Images (Compress by 50%)
- 📊 Check Status of image processing (`GET /status/<id>`)
- 📤 Export Processed Data as CSV (`GET /export`)
- 🔔 Webhook Notification when processing is completed (`POST /webhook`)

---

## 🛠️ Technologies Used
- Flask (Python Web Framework)
- SQLite (Database)
- Pandas (CSV Handling)
- Pillow (PIL) (Image Processing)
- cURL (API Testing)

---

## 📌 API Endpoints

**POST /upload** – Upload a CSV file with image URLs  
**GET /status/<id>** – Check processing status for an image ID  
**GET /export** – Export processed data as a CSV file  
**POST /webhook** – Webhook to receive processing completion notifications  

---

## ⚡ How to Run

### 1️⃣ Clone the Repository  
git clone https://github.com/Roshan181519/image-processing-system.git  

### 2️⃣ Navigate to the Project Folder  
cd image-processing-system  

### 3️⃣ Create a Virtual Environment & Activate It  
python -m venv venv  
venv\Scripts\activate  # For Windows  

### 4️⃣ Install Dependencies  
pip install -r requirements.txt  

### 5️⃣ Start the Flask Server  
python app.py  

### 6️⃣ Test APIs Using cURL  

#### Upload CSV  
curl -X POST -F "file=@sample.csv" http://127.0.0.1:5000/upload  

#### Check Processing Status  
curl -X GET http://127.0.0.1:5000/status/5  

#### Export Processed Data  
curl -X GET http://127.0.0.1:5000/export -o processed_images.csv  

#### Trigger Webhook Manually  
curl -X POST http://127.0.0.1:5000/webhook -H "Content-Type: application/json" -d '{"image_id": 5, "status": "completed", "output_images": ["compressed_images/compressed_5_0.jpg"]}'  

---

## 🏗️ Role and Function of Each Component

### 1️⃣ Image Processing Service Interaction
- The **image processor** downloads images from given URLs, compresses them, and updates the database with processed image paths.
- Runs asynchronously, ensuring efficient handling of multiple images.

### 2️⃣ Webhook Handling
- The **webhook API (`/webhook`)** receives notifications when image processing is completed.
- External systems can subscribe to this webhook to receive updates automatically.

### 3️⃣ Database Interaction
- Uses **SQLite** to store image processing requests and track their status.
- Schema includes:
  - `id` (Unique identifier for each request)
  - `product_name` (Name of the product associated with images)
  - `input_image_urls` (Original image URLs)
  - `output_image_urls` (Compressed image paths)
  - `status` (`processing` → `completed` when done)

### 4️⃣ API Endpoints
- **Upload API (`POST /upload`)** – Accepts a CSV file and stores image URLs in the database.
- **Status API (`GET /status/<id>`)** – Checks the processing status of an image request.
- **Export API (`GET /export`)** – Allows users to download a CSV with processed image details.
- **Webhook API (`POST /webhook`)** – Notifies external services when processing is completed.

---
 

---

✅ **Project is complete!** 🎉

