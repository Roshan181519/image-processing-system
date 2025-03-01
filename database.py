import sqlite3

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect("image_processing.db")
cursor = conn.cursor()

# Create a table to store CSV data and processed images
cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        input_image_urls TEXT NOT NULL,
        output_image_urls TEXT,
        status TEXT DEFAULT 'processing'
    )
''')

# Commit and close connection
conn.commit()
conn.close()

print("Database and table created successfully!")
