import psycopg2

# Open a connection to the database
conn = psycopg2.connect(database="test", user="postgres", password="apeed", host="localhost", port="5432")

# Read the image data from a file
with open("camera.jpg", "rb") as f:
    image_data = f.read()

# Insert the image data into the database
cur = conn.cursor()
cur.execute("INSERT INTO images (name, data) VALUES (%s, %s)", ("camera.jpg", psycopg2.Binary(image_data)))
conn.commit()

# Close the database connection
cur.close()
conn.close()
