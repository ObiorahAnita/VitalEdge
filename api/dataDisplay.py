import requests
import sqlite3

request = requests.get('http://127.0.0.1:8000')
print(request.json())

# Connect to your database
conn = sqlite3.connect("PINT.db")
cursor = conn.cursor()

# Query the table
cursor.execute("SELECT * FROM records")  # display all data in this table
rows = cursor.fetchall()

# Print results
for row in rows:
    print(row)

# Close the connection
conn.close()