import requests
import sqlite3

request = requests.get('http://127.0.0.1:8000')
print(request.json())

# Connect to your database
conn = sqlite3.connect("PINT.db")
cursor = conn.cursor()

# Query the table
cursor.execute("SELECT * FROM records")  # Replace 'my_table' with your table name
rows = cursor.fetchall()

# Print results
for row in rows:
    print(row)

# Close the connection
conn.close()