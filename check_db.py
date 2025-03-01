import sqlite3

# Connect to the database
conn = sqlite3.connect("image_processing.db")
cursor = conn.cursor()

# Fetch all rows from the images table
cursor.execute("SELECT * FROM images")
rows = cursor.fetchall()

# Print the stored data
for row in rows:
    print(row)

conn.close()
