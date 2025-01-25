import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('../../insurance.db')
cursor = conn.cursor()

# Create the products table with NOT NULL constraints
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('Death', 'TPD', 'Critical Illness', 'Accidental', 'Hospitalisation')),
        descriptions TEXT NOT NULL
    )
''')
conn.commit()

# Define the types and corresponding descriptions for each product
types = ['Death', 'TPD', 'Critical Illness', 'Accidental', 'Hospitalisation']
product_details = {
    'A': '{"coverage": "term", "premium": 100, "SA":10000}',
    'B': '{"coverage": "endowment", "premium": 200, "SA":20000}',
    'C': '{"coverage": "full", "premium": 300, "SA":30000}'
}

# Insert 3 products for each type
for t in types:
    for label, desc in product_details.items():
        name = f'{t} {label}'
        cursor.execute('''
            INSERT INTO products (name, type, descriptions)
            VALUES (?, ?, ?)
        ''', (name, t, desc))

conn.commit()

# Fetch data
cursor.execute('SELECT * FROM products')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close connection
conn.close()