import sqlite3

# Connect to the database
conn = sqlite3.connect("image_processing.db")
cursor = conn.cursor()

# Reset all completed images back to "processing"
cursor.execute("UPDATE images SET status='processing' WHERE status='completed'")
conn.commit()

print("✅ Image status reset to 'processing'.")

conn.close()
